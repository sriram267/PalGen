# PalGen Product Strategy — Canonical Source of Truth

**Version:** 2.0
**Date:** 12 October 2026
**Brand status:** PalGen is the chosen product name; trademark/domain/app-store checks remain a separate launch task.
**Scope status:** Product vision and build order are **decided by the founder** (Section 1–3). Buyer segment, first channel, providers, and pricing are **not yet validated** (Section 8).

## 1. Vision

PalGen is a **sales and marketing ERP** built on its own **channel orchestration layer**: CPaaS-style capabilities (one API over many channels, routing, templates, delivery tracking, usage metering) running on top of third-party providers. PalGen does **not** build carrier infrastructure or a raw CPaaS.

A business uses PalGen to reach customers on every channel it cares about, run campaigns across those channels from one place, and — later — capture, track, and convert leads from advertising, content, and search.

PalGen serves **two buyers on one platform and one meter**:

1. **First buyer — marketers and business owners** who run campaigns. This is the product the first releases are built for.
2. **Second buyer — developers** who integrate messaging into their own products through a PalGen API. This is **additional monetization** on the same orchestration layer and the same ledger, and starts only after Campaign Management is proven.

The commercial model is **pay-as-you-go**: customers pay for what they use. The orchestration layer is built first because Campaign Management cannot exist without it.

## 2. Product map

```
PALGEN — SALES & MARKETING ERP
│
├── Platform foundation (shared)
│     tenants · identity · roles · entitlements · contacts · consent ·
│     billing ledger · connections hub · audit · notifications · Pal events
│
├── Channel orchestration layer  (built first; CPaaS-style, over third-party providers)
│     Channels — each has TWO parts: Integration + Recharge
│     ├── WhatsApp   integration │ recharge
│     ├── SMS        integration │ recharge
│     ├── Email      integration │ recharge
│     ├── Phone      integration │ recharge
│     └── Instagram  integration (messaging inbox, Interakt-style)
│
├── Campaign Management  (first SaaS module — NOW)
│     audiences · templates · multi-channel campaigns · scheduling ·
│     throttling · conversations/inbox · delivery and campaign reports
│
├── Lead Management  (marketing ERP — LATER, designed-for now)
│     ├── Google Ads console
│     ├── Meta Ads console
│     ├── Content writing + landing-page visitor conversion
│     └── Automated SEO + AEO (answer-engine optimization)
│
├── Developer API  (additional monetization — LATER, designed-for now)
│     public API · API keys · logs · outbound webhooks · sandbox · SDKs
│
└── Pal  (ambient interface across all of the above)
```

**Interpretation to confirm:** "Instagram like in Interakt" is read here as Instagram Direct messaging connected to PalGen (inbox + campaign-adjacent replies and automation), not as an ads product. Instagram has no per-message charge comparable to SMS, so it has an integration but, unless Meta terms say otherwise, no recharge.

## 3. Build order (decided)

1. **Channel orchestration foundation** — channel adapters, canonical message model, routing and fallback rules, delivery tracking, consent, and the usage ledger.
2. **Campaign Management** — the first sold module, running on the orchestration layer.
3. **Lead Management** — later. **Nothing in Lead Management is built yet**, but the data model, architecture, and UX must not need rework when it arrives (Section 6).

A parallel **Developer API track** can start once Campaign Management shows paid usage (see roadmap, Track D). It is exposure of the same platform, not a second platform.

Within each phase, work is gated by evidence (see `implementation_roadmap.md`), not by calendar.

## 4. Layers and boundaries

### Layer A — Shared platform
- Organizations/tenants, memberships, authentication, roles, permissions, audit
- Module entitlements and dependency rules
- **Contacts** (the single customer/lead record — see Section 6), consent and preferences
- Subscription plans, invoicing, payment gateway, **ledger**
- **Connections hub:** every external account (WhatsApp, SMS provider, email domain, Instagram, later Google/Meta Ads) is a *connection* with one lifecycle and one health model
- Webhooks/events, notifications, support tooling, observability

### Layer B — Channel orchestration (CPaaS-style capabilities)
Every channel has two independent concerns:

| Concern | Meaning | Examples |
|---|---|---|
| **Integration** | Connect and configure a provider; send/receive; templates; sender identity; delivery state | WABA onboarding, DLT-registered sender, verified email domain, Instagram account link, SIP/phone number |
| **Recharge / consumption** | Meter usage, price it, sell prepaid credit, reconcile to provider bills | Credits purchased, per-message debit, refunds, provider invoice match |

