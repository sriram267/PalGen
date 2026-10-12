# Coucou (formerly NotchBuddy) — End-to-End Architectural & Product Analysis

> **Target Repository:** [Louis-CFM/coucou](https://github.com/Louis-CFM/coucou)  
> **Analysis Date:** October 2026  
> **Orchestrated By:** `master-skiller` Architectural Framework (`architecture` + `github` analysis pipeline)

---

## 1. Executive Summary & Product Thesis

**Coucou** is an open-source, multi-platform desktop companion and mobile relay system designed to provide real-time visibility, interactive approvals, and telemetry for autonomous AI coding agents (Claude Code, Cursor, OpenAI Codex, Gemini CLI, Google Antigravity, and custom CLI agents).

### The Core Problem
When developers run autonomous coding agents in the terminal or background IDEs:
1. **Context Switching:** Developers constantly tab back and forth to check whether an agent is thinking, editing files, running bash commands, or hanging on a permission prompt.
2. **Permission Friction:** Agents block waiting for human confirmation (`Allow / Deny`). If the developer steps away, the agent sits idle.
3. **Proprietary Moats:** Several commercial studios teased desktop notch companions without open-sourcing their architectures.

### Coucou's Solution
Coucou places an interactive character named **Mochi** inside the MacBook notch (or top-screen status island on Windows, Linux, and non-notch Macs):
- **Live Agent Feed:** Displays real-time diff stats (`+N -M`), active commands, and subagent trees.
- **In-Notch Approvals:** Inline decision cards for `Allow / Deny / Always Allow` and multi-question prompts (`AskUserQuestion`).
- **Seamless Mobile Continuity:** When the developer steps away or locks their Mac, Mochi moves to the iPhone via **iOS 18 Live Activities**, **Dynamic Island**, and **Lock Screen Widgets**. Approvals can be granted directly from the Lock Screen authenticated via **Face ID**.

---

## 2. System Architecture & High-Level Topology

```
┌────────────────────────────────────────────────────────────────────────┐
│                             DESKTOP LAYER                              │
│                                                                        │
│   ┌─────────────────────┐             ┌────────────────────────────┐   │
│   │   AI Coding Agent   │             │   Coucou Host Application  │   │
│   │ (Claude / Cursor /  │             │  (macOS Swift 6 / SwiftUI) │   │
│   │  Codex / Antigravity│             │  (Windows/Linux Tauri+Rust)│   │
│   └──────────┬──────────┘             └─────────────▲──────────────┘   │
│              │                                      │                  │
│              ▼ Hook Event                           │ Local IPC        │
│   ┌─────────────────────┐      nb.sock / Pipe       │ (Zero latency)   │
│   │ nb-hook (CLI Relay) ├───────────────────────────┘                  │
│   └─────────────────────┘                                              │
└─────────────────────────────────────┬──────────────────────────────────┘
                                      │
                                      ▼ Encrypted CloudKit Sync
┌────────────────────────────────────────────────────────────────────────┐
│                              MOBILE LAYER                              │
│                                                                        │
│   ┌────────────────────────┐                  ┌────────────────────┐   │
│   │  Cloudflare Worker     │                  │  iPhone Companion  │   │
│   │  (Stateless APNs push) │──APNs Push Alert─▶ (iOS 18 Swift 6)   │   │
│   │  relay/src/index.ts    │                  │  • Live Activity   │   │
│   └────────────────────────┘                  │  • Dynamic Island  │   │
│                                               │  • Face ID Guard   │   │
│                                               └────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Platform Breakdown & Codebase Organization

### 3.1 macOS Native App (`NotchBuddy/Sources/App` & `CoucouKit`)
- **Technology Stack:** Swift 6, SwiftUI, AppKit (`NSPanel`).
- **Window Architecture:**
  - Borderless `NSPanel` (`styleMask: [.borderless, .nonactivatingPanel]`).
  - Positioned above fullscreen applications (`.mainMenu + 3`).
  - Non-blocking mouse pass-through: polling `NSEvent.mouseLocation` at 60 Hz; transparent zones set `ignoresMouseEvents = true` so desktop clicks pass directly to background apps.
- **Notch Detection & Fallback:**
  - Reads `NSScreen.safeAreaInsets.top`, `auxiliaryTopLeftArea`, and `auxiliaryTopRightArea`.
  - Non-notch displays (iMac, Mac mini, external monitors): Automatically adapts to a 80 pt compact top bar (capped at menu bar height).
- **Desktop Mochi Mode (`DesktopMochi.swift`):**
  - Mochi can be dragged out of the notch to become a floating 120 pt companion widget with physics-based eye tracking and alert animations.

### 3.2 Windows & Linux Desktop (`windows/`)
- **Technology Stack:** Tauri v2 (Rust backend) + Vite / TypeScript / HTML5 Canvas frontend.
- **Inter-Process Communication:**
  - **Windows:** Named Pipe (`\\.\pipe\coucou-<user-SID>`).
  - **Linux:** Unix Domain Socket (`$XDG_RUNTIME_DIR/coucou.sock`, user-restricted 0600 permissions).
- **Credential Storage:** Windows Credential Manager (`wincred`) / Linux Secret Service (`libsecret` / GNOME Keyring / KWallet).

### 3.3 iOS Companion & Extensions (`NotchBuddy/Sources/Phone`, `Widgets`)
- **Technology Stack:** iOS 18+, SwiftUI, ActivityKit, WidgetKit, AppIntents, LocalAuthentication.
- **Features:**
  - **Live Activity & Dynamic Island:** Displays agent state in real-time when the Mac is locked.
  - **Face ID Guarded Approvals:** Any `Allow` action triggered from iPhone executes biometric authentication before sending the signed decision back to the Mac.
  - **Siri & Shortcuts:** Voice commands to inspect agent status or submit instructions remotely.

### 3.4 Push Relay Microservice (`relay/`)
- **Technology Stack:** Cloudflare Workers, TypeScript.
- **Purpose:** Securely manages the Apple Push Notification Service (APNs) AuthKey (`.p8`) for live activity background push updates.
- **Privacy Design:** Completely stateless, zero logging, stores zero tokens. Only receives minimal state metadata (`state`, `color`, `stepIndex`, `pillId`).

---

## 4. Hook Protocol & Agent Integration Specification

Coucou interfaces with AI coding agents via a universal hook mechanism (`nb-hook`).

### 4.1 Supported Lifecycle Events

| Hook Event Name | Mochi State | Visual / Interaction Behavior |
|---|---|---|
| `SessionStart` | `idle` | Initializes session pill in notch; tracks repository directory. |
| `UserPromptSubmit` | `thinking` | Displays user prompt snippet in the rolling ticker. |
| `PreToolUse` | `working` | Displays tool icon + target (e.g. `Edit Invoice.swift`, `Bash npm test`). Shows diff summary `+N -M`. |
| `PostToolUse` | `working` | Updates ticker progress; records step execution. |
| `PermissionRequest` | `approval` | **Opens alert card.** Prompts user with `Allow (Y)`, `Deny (N)`, or `Always Allow`. Blocks until answered. |
| `AskUserQuestion` | `question` | **Opens question card.** Renders 1–4 questions with single/multi-select chip buttons or freeform text. |
| `Notification` | `ratelimit` / `question` | Warns of quota exhaustion or required user action. |
| `Stop` | `finished` | Mochi celebrates (5.2s duration); displays AI summary of completed task. |
| `SessionEnd` | Dismissed | Cleans up session pill and returns notch to hidden state. |

### 4.2 Safe Failover Mechanism
- `nb-hook` enforces a strict **300ms timeout**: if the Coucou app is not running or fails to answer immediately, the hook script exits with code `0`.
- The CLI agent continues in the terminal without blocking or crashing.

---

## 5. Security & Privacy Architecture

| Vector | Coucou Implementation |
|---|---|
| **API Keys** | Stored locally in OS Keychains (macOS Keychain, Windows Credential Manager, Secret Service). Never synced to cloud. |
| **Telemetry** | **Zero analytics, zero tracking.** No third-party analytics SDKs. |
| **Sync Protocol** | Relies entirely on the developer's personal **private iCloud CloudKit database**. End-to-end encrypted with user's Apple Account keys. |
| **Remote Approvals** | Remote `Allow` actions on iPhone require **Face ID / Touch ID** verification; decision payloads enforce a 2-minute expiration window and match exact session IDs. |

---

## 6. Directory & Codebase Map

```
coucou/
├── NotchBuddy/                    # macOS & iOS Native Codebase (Xcode / Swift 6)
│   ├── Sources/
│   │   ├── App/                   # macOS Menu Bar & Notch Island App
│   │   │   ├── IslandStateMachine.swift  # Island FSM (hidden/peek/compact/expanded)
│   │   │   ├── HookServer.swift          # Unix domain socket server
│   │   │   ├── BotCanvasView.swift       # Mochi procedural rendering & physics
│   │   │   ├── DesktopMochi.swift        # Floating desktop companion
│   │   │   └── ClaudeService.swift       # Direct API chat integration
│   │   ├── Phone/                 # iOS Companion App (Session list, remote approvals)
│   │   ├── CoucouKit/             # Shared Foundation types (DiffEngine, Models)
│   │   └── Widgets/               # iOS Live Activities & Dynamic Island widgets
│   └── Resources/                 # Sound effects (.wav), app icons, entitlements
│
├── windows/                       # Cross-Platform Desktop App (Windows & Linux)
│   ├── src-tauri/                 # Rust core (Named pipes, sockets, secrets)
│   └── src/                       # TypeScript/Canvas UI (Island FSM, Mochi engine)
│
├── relay/                         # Cloudflare Workers APNs push relay
│   └── src/index.ts               # Stateless APNs JWT signing & token dispatch
│
├── docs/                          # Technical documentation
│   ├── SPEC.md                    # Exact pixel dimensions, timings, bezier curves
│   ├── AGENTS.md                  # Custom agent hook setup guide
│   ├── IPHONE.md                  # iOS pairing, CloudKit & Live Activities guide
│   └── INTEGRATIONS.md            # Third-party service API contracts
│
└── tests/                         # Swift test suite (Diff engine, geometry, parsing)
```

---

## 7. SWOT & Engineering Assessment

### Strengths
1. **Exceptional Craft & Polish:** Pixel-level fidelity with Apple-grade fluid animations (`.spring(response: 0.5, dampingFraction: 0.72)`), custom SFX, and zero-flicker transitions.
2. **True Native Performance:** Swift 6 on macOS/iOS and Rust/Tauri on Windows/Linux ensure sub-1% CPU usage when idle.
3. **Privacy-First Zero-Knowledge Sync:** Uses private iCloud CloudKit rather than spinning up a custom backend database.
4. **Resilient IPC:** Non-blocking 300ms socket timeout prevents agent deadlocks if Coucou crashes or closes.

### Considerations & Technical Constraints
1. **Sandboxing Limitations:** App Store sandboxed builds cannot read external process trees (`ps`) or inspect active window contexts without Accessibility permissions.
2. **Relay Dependency for iOS:** Live Activities push updates require Cloudflare Worker relay to sign APNs tokens (inherent iOS architecture constraint).
3. **Multi-Agent Scale:** Notch width is physically bounded (~640 pt in expanded mode); managing more than 4 concurrent agent sessions simultaneously shifts secondary agents into vertical pill lists.

---

## 8. Summary & Takeaways

Coucou represents a reference implementation for **Ambient AI Developer Experience (DevEx)**. Instead of burying AI coding progress inside hidden terminal tabs, it surfaces agent actions at the physical periphery of the user's workspace, creating a seamless, delightful, and non-intrusive supervision workflow.
