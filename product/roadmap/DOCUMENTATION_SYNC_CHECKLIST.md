# Documentation Synchronization Checklist

Before merging any roadmap, UX, or architecture change:

- [ ] Product identity is **PalGen** (product) and **Pal** (ambient interface); naming clearance is still a launch task.
- [ ] PalGen is described as a **sales and marketing ERP on its own channel orchestration layer** (no carrier infrastructure, no raw CPaaS); no generic-ERP domains (inventory, POS, purchasing) are described as scope.
- [ ] Build order is intact: **channel orchestration → Campaign Management → Lead Management**, with the Developer API as a later parallel track.
- [ ] Channel list is intact: WhatsApp, SMS, Email, Phone (each integration + recharge) and Instagram (integration).
- [ ] Two buyers are respected: marketers/business owners first; developers through the API as additional monetization, not first-release scope.
- [ ] Pricing is pay-as-you-go; usage and any access fee stay separate; gross margin is tracked per channel and per unit.
- [ ] Internal design is API-first; no important capability exists only behind a private endpoint.
- [ ] Lead Management (Google Ads console, Meta Ads console, content/landing pages, SEO, AEO) is shown as **later**, never as MVP scope.
- [ ] **Lead-readiness contract** (`product_strategy.md` §6) still holds: one Contact entity, event timeline, attribution fields, connections hub, module registry, ledger namespaces, module-agnostic Pal events, reserved UX areas.
- [ ] No schema, screen, or report assumes campaigns are the only source of contacts or events.
- [ ] Provider connection/integration is separate from usage/recharge/ledger accounting.
- [ ] Ad spend, communication costs, and PalGen revenue remain separate.
- [ ] Modules are independently purchasable and dependencies are explicit.
- [ ] Target-state architecture is not presented as MVP scope.
- [ ] Kafka/Temporal/service extraction is justified by a real workflow or operational need.
- [ ] Telephony is provider-backed with India-specific launch and compliance gates; PalGen is not a carrier.
- [ ] Messaging compliance (DLT/sender registration, WhatsApp template approval, consent, opt-out, email authentication) is addressed for each channel.
- [ ] Pal actions enforce server-side authorization, confirmation, idempotency, and audit.
- [ ] Buyer segment, first channel, providers, and prices are not described as validated unless recorded in the decision register.
- [ ] Search for stale terms: `Palgen`, "generic ERP", "salon", "warehouse", "Final Locked Stack", old phase numbers.
- [ ] Update the decision register, strategy, roadmap, UX architecture, and affected architecture docs together; refresh `FILE_INDEX.md`.