Rules:
- Integration state (connected, needs authorization, suspended) never changes the ledger; ledger state (out of credits) never changes connection state. The UI shows both.
- A balance is a **projection of immutable ledger entries**. No mutable wallet field is authoritative.
- Channels differ in pricing, windows, templates, compliance, and delivery semantics. The canonical model abstracts the common parts and exposes channel-specific capabilities explicitly.
- PalGen builds the **orchestration layer** (unified API, adapters, routing and fallback, metering, billing, delivery tracking). It does **not** build carrier infrastructure, peering, or a raw CPaaS; upstream providers carry the traffic (Decision D-011, decided). The value sold is convenience, clean abstractions, compliance handled, and saved effort — not bandwidth.
- Orchestration capabilities that belong here: channel fallback rules (e.g. WhatsApp, then SMS or email if undelivered after a wait), frequency caps, per-contact channel preferences, template management across channels, and one delivery log.

### Layer C — Campaign Management (SaaS module 1)
- Audiences and segments over Contacts
- Message templates (channel-specific approval status tracked)
- Campaigns: one or many channels, schedule, throttling, budget cap (credit reservation), A/B variants where useful
- Conversations/inbox for replies (WhatsApp, Instagram, SMS where supported, email replies)
- Reports: sent, delivered, read, failed, replied, opted-out, cost
- Orchestration rules: fallback between channels, frequency caps, quiet hours, per-contact preferences
- Honest status model: *not connected · needs authorization · template pending · out of credits · paused · failed · running*

Campaign orchestration calls the channel adapters; it never hard-codes a provider and never assumes every tenant has bought every channel.

### Layer D — Lead Management (SaaS module 2, later)
Sections to be built later, in the order the evidence supports:
- Landing pages + visitor-to-lead conversion, content writing
- Meta Ads console, Google Ads console
- Automated SEO and AEO
- Lead pipeline, scoring, attribution, reporting

Ad spend is paid to Google/Meta and is **never** mixed with PalGen revenue or communication credits (separate ledger namespace).

### Layer D2 — Developer API (additional monetization, later)
A documented, versioned API over the same orchestration layer, for developers who want to send messages from their own products (including transactional and notification use cases), plus API keys, request/delivery logs, outbound webhooks, a sandbox, and SDKs.

- Same ledger and same pay-as-you-go meter as the campaign product; usage is attributed to a source (campaign, inbox, API key).
- Needs its own abuse, fraud, and spend controls (Section 6, Section 11 non-goals).
- Not exposed publicly until its roadmap gate is met; internal design is API-first from Phase 1.

### Layer E — Pal ambient interface
Pal surfaces events and safe actions from modules the user may access: low credits, template rejected, campaign failing, reply waiting, number suspended — and later lead and ad events. The product is fully usable without Pal. Principles: calm by default; every card says what happened / why it matters / what the safe action is; server-side authorization, confirmation, idempotency, audit on every action; suggestions are dismissible and explainable.

## 5. Packaging and monetization

1. Modules are individually purchasable; dependencies are visible before purchase (e.g. Campaign Management requires at least one connected channel).
2. The commercial model is **pay-as-you-go**: customers pay for what they use (messages, minutes, API calls). Whether any module also carries an access fee is open; either way, keep usage and access dimensions separate in code and on invoices.
3. Communication charges are itemized by channel, unit, and provider, and reconciled to upstream provider data.
4. Google/Meta ad spend is separate from PalGen revenue and communication charges.
5. Margins differ by component. Pass-through provider fees (Meta, SMS, carrier) carry thin margins; the orchestration value must be priced above them. Track gross margin per channel and per unit from the first paid customer.
6. Developer API usage runs on the same meter and ledger; whether it has its own rate card is open.
7. Do not publish prices until provider costs, taxes, payment fees, support burden, and willingness to pay are measured.
8. Free trial/sandbox only with clear abuse, cost, and compliance controls.

## 6. Lead-Management readiness contract

Lead Management is not built now. The following are mandatory **now**, so it can be added without migration pain:

