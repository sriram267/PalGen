# PalGen Implementation Roadmap — Evidence-Gated Delivery

**Date:** 12 October 2026
**Rule:** Phases are gates, not calendar promises. Do not advance because code exists; advance because the exit gate is met.
**Scope:** channel orchestration → Campaign Management now; Developer API as a parallel monetization track; Lead Management later but designed for from Phase 1.

```
P0 Validate ─▶ P1 Foundation ─▶ P2 First channel ─▶ P3 Campaigns v1 ─▶ P4 More channels
                                                                           │
P8 Scale/Intl ◀─ P7 Lead Mgmt ◀─ P6 Phone pilot ◀─ P5 Pal + Inbox ◀──────┘
```

Phases 0 and 1 overlap: provider and compliance work runs alongside the foundation build. **Track D (Developer API)** is not a numbered phase; it can start once Phase 3 exit shows paid usage.

## Phase 0 — Validation and provider groundwork

**Goal:** confirm who buys Campaign Management first, which channel leads, and that the economics work.

Deliverables:
- 15–25 structured interviews across a few candidate segments (Chennai first)
- Current campaign workflow maps: tools, costs, workarounds, failure points, buying authority
- Alternatives matrix (Interakt/Wati-style tools, SMS gateways, email tools, CRMs, agencies) and switching-cost notes
- Provider shortlist per channel with commercial terms and margin model (WhatsApp BSP or Cloud API; SMS aggregator; email provider; Instagram access path)
- Compliance map: SMS sender/template registration, WhatsApp business verification and template approval, consent and opt-out, email domain authentication
- Clickable prototypes of the campaign workflow and the Connections/Wallet screens
- Scored workflows (framework in `product_strategy.md`), design-partner shortlist, pilot hypotheses

Exit gate:
- One primary buyer segment and first channel chosen with evidence
- 3–5 credible design partners, preferably with pilot commitments
- Unit economics per message estimated from real provider quotes
- Success metric and willingness-to-pay test defined

## Phase 1 — Platform foundation and channel orchestration core

**Goal:** the thin shared platform and the orchestration skeleton, built lead-ready and API-first.

Build only what the first channel needs, but with the readiness contract applied:
- Tenants, memberships, authentication, roles, audit trail
- Module entitlement registry (Campaign Management sold; Lead Management registered, unavailable)
- **Contacts + event timeline + consent** (single entity for customers and future leads)
- **Connections hub** (generic provider connection model, secrets handling, health states)
- **Ledger:** immutable entries, idempotency keys, reservations, adjustments; wallet balance as projection
- Canonical message model, adapter interface, delivery state machine, webhook ingest (verified, deduplicated, tenant-resolved)
- Job queue with retries, rate limits, and tenant context (PostgreSQL-backed to start)
- **API-first discipline:** the web app calls the same domain API a developer would; API keys and scopes, idempotency keys, per-key rate limits, outbound webhooks, and per-source usage attribution (campaign, inbox, API key) are designed in, but not publicly exposed
- PostgreSQL schema with migration discipline; telemetry, error reporting, backups

Exit gate:
- Tenant-isolation tests pass; a mock adapter exercises send → receipt → inbound → debit end-to-end
- Ledger invariants proven by tests (no balance without entries; duplicate events do not double-debit)
- Information architecture reserves Leads and Ads areas (see `ux_information_architecture.md`)

## Phase 2 — First channel end-to-end (hypothesis: WhatsApp)

**Goal:** one real channel, integration and recharge, in a design partner's hands.

Deliverables:
- Integration: provider onboarding, sender identity, template create/submit/approval status, send, delivery/read receipts, inbound messages, opt-out handling
- Recharge (pay-as-you-go): credit purchase via payment gateway, per-message pricing with the rate-card version stored on each debit, debit on send, refunds/adjustments, customer-visible usage
- Provider usage import and reconciliation
- Clear failure states: not connected, needs authorization, template pending, out of credits, suspended

Exit gate:
- A design partner connects the channel and sends real messages without developer help
- Usage and provider costs reconcile within an agreed tolerance
- Billing errors are corrected by adjustment entries, never by editing history

## Phase 3 — Campaign Management v1

**Goal:** the first sold module on the first channel.

