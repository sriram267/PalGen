# PalGen Platform — System Design (Channel Orchestration + Campaign Management, Lead-Ready and API-First)

**Date:** 12 October 2026
**Status:** Target-state architecture. Only phase-gated work in `implementation_roadmap.md` is committed.

**Product:** PalGen, a multi-tenant sales and marketing ERP built on its own channel orchestration layer over third-party providers (no carrier infrastructure, no raw CPaaS). **Now:** orchestration + Campaign Management. **Later:** Developer API (additional monetization) and Lead Management. **Commercial model:** pay-as-you-go. **Pal** is the optional ambient interface.

**Core stack (starting point):** React, TypeScript, Node.js, PostgreSQL. Add Redis, Kafka, Temporal only when a workflow justifies them (Section 14).

> Principle: build a serious modular monolith with hard domain boundaries and a correct ledger. Extract only what has a demonstrated operational boundary.

---

## 1. Product boundary

```
PalGen
├── Platform: tenancy, identity, roles, entitlements, contacts, consent, connections, audit
├── Billing: plans, payment gateway, LEDGER, recharge, invoices
├── Orchestration (CPaaS-style): canonical messaging, channel adapters, routing/fallback, delivery tracking, webhooks
│     whatsapp · sms · email · instagram · phone(voice plane, isolated)
├── Campaigns: audiences, templates, campaigns, scheduling, throttling, inbox, reports
├── Developer API (LATER): public API, keys, logs, outbound webhooks, sandbox, SDKs
├── Leads (LATER): pages, ads consoles, SEO/AEO, pipeline, attribution
└── Pal: event consumer and action surface
```

Three rules shape everything:
1. **Integration ≠ recharge.** The connection to a provider and the commercial consumption of that channel are separate domains.
2. **Lead-ready now.** No shared model may assume campaigns are the only producer of contacts, events, or attribution (readiness contract in `product_strategy.md` §6).
3. **API-first.** The web app calls the same documented domain API a developer would, so the Developer API later is exposure, not a rewrite (Section 10a).

## 2. High-level topology

```
 React Web (TypeScript)
        │ HTTPS / WSS
        ▼
┌───────────────────────── Application plane ─────────────────────────┐
│  Node.js modular monolith                                           │
│  platform │ billing │ orchestration │ campaigns │ contacts │ pal │ (leads) │
└───────┬───────────────────┬──────────────────┬──────────────────────┘
        ▼                   ▼                  ▼
   PostgreSQL          Job workers        Webhook ingest
 (source of truth)   (send, retry,        (verify, dedupe,
  incl. outbox,       reconcile,           resolve tenant,
  ledger, queue)      import, schedule)    enqueue)
                          │                   ▲
                          ▼                   │
                ┌──── Provider adapters ──────┴───────┐
                │ WhatsApp │ SMS │ Email │ Instagram  │
                └───────────────┬─────────────────────┘
                                ▼
                   Third-party providers / Meta / carriers

        ┌──────── Telephony plane (separate infrastructure) ────────┐
        │ SIP provider ▸ SBC/PBX ▸ WebRTC edge ▸ browser softphone  │
        └───────────────────────────────────────────────────────────┘
```

The telephony plane is separate from day one because media, networking, and carrier failure modes differ. See `erp_webrtc_telephony_system_design.md`.

## 3. Modular monolith layout

```
apps/
  web/            React app (shell generated from the module registry)
  api/            HTTP + WebSocket API
  workers/        send, retry, reconcile, import, scheduler
packages/
  domain/ contracts/ database/ events/ auth/ observability/ config/

api/src/modules/
  identity/ tenancy/ entitlements/ audit/ notifications/
  contacts/            contacts, event timeline, consent, tags, custom fields
  connections/         provider accounts, OAuth/tokens, health
  billing/             plans, payments, ledger, recharge, invoices
  orchestration/
    core/              canonical message model, delivery state machine, templates
    adapters/          whatsapp/ sms/ email/ instagram/ (voice → telephony plane)
    webhooks/          ingest, verification, dedupe
  campaigns/           audiences, campaigns, schedules, throttling, inbox, reports
  pal/                 event projection, cards, action dispatcher
  leads/               (reserved — empty until Phase 7)
```