| Area | Requirement today | Why it prepares for leads |
|---|---|---|
| **Data model** | One `contacts` entity with lifecycle stage, source, owner, tags, custom fields; no separate "customer" and "lead" tables | A lead is a contact at an earlier lifecycle stage |
| **Event timeline** | Append-only `contact_events` (message sent/delivered/replied, opt-in/out, import, later: page view, form fill, ad click) | Attribution and scoring read the same timeline |
| **Attribution fields** | Contacts and conversations carry `source`, `medium`, `campaign_id`, `first_touch`, `last_touch` (nullable) | Campaigns already produce attribution data |
| **Identity and consent** | Consent and preferences are per contact per channel/purpose, with timestamp and evidence | Landing pages and ads collect consent too |
| **Connections hub** | Generic connection model: provider, scopes, secrets reference, status, health | Google/Meta Ads connections reuse OAuth, token refresh, review state |
| **Entitlements** | Module registry with dependency declarations; Lead Management registered as a known-but-unavailable module | Navigation and billing need no redesign |
| **Ledger namespaces** | Ledger supports `communication_credit`, `subscription`, and reserved `ad_spend_reference` accounts | Ad spend stays separate |
| **Reporting** | Reports read from events and facts, not from per-module tables | Cross-module funnel reports are possible later |
| **Pal events** | Event schema is module-agnostic (`module`, `entity`, `severity`, `actions`) | Lead and ad events plug in |
| **API surface** | The web app uses the same domain API a developer would; API keys, scopes, idempotency keys, per-key rate limits, outbound webhooks, and per-source usage attribution are designed in | The Developer API is exposure of what exists, not a rewrite |
| **UX** | Information architecture reserves the Leads and Ads areas (see `ux_information_architecture.md`) | No navigation redesign |

Anything that would force a campaign-only assumption into the schema (e.g. an `audience` table that cannot hold a lead stage) fails this contract.

## 7. Customer and market strategy

- **Discovery geography:** Chennai first, then India; international later.
- **First buyer (decided):** the marketer or business owner running campaigns — owner/operator or marketing/sales lead at a small or mid-sized business. Which segment inside that group comes first is still to be validated.
- **Second buyer (decided, later):** developers integrating messaging through the API.
- **Segment hypotheses** (none selected): D2C and retail, clinics and wellness, education and coaching, real estate, local services, agencies running campaigns for clients.
- **Alternatives buyers use today:** WhatsApp marketing tools (Interakt, Wati and similar), SMS gateways, email platforms, CRMs with campaign add-ons, agencies, manual WhatsApp broadcast. Understand switching cost and why they would move.
- **Developer comparables:** Twilio and Sinch (raw CPaaS), Resend, Novu, and Courier (orchestration). Their moat is developer experience; that applies to the second buyer, not the first.
- **Differentiation hypothesis:** one place to connect every channel, hold one prepaid balance model, run multi-channel campaigns, and later grow into leads and ads — with the shared contact record as the spine.

Do not claim a moat or market gap from desk research alone.

## 8. Decided vs open

**Decided by founder:** modular sales and marketing ERP; the channel list and the integration/recharge split; Instagram as an Interakt-style integration; Campaign Management first, Lead Management later; design for Lead Management from day one; PalGen builds an orchestration layer over third-party providers, not a raw CPaaS (D-011); first buyer is the marketer/business owner and developers are a second buyer through an API as additional monetization; the model is pay-as-you-go.

**Proposed by CTO/COO/CSO, needs confirmation:**
- Initial channel order (hypothesis): WhatsApp → Email → SMS → Instagram → Phone, subject to Phase 0 evidence.
- Lead Management order (hypothesis): landing page + lead capture → Meta Ads → Google Ads → content writing → SEO/AEO.
- API-first internal design from Phase 1 (D-022).

**Open (need evidence or counsel):** which segment of marketers/owners comes first; first paid workflow; providers per channel; **bring-your-own-provider versus PalGen-resold credits**, and the accounting, GST, and regulatory treatment of prepaid balances; whether any access fee sits on top of pay-as-you-go; the Developer API rate card, scope, and start date; India messaging and telephony compliance; payment, tax, and invoicing rules; final trademark clearance.

## 9. MVP definition

An MVP is a narrow workflow, not a screen collection. The first release is **Campaign Management on one or two channels** that:
- Serves one buyer segment
- Works end-to-end with a real provider connection and real recharge
- Has tenant-safe permissions, failure handling, observability, and a support path
- Produces a measurable outcome (e.g. campaign delivered, replies handled, cost per reply)
- Has at least some customers who will pay or commit to a paid pilot

## 10. Success measures

Pilot activation and time to first campaign sent; weekly active senders; delivery and failure rates; reply handling time; credits purchased and consumed; ledger-to-provider reconciliation accuracy; paid conversion and retention; support hours per account; gross margin per channel; tenant-isolation test results and incidents. Module count and feature count are not success measures.

## 11. Non-goals for the first release

- Lead Management features and a public Developer API (only readiness work from Section 6)
- Becoming a telecom carrier, building a raw CPaaS, or bypassing provider/regulatory requirements
- All channels live at once
- Generic ERP domains (inventory, purchasing, POS, finance) — out of scope; the ERP here is a sales and marketing ERP
- Microservice-per-module; mandatory Kafka/Temporal before a workflow needs them
- Unsupervised AI taking high-impact external actions
- Claims of full attribution or SEO/AEO outcomes without platform access and evidence
