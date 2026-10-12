# PalGen Project Roadmap

**Product:** PalGen — a sales and marketing ERP built on its own channel orchestration layer (CPaaS-style capabilities over third-party providers)
**Ambient interface:** Pal
**Status:** Strategy and architecture baseline, October 2026

**Build order:** channel orchestration foundation → Campaign Management (now) → Lead Management (later, designed-for from day one). A Developer API is an additional-monetization track.
**Buyers:** marketers and business owners first; developers second. **Model:** pay-as-you-go.

## Read this first

1. [`product/product_strategy.md`](product/product_strategy.md) — canonical product definition, layers, channels, packaging, and the lead-readiness contract.
2. [`product/implementation_roadmap.md`](product/implementation_roadmap.md) — evidence-gated phases and deliverables.
3. [`product/architecture_decisions.md`](product/architecture_decisions.md) — decisions, proposals, hypotheses, and open questions.
4. [`product/ux_information_architecture.md`](product/ux_information_architecture.md) — navigation and shared surfaces that serve Campaign Management now and Lead Management later.
5. [`architecture/erp_production_system_design.md`](architecture/erp_production_system_design.md) — platform architecture (orchestration, ledger, contacts, connections, campaigns).
6. [`architecture/erp_webrtc_telephony_system_design.md`](architecture/erp_webrtc_telephony_system_design.md) — Phone channel architecture and launch gates.
7. [`product/pal_brainstorm.md`](product/pal_brainstorm.md) — Pal concept and event contract.
8. [`product/DOCUMENTATION_SYNC_CHECKLIST.md`](product/DOCUMENTATION_SYNC_CHECKLIST.md) — checks before merging doc changes.

Research references (not sources of truth): [`research/pal_apple_hig_ui_ux_analysis.md`](research/pal_apple_hig_ui_ux_analysis.md), [`research/agency_agents_analysis.md`](research/agency_agents_analysis.md).

## Source-of-truth rules

- Product strategy defines what and why; the roadmap defines sequencing; architecture documents define how; the UX document defines structure.
- If older prose conflicts with the canonical contract, follow the canonical contract and fix the conflicting document in the same change.
- "Target-state" does not mean "MVP scope." Only phase-gated work is committed.
- Lead Management is not built before Phase 7, but nothing may be built that would make it require rework.
- Do not describe the name as legally cleared until checked.
- Do not describe a buyer segment, channel provider, price, or launch date as decided unless it is recorded as decided in the register.