A module exposes a contract and does not reach into another module's tables. Cross-module reactions use domain events (Section 8).

## 4. Tenancy and authorization

```
request → authenticate → resolve tenant (server-side) → authorize → domain operation → database
```

- `organization_id` on every tenant-owned row; never trust a tenant ID from the client.
- PostgreSQL Row-Level Security as defense in depth.
- Every job and webhook carries tenant context; webhook handlers resolve the tenant from provider identifiers, never from payload claims alone.
- Automated cross-tenant tests for API, jobs, webhooks, exports.

## 5. Contacts, timeline, consent (the lead-ready spine)

```
contacts(id, organization_id, display_name, phones[], emails[], handles{instagram,...},
         lifecycle_stage, source, medium, first_touch, last_touch, owner_id,
         custom_fields jsonb, tags, created_at, ...)
contact_events(id, organization_id, contact_id, type, occurred_at, source_module,
               entity_ref, payload jsonb)           -- append-only
consents(id, organization_id, contact_id, channel, purpose, status,
         evidence, captured_at, withdrawn_at)
```

- `lifecycle_stage`, `source`, `medium`, `first_touch`, `last_touch` exist now (nullable). Campaign Management uses `source` for imports and forms; Lead Management fills the rest.
- Event types today: `message.sent/delivered/read/failed`, `message.received`, `consent.granted/withdrawn`, `contact.imported`. Later: `page.viewed`, `form.submitted`, `ad.clicked`, `stage.changed`.
- Identity resolution (merge duplicates) is designed as an explicit, audited operation.
- Audiences compile to queries over contacts and events, so adding lead filters later requires no new engine.

## 6. Connections hub

```
connections(id, organization_id, provider, kind[channel|ad_account|site], external_id,
            scopes, secret_ref, status, health, last_checked_at, last_error)
```

- Status vocabulary shared with the UX: *not connected, needs authorization, pending approval, active, suspended, error*.
- Secrets are references into a secret manager or encrypted storage, never returned to the browser.
- Token refresh, health checks, and review/approval state are generic. Instagram uses this now; Google and Meta Ads reuse it later.

## 7. Channel orchestration core

### 7.1 Canonical model

```
message(id, organization_id, channel, direction, contact_id, conversation_id,
        template_id?, content, status, provider, provider_message_id,
        idempotency_key, campaign_id?, cost_ref?, created_at)
```

Delivery state machine (superset; channels use subsets):

```
queued → submitted → sent → delivered → read
   │         │         └────────────→ failed(reason)
   └── rejected/blocked/expired/opted_out
```

- Provider statuses map into this machine; unmapped statuses are stored raw and alerted on.
- Events may arrive duplicated, delayed, or out of order; transitions are monotonic and idempotent.
- Inbound messages create or update conversations, contact events, and consent changes (e.g. STOP).

### 7.2 Adapter interface

```
Adapter {
  capabilities(): ChannelCapabilities      // templates, windows, media, receipts, pricing unit
  connect/verify(connection)
  submitTemplate(), getTemplateStatus()
  send(message): ProviderResult            // timeout, retry class, rate limit declared
  parseWebhook(request): NormalizedEvent[]
  fetchUsage(range): UsageRecord[]         // for reconciliation
}
```

- No provider vocabulary leaks outside adapters.
- Each adapter ships with a contract test suite and a fake provider for tests.
- Channels are not assumed equal: WhatsApp has template categories and conversation rules, SMS has sender and template registration constraints, email has domain authentication and reputation, Instagram has messaging-window rules. Capabilities are explicit, not hidden.

### 7.3 Send pipeline

```
campaign run → resolve audience → consent check → per-message idempotency key
   → ledger RESERVE (credits) → enqueue send job → adapter.send
   → provider result → ledger DEBIT (commit) / RELEASE (failed) → events
```

- Throttling per tenant, per channel, and per provider limit.
- Poison messages go to a dead-letter state with an operator view.
- Pausing a campaign stops new jobs; in-flight sends settle normally.

### 7.4 Orchestration rules

