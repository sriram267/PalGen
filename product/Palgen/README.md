# Palgen — The Ambient ERP Platform

> **"Traditional ERPs make you live inside software. Palgen brings the business to your fingertips only when decisions matter."**

Palgen is an event-driven, production-grade multi-tenant ERP platform. Rather than forcing managers and frontline operators to spend their days drilling through complex nested menus and dense form tables, Palgen is architected around **Pal Dynamic Island** — a cross-device ambient interface functioning as **Control Central + Live Activities** for fast, frictionless decisions and actions.

---

## 🌟 The Core Differentiator: Pal Dynamic Island

Palgen reimagines ERP interactions through Apple’s fluid Dynamic Island and Live Activities design language:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PALGEN DYNAMIC ISLAND                             │
├──────────────────────────────────────┬──────────────────────────────────────┤
│           CONTROL CENTRAL            │           LIVE ACTIVITIES            │
│       (Unified Command Hub)          │       (In-Flight Process Pulse)      │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • Omnipresent cross-module health    │ • Live timers & progress indicators  │
│ • Intelligent priority action queue  │ • Ongoing service / chair turnover   │
│ • Urgent business threshold alerts   │ • Native WebRTC softphone call HUD   │
│ • Aggregated multi-module approvals  │ • Dispatch & inventory transit pulse │
└──────────────────────────────────────┴──────────────────────────────────────┘
                                  │
                                  ▼
      ┌────────────────────────────────────────────────────────┐
      │           DECISIONAL ECONOMY & ACTION ENGINE           │
      │ • Sub-3-second operational turnarounds                │
      │ • 1-Tap / 2-Button binary decisions: [Approve/Decline] │
      │ • Background atomic mutation — zero context-switching  │
      └────────────────────────────────────────────────────────┘
```

### 1. Control Central (Aggregated Operational Command)
- **Single Focal Point**: Aggregates urgent alerts, pending managerial sign-offs, and health telemetry from across all Palgen modules (Sales, Inventory, Purchasing, Finance, CRM, Staffing).
- **At-a-Glance Telemetry**: A glance at the collapsed capsule conveys immediate operational status (`🟢 All Clear`, `🟠 2 Invoices Pending`, `🔴 High-Value Client Delayed`).
- **Multi-Surface Uniformity**: Embedded as a floating dynamic capsule on Web and iPad, a native Dynamic Island on iOS, and a notch/status menu companion on macOS.

### 2. Live Activities (Real-Time Workflows)
- **Active Process Tracking**: Monitors long-running, in-flight business events as they happen without needing to refresh pages.
- **First-Class Telephony HUD**: Instant caller ID, lifetime value, and call controls (`[Answer]`, `[Transfer]`, `[Mute]`) integrated directly into the island when incoming PSTN/SIP calls ring.
- **Operational Progress**: Visualizes service durations, table/chair turnarounds, and pending deliveries with live countdown rings.

### 3. Decisional Economy (Frictionless Actions)
- Turns 6-step form flows into **1-tap or 2-choice binary actions** (`[Approve / Reject]`, `[Auto-SMS / Hold]`, `[Reorder / Dismiss]`).
- Actions execute instantaneously through transactional background APIs, keeping operators fully present in their real-world environment.

---

## 🏛️ System Architecture

Palgen uses a **hybrid modular monolith** paired with event-driven background workers:

- **Frontend Application**: React 19, TypeScript, Vanilla CSS + Glassmorphism design tokens, Apple-standard spring physics (`damping: 0.82`, `response: 0.38s`).
- **Application Core**: Node.js & TypeScript modular monolith with domain isolation:
  - Identity & Multi-Tenancy
  - CRM & Customer Lifecycle
  - Inventory & Stock Thresholds
  - Orders & POS
  - Purchasing & Supplier Management
  - Payments & Billing
  - Native WebRTC Softphone & Telephony (Asterisk / FreeSWITCH + Indian SIP trunks)
  - Pal Control Central & Live Activity Event Engine
- **State & Data Store**: PostgreSQL (source of truth) + Redis (cache, softphone sessions, live presence).
- **Event Streaming & Workflows**: Kafka event bus + Temporal workflows for mission-critical business transactions and notifications.
- **Realtime Gateway**: WebSockets + Server-Sent Events (SSE) + Apple ActivityKit APNs Push.

---

## 🗺️ Product Roadmap & Specifications

Detailed blueprints and technical specifications:

1. **[pal_brainstorm.md](file:///Users/waffor/Desktop/Skills/product/roadmap/pal_brainstorm.md)** — Master product brainstorming, vertical analysis (Salon & Spa beachhead), mode-shifting architecture, and 4-phase rollout plan.
2. **[erp_production_system_design.md](file:///Users/waffor/Desktop/Skills/product/roadmap/erp_production_system_design.md)** — Production-grade multi-tenant backend architecture, database schemas, resilience, and scaling topologies.
3. **[erp_webrtc_telephony_system_design.md](file:///Users/waffor/Desktop/Skills/product/roadmap/erp_webrtc_telephony_system_design.md)** — WebRTC Softphone architecture, SIP trunking, call recording, and Indian telecom PSTN integration.
4. **[pal_apple_hig_ui_ux_analysis.md](file:///Users/waffor/Desktop/Skills/product/req/apple_os/pal_apple_hig_ui_ux_analysis.md)** — Apple HIG compliance, Dynamic Island morphology, spring physics, and multi-surface container states.

---

## 🚀 Execution Phases

| Phase | Milestone | Core Deliverables |
| :--- | :--- | :--- |
| **Phase 1** | **Pal Dynamic Island Foundation & Simulator** | ActivityKit iOS Widget, Web Dynamic Island component, Control Central & Live Activity JSON schemas, Salon & Spa interactive scenario simulator. |
| **Phase 2** | **Palgen Core Monolith & Realtime Bus** | Multi-tenant schema, Temporal workflows, Redis/Kafka event pipeline, atomic action mutation APIs. |
| **Phase 3** | **Integrated Telephony & Live Ops HUD** | WebRTC softphone, Asterisk PBX bridge, Inbound call Live Activity HUD, chair turnover timers. |
| **Phase 4** | **Production Hardening & Native Desktop** | macOS notch companion, offline resilience, enterprise RBAC, multi-branch switching from Control Central. |
