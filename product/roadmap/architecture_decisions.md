# PalGen Architecture & Product Decision Register

**Status date:** 12 October 2026. This register separates decisions from proposals, hypotheses, and open questions.

Status values: **Decided** (founder decision), **Proposed** (CTO/COO/CSO recommendation awaiting confirmation), **Principle** (engineering rule), **Provisional** (working choice that may change).

## Decisions

| ID | Decision | Status | Rationale / constraint |
|---|---|---|---|
| D-001 | **PalGen** is the product name; **Pal** is the ambient interface | Decided; clearance pending | Trademark/domain/app-store checks are a launch task, not an engineering dependency. Use a configurable product label in code. |
| D-002 | PalGen is a **sales and marketing ERP** built on its own channel orchestration layer (CPaaS-style capabilities over third-party providers). Generic ERP domains (inventory, POS, purchasing, finance) are out of scope | Decided | Replaces earlier "generic/vertical ERP" language. |
| D-003 | **Build order:** channel orchestration foundation → Campaign Management → Lead Management | Decided | Campaign Management cannot exist without channels, consent, and a ledger. A Developer API track may run in parallel after Campaign Management shows paid usage. |
| D-004 | **Channels:** WhatsApp, SMS, Email, Phone (each with integration + recharge) and Instagram (integration, Interakt-style) | Decided | Instagram recharge only if Meta terms require it. |
| D-005 | **Lead Management** (Google Ads console, Meta Ads console, content/landing pages, automated SEO and AEO) comes later; architecture, data model, and UX are designed for it now | Decided | Enforced by the readiness contract in `product_strategy.md` §6. |
| D-006 | PalGen serves two buyers: marketers/business owners first (Campaign Management); developers integrating messaging through an API as additional monetization | Decided | One platform, one ledger. Developer API scope and timing are open (Q-3). |
| D-007 | Modules are individually purchasable with explicit dependencies | Decided | No forced full-suite bundle. |
| D-008 | Integration state is separate from recharge/usage/ledger state | Principle | Different domain concerns; different failure modes. |
| D-009 | Ad spend, communication charges, and PalGen revenue are separate ledgers/namespaces | Principle | Accuracy, reconciliation, trust. |
| D-010 | Modular monolith with separately deployed workers; PostgreSQL is the transactional source of truth | Principle | Extract only components with a demonstrated boundary. Events and caches are derived. |
| D-011 | PalGen builds an **orchestration layer** (unified API, adapters, routing and fallback, metering, billing, delivery tracking) over third-party providers; it does **not** build carrier infrastructure, peering, or a raw CPaaS | **Decided** | Raw CPaaS is a scale and peering business with thin margins and heavy fraud/regulatory load. The value sold is convenience and abstraction. |
| D-012 | **One Contact entity** for customers and future leads, plus an append-only event timeline | Proposed (required by D-005) | A lead is a contact at an earlier lifecycle stage. |
| D-013 | **Connections hub:** every external account uses one connection model (provider, scopes, secret reference, status, health) | Proposed (required by D-005) | Reused by Google and Meta Ads later. |
| D-014 | Ledger is **double-entry-style and immutable**; balances are projections; campaigns **reserve** credit before sending | Proposed | Prevents overspend and supports reconciliation and refunds. |
| D-015 | Telephony media/PBX infrastructure is isolated from the application plane | Principle | Different latency, networking, carrier, and failure modes. |
| D-016 | Pal is an optional event-driven interface; domain APIs stay authoritative | Principle | No parallel business logic in the ambient UI. |
| D-017 | Initial discovery geography is Chennai, then India | Provisional | International follows validation. |
| D-018 | Initial channel order: WhatsApp → Email → SMS → Instagram → Phone | Proposed (hypothesis) | Confirm in Phase 0 with demand, provider, and compliance evidence. |
| D-020 | **First buyer** is the marketer or business owner running campaigns; developers are a second buyer | Decided | Developer-experience moats (SDKs, components) apply to the second buyer, not the first. |
| D-021 | **Pay-as-you-go** commercial model | Decided | Whether any access fee is added, and the exact meaning of recharge per channel, are open (Q-5, Q-12). |
| D-022 | **API-first internal design:** the web app uses the same domain API a developer would; keys, scopes, idempotency, rate limits, outbound webhooks, and per-source usage attribution are designed in from Phase 1; public exposure waits for Track D | Proposed | Makes the Developer API an exposure step, not a rewrite. |
| D-019 | Lead Management order: landing page + lead capture → Meta Ads → Google Ads → content writing → SEO/AEO | Proposed (hypothesis) | Revisit after Campaign Management traction. |

## Hypotheses — not decisions

- A specific buyer segment (D2C/retail, clinics, education, real estate, local services, agencies) is the best first market.
- WhatsApp is the strongest first channel.
- Customers will pay both module access fees and channel consumption charges, at margins that cover support.
- Prepaid recharge is the right model for each channel.
- Pal materially improves productivity versus conventional screens.
- Telephony is worth building before Lead Management.
- Developers will adopt and pay for the API at usage rates that leave acceptable margin after support and abuse costs.

Each needs evidence and an owner before it drives major implementation.

## Open questions

1. Q-1 Which buyer segment and first workflow win Phase 0 discovery?
2. Q-2 What is the smallest paid product with a measurable outcome?
3. Q-3 Developer API: scope (transactional, notifications, campaigns), rate card, SDKs, onboarding and KYC, and when to start.
4. Q-4 Which providers per channel (WhatsApp BSP or Cloud API direct; SMS aggregator; email provider; SIP/voice provider)? What are their margins and terms?
5. Q-5 What exactly is "recharge" per channel: prepaid credits, pass-through invoicing, usage billing, or provider-direct billing? Can customers bring their own provider accounts?
6. Q-6 Payment gateway, GST/tax, invoicing, refunds, and disputes.
7. Q-7 Messaging compliance for India: SMS sender/template registration (DLT), WhatsApp business verification and template approval, consent and opt-out rules, email domain authentication.
8. Q-8 Telephony: carrier/numbering, KYC, recording consent, and regulatory constraints.
9. Q-9 Instagram messaging: API access, app review, messaging-window rules, and whether any charges apply.
10. Q-10 SLOs, retention, backups, and support commitments for the first paid release.
11. Q-11 Final trademark, domain, and taxonomy.
12. Q-12 Pay-as-you-go details: prepaid versus postpaid; any access fee on top; bring-your-own-provider versus resold credits; and the accounting, GST, and regulatory treatment of prepaid customer balances (verify with a CA/counsel).

## Architecture guardrails

- Do not build Kafka, Temporal, microservices, or an event mesh until a real workflow and operations plan justify them. Campaign sending can start on a PostgreSQL-backed job queue.
- A provider API integration is not commercial permission to resell or route traffic.
- Never trust client-side tenant IDs; derive tenant and permissions from authenticated server context.
- Meter usage idempotently and reconcile it with provider records.
- Every async job defines retries, idempotency, poison handling, and tenant context.
- Every external call defines timeout, retry, rate limit, audit, and failure UX.
- Never add a campaign-only assumption to the core data model (see readiness contract).
- AI output is a suggestion unless the user approves an allowed automation policy.

## Change protocol

1. Update this register and state why.
2. Update `product_strategy.md` if scope or packaging changes.
3. Update `implementation_roadmap.md` if sequencing or gates change.
4. Update `ux_information_architecture.md` and architecture documents affected.
5. Search the repository for stale terms, names, and phase numbers.