- **Routing and fallback:** per-campaign or per-contact rules such as WhatsApp → wait → check delivery/read → SMS or email. Evaluated by scheduled jobs against message state; no new infrastructure at first. Durable workflow tooling (Temporal) is added only if journeys become long-running or complex.
- **Frequency caps and quiet hours:** enforced at send time using the contact event timeline, per tenant policy.
- **Preferences:** per-contact, per-channel, per-purpose (marketing versus transactional), backed by the consent records in Section 5.
- **One delivery log:** every attempt, including fallback steps, is a message record linked to the same campaign step.

## 8. Events and the outbox

- State change and an `outbox_events` row commit in the same PostgreSQL transaction.
- A publisher delivers outbox events to in-process subscribers and the job queue. **No Kafka initially**; the event contract (`event_id`, `type`, `organization_id`, `module`, `entity`, `occurred_at`, `payload`) is stable so a broker can be added later without rewriting producers.
- Consumers are idempotent (unique `event_id` per consumer).
- Subscribers: Pal projection, reporting facts, notifications, billing reconciliation triggers.

## 9. Ledger and recharge

Principles: immutable, idempotent, auditable, projected balance.

```
ledger_accounts(id, organization_id, namespace, channel?, currency_or_unit)
   namespace ∈ communication_credit | subscription | provider_cost | ad_spend_reference
ledger_entries(id, organization_id, account_id, direction, amount, unit,
               kind[recharge|reserve|debit|release|refund|adjustment],
               idempotency_key UNIQUE, ref_type, ref_id, provider, provider_ref,
               reconciliation_status, created_at)    -- never updated
balances = projection(ledger_entries)                  -- rebuildable
```

- **Reserve → commit/release** prevents campaigns from overspending.
- **Pay-as-you-go:** usage debits are the primary revenue event. Each debit stores the rate-card version and unit price used, and the usage `source` (campaign, inbox, API key), so charges stay explainable when prices change.
- Corrections are new adjustment entries; history is never edited.
- Provider usage import is matched against debits; mismatches enter a reconciliation queue.
- **Provider cost and customer price are separate accounts**, so margin is measurable per channel.
- **Ad spend never enters `communication_credit`.** The `ad_spend_reference` namespace is for read-only display of platform-paid spend in Phase 7.
- Payments: gateway webhooks are idempotent; a recharge becomes a ledger credit only after confirmed payment; refunds and disputes have defined paths.

## 10. Campaign Management

- Audiences: saved queries over contacts/events with snapshot-at-send semantics.
- Campaigns: one or more channel steps, schedule, throttle, budget cap, status machine (`draft → scheduled → running → paused → completed/failed`).
- Templates: per-channel with provider approval status.
- Reports read from events and facts, scoped by campaign/channel/contact set (later source or ad).
- Inbox: conversations over `message` and `contact_events`; assignment and status. Phase 5.

## 10a. API-first design and the Developer API

Pay-as-you-go developers are a second buyer, served by the same layer. Design rules from Phase 1:

- **One domain API.** The web app uses it; nothing important is only available through private endpoints.
- **Versioned, documented contracts** with a stable error model; breaking changes need a new version.
- **API keys** are tenant-scoped, hashed at rest, scoped by permission, rotatable, and attributable (`api_key_id` on messages and ledger entries).
- **Idempotency keys** on all mutating endpoints; the same key never produces a second send or a second debit.
- **Rate and spend limits** per key and per tenant; new-account sending limits.
- **Outbound webhooks** signed, retried with backoff, with a delivery log.
- **Sandbox** uses fake provider adapters and a separate ledger namespace; no real sends.
- **Abuse and fraud controls:** velocity limits, destination and content rules, complaint thresholds, and spend alerts. Raw sending APIs attract abuse; this is a launch gate for Track D.
- **Consent purposes:** transactional and marketing messages use different consent and preference rules.
- The API is **not publicly exposed** until the Track D gate in the roadmap.

## 11. Pal architecture

```
domain event → outbox → Pal projector → severity/dedupe/priority → Pal event → realtime gateway → UI
```