Deliverables:
- Audiences/segments over Contacts (including lifecycle-stage and source filters, even though leads are not yet captured)
- Templates, campaign builder, scheduling, throttling, credit reservation and budget cap, pause/resume
- Orchestration rules: channel fallback (e.g. WhatsApp, then SMS or email if undelivered after a wait), frequency caps, quiet hours, per-contact preferences
- Campaign reports: sent, delivered, read, failed, replied, opted out, cost
- Import (CSV) with consent capture
- Terms, privacy, retention, and support policies reviewed

Exit gate:
- At least one customer pays or signs a credible paid pilot
- Campaign outcome metric measured for pilots
- Support burden and gross margin per message are known

## Phase 4 — Additional channels

**Goal:** add one channel at a time; each channel ships integration **and** recharge together.

Order (hypothesis, re-confirm with evidence): Email → SMS → Instagram. Each channel needs: provider choice, compliance gate, adapter, pricing/ledger rules, templates or sender setup, campaign support, tests, runbook.

Exit gate per channel: documented buyer demand, passing adapter contract tests, reconciliation working, support owner named, rollback plan.

## Phase 5 — Conversations/inbox and Pal v1

**Goal:** make replies and operational events actionable.

- Shared inbox for WhatsApp and Instagram (and email/SMS replies where supported), assignment, status, canned replies
- Pal v1: one compact surface, two or three event types (low credits, template rejected, campaign failing, reply waiting), at most two actions per card, server-authorized, confirmed, idempotent, audited
- Dismiss/snooze, keyboard and screen-reader support, reduced motion, responsive layout

Exit gate: users can explain why an alert appeared; duplicate alerts controlled; actions cannot bypass permissions; measurable utility versus the normal UI.

## Phase 6 — Phone/telephony pilot (separate readiness gate)

Prerequisites and exit gate are in `erp_webrtc_telephony_system_design.md` §16. Telephony is not a prerequisite for the first release and is not scheduled ahead of Lead Management unless Phase 0 shows it is a core buying reason.

## Phase 7 — Lead Management (marketing ERP)

Starts only after Campaign Management shows repeat usage and payment. Each sub-module needs buyer evidence, dependencies, provider/review constraints, security impact, cost, and rollback plan.

Order (hypothesis):
1. Landing pages + visitor-to-lead capture, content writing (reuses Contacts, events, consent)
2. Meta Ads console (OAuth, app review, ad-spend ledger namespace)
3. Google Ads console
4. Automated SEO and AEO
5. Lead pipeline, scoring, attribution, cross-module funnel reports

Exit gate per sub-module: named customer problem, activation path, entitlement and dependency rules, measurable success metric, support owner.

## Track D — Developer API (additional monetization, parallel)

**Goal:** let developers integrate messaging through PalGen on the same orchestration layer, ledger, and pay-as-you-go meter.

Start gate: Campaign Management has paying customers, the ledger reconciles with provider data, and abuse controls are proven on the campaign product.

Deliverables:
- Public, versioned REST API with documented idempotency and error model
- API keys with scopes, rotation, and per-key rate and spend limits
- Request and delivery logs, outbound signed webhooks with retries
- Sandbox using fake provider adapters; quickstarts; TypeScript SDK first
- Usage dashboard by key and source; developer rate card (if separate)
- Developer onboarding checks, new-account sending limits, and fraud/abuse monitoring
- Consent model for transactional versus marketing purposes

Exit gate:
- First external developers integrate without hands-on help
- Margin per usage unit is positive after support and abuse costs
- No cross-tenant exposure or key leakage in security tests

## Phase 8 — Scale and international

Introduce Kafka, Temporal, Redis, or separate services only when measured needs justify them (fan-out/replay; durable long-running workflows; caching/rate limiting; distinct scaling or ownership). Validate tax, privacy, messaging, telephony, and data residency per jurisdiction. Localize currency, time zones, templates, billing, and support. Re-check trademark and domains per market.

## Ongoing release gates

Every production release includes: automated tests and migration review; tenant-isolation and authorization checks; secrets and dependency scanning; observability and actionable alerts; backup/restore verification; rollback plan and owner; updated docs and decision records; cost and usage impact assessment; and a **lead-readiness check** (no campaign-only assumption added to shared models).