- Pal reads authoritative state and projections; it never invents business state.
- Event schema is module-agnostic: `event_id, module, entity, severity, title, why, actions[], expires_at`.
- Actions call ordinary domain APIs: server-side authorization, confirmation for consequential operations, idempotency key, audit record.
- Initial event types: low credits, template rejected, campaign failing, reply waiting, connection needs authorization.

## 12. Security

- Edge: WAF/CDN, TLS, rate limits. App: MFA, RBAC, tenant authorization, CSRF, input validation, secure headers, audit logs.
- Provider tokens and API keys encrypted, referenced not exposed, rotated; webhook signatures verified; replay windows enforced.
- PII minimization: contact data, message content, and recordings are sensitive; retention and deletion policies per tenant.
- Abuse controls: spam/complaint thresholds, sending limits for new tenants, blocklist handling, spend limits.
- Consent evidence stored; opt-out honored across channels per policy.

## 13. Reliability, SLOs, observability

Every async operation answers: *what happens if this dies right now?* Retries use backoff; every job is idempotent; every external call has timeout, retry policy, rate limit, audit, and a failure UX.

Initial targets (engineering goals, not claims): API availability 99.9%; read p95 < 300 ms; write p95 < 500 ms; WebSocket delivery < 1 s; webhook-to-state update < 5 s normal; scheduled campaign start within agreed skew; RPO/RTO defined per data class (ledger is highest).

Telemetry carries `trace_id, request_id, organization_id, user_id, job_id, event_id, message_id, campaign_id`.

## 14. When to add heavier infrastructure

| Component | Add when |
|---|---|
| Redis | Rate limiting, caching, presence, or queue throughput outgrows PostgreSQL |
| Kafka | Multiple independent consumers, replay, or throughput need fan-out beyond the outbox |
| Temporal | Long-running workflows with durable timers, human approvals, or compensation (e.g. drip journeys, approvals) |
| Separate services | A boundary with distinct scaling, security, reliability, or ownership needs |

Each addition requires a documented reason, owner, failure mode, recovery plan, and cost.

## 15. Scaling path

1. One API deployment + workers + PostgreSQL; separate telephony infrastructure.
2. Multiple stateless API instances; dedicated send workers per channel; Redis if needed.
3. Workload isolation: realtime gateway, reconciliation workers, reporting workers.
4. Selective extraction (likely the orchestration core, once the Developer API has its own scaling needs) once boundaries are proven.

## 16. Lead Management extension points (designed now, built later)

| Future need | Existing hook |
|---|---|
| Landing pages and visitor tracking | `contact_events`, `source/medium/first_touch`, consent, a site connection in the hub |
| Meta/Google Ads consoles | Connections hub (OAuth, scopes, review state), `ad_spend_reference` namespace, event timeline for clicks and conversions |
| Content writing and SEO/AEO | Module registry and entitlements, job/worker framework, Pal events |
| Lead pipeline and scoring | `lifecycle_stage`, owner, events, audiences |
| Attribution and funnel reports | Event facts across modules, report scopes |

A `leads/` module directory exists but stays empty. No lead tables ship until Phase 7.

## 17. Repository layout

```
palgen/
├── apps/ (web, api, workers)
├── packages/ (domain, contracts, database, events, auth, observability, config)
├── telephony/ (sip, routing, media, webrtc, provisioning)   # separate plane
├── infrastructure/ (docker, terraform, secrets, observability)
└── docs/ (architecture, adr, api, events, security, runbooks)
```

## 18. What we will not build yet

Microservices per module; Kafka/Temporal by default; multi-region; service mesh; custom SIP stack; event sourcing for everything; an AI agent swarm; any Lead Management feature; a public Developer API before Track D; generic ERP domains.

## 19. Architecture principle

This is the canonical baseline. Evolve modules, contracts, and infrastructure boundaries inside it; do not redesign the stack when a feature arrives. Any new component needs an ADR with reason, owner, failure mode, recovery plan, and cost.

Initial ADRs: modular monolith · PostgreSQL source of truth · channel adapter contract · immutable ledger with reserve/commit · single Contact entity and event timeline · connections hub · transactional outbox · tenant isolation · API-first domain API · telephony plane isolation · observability standard.
