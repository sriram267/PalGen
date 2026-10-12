# The Agency (`agency-agents`) — End-to-End Architectural & Multi-Agent Framework Analysis

> **Target Repository:** [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)  
> **Repository Scale:** 282+ Production AI Agent Personas, 18 Divisions, Full Orchestration Suite  
> **Ecosystem Companion:** [agencyagents.app](https://agencyagents.app) (Desktop App for macOS, Windows, Linux)  
> **License:** MIT License  
> **Analysis Date:** October 2026  
> **Orchestrated By:** `master-skiller` Architectural Framework (`prompt-engineering-patterns` + `tdd-workflows-tdd-cycle` pipeline)

---

## 1. Executive Summary & Product Vision

**The Agency (`agency-agents`)** is an open-source, multi-tool AI specialist framework providing a curated roster of **282 battle-tested AI agent personas** organized across **18 operational divisions**.

### The Core Problem
General-purpose LLMs acting under generic prompts ("You are an expert developer") suffer from:
1. **Context Drift & Hallucination:** Lack of domain-specific constraints, deliverables, and operational boundaries.
2. **Missing Multi-Agent Handoffs:** Inability to coordinate specialized roles (e.g., UX Architect ➔ Frontend Developer ➔ Evidence Collector ➔ Reality Checker) across structured project phases.
3. **Tool Fragmentation:** Developers use multiple AI coding environments (Claude Code, Antigravity, Cursor, Gemini CLI, Copilot, Codex, Windsurf, Aider). Personas written for one tool do not natively translate to others.

### The Agency's Solution
- **Meticulously Crafted Personas:** Each agent possesses an explicit identity, memory model, non-negotiable rules, concrete technical deliverables, and measurable success criteria.
- **Transpiler & Multi-Tool Matrix:** A built-in compiler (`scripts/convert.sh`) transforms persona definitions into native configurations for **14+ AI agent environments**.
- **The NEXUS Strategy Doctrine:** A comprehensive multi-agent orchestration framework with standardized runbooks (`startup-mvp`, `enterprise-feature`, `marketing-campaign`, `incident-response`) and phase-based handoff protocols.
- **Native Desktop App & One-Click Distribution:** A desktop app (`agencyagents.app`) and Homebrew cask for zero-terminal discovery and installation.

---

## 2. The 18 Operational Divisions (282 Agents Total)

The repository's canonical catalog is defined in `divisions.json` and validated by strict CI checks (`scripts/check-divisions.sh`):

| Division | Agent Count | Primary Focus & Flagship Roles | Brand Color | Icon |
|---|---|---|---|---|
| **`engineering`** | **65** | Frontend Developer, Backend Architect, Mobile App Builder, SRE, DevOps, Rust Specialist, WASM, WeChat Mini Program, China Network Engineer, Embedded Firmware. | `#3B82F6` | `Code` |
| **`specialized`** | **59** | Agents Orchestrator, Whimsy Injector, Reality Checker, Prompt Engineer, Minimal Change Engineer, ATS Validator, Knowledge Graph Engineer. | `#6366F1` | `Sparkles` |
| **`marketing`** | **37** | Growth Hacker, Content Creator, Reddit Community Ninja, Social Media Strategist, Technical Copywriter, SEO/AEO Specialist. | `#F97316` | `Megaphone` |
| **`game-development`**| **21** | Unity Architect, Godot Gameplay Scripter, Roblox Experience Designer, Blender Addon Engineer, Shader Graph Artist. | `#A855F7` | `Gamepad2` |
| **`gis`** | **13** | GeoAI ML Engineer, Spatial Data Scientist, Drone Reality Mapping, BIM Specialist, Cartography Designer. | `#14B8A6` | `Map` |
| **`security`** | **12** | Application Security Specialist, Threat Modeler, Incident Response Commander, Cloud Security Architect, Privacy Engineer. | `#EF4444` | `ShieldCheck` |
| **`design`** | **10** | UX Architect, UI Designer, Brand Guardian, Design System Engineer, Motion Designer. | `#EC4899` | `PenTool` |
| **`testing`** | **9** | Evidence Collector, Reality Checker, Performance Benchmarker, Chaos Engineer, E2E Automation Lead. | `#F59E0B` | `FlaskConical` |
| **`sales`** | **9** | Enterprise Account Executive, SDR Lead, Technical Sales Engineer, Deal Closer. | `#10B981` | `TrendingUp` |
| **`project-management`**| **7** | Senior Project Manager, Agile Coach, Delivery Lead, Technical Program Manager. | `#0EA5E9` | `ClipboardList` |
| **`paid-media`** | **7** | Meta Ads Buyer, Google Search Lead, TikTok Performance Marketer, Attribution Specialist. | `#EAB308` | `Target` |
| **`academic`** | **6** | Literature Reviewer, Peer Reviewer, Grant Proposal Writer, Statistical Validator. | `#8B5CF6` | `GraduationCap` |
| **`product`** | **6** | Product Sprint Prioritizer, Technical Product Manager, User Research Synthesizer. | `#D946EF` | `Box` |
| **`spatial-computing`** | **6** | VisionOS Spatial Engineer, AR/VR Experience Designer, 3D Interaction Specialist. | `#06B6D4` | `Boxes` |
| **`support`** | **6** | IT Service Manager, Infrastructure Maintainer, Customer Solutions Engineer. | `#84CC16` | `LifeBuoy` |
| **`finance`** | **5** | Financial Modeling Specialist, Payments & Billing Engineer, FinOps Cloud Optimizer. | `#22C55E` | `DollarSign` |
| **`healthcare`** | **3** | Clinical Data Compliance Specialist, HealthTech Systems Engineer, HIPAA Validator. | `#0D9488` | `Stethoscope` |
| **`research`** | **1** | Deep Market & Technical Synthesizer. | `#7C3AED` | `Search` |

---

## 3. Agent Persona Anatomy & Prompt Engineering Standard

Every agent file in the repository follows a deterministic markdown template with YAML frontmatter:

```markdown
---
name: Frontend Developer
description: Expert frontend developer specializing in modern web technologies, UI implementation, and performance optimization
color: cyan
emoji: 🖥️
vibe: Builds responsive, accessible web apps with pixel-perfect precision.
---

# [Agent Name] Personality

## 🧠 Your Identity & Memory
- Explicit definition of background, memory anchors, and past experiences.
- Reinforces what the agent prioritizes and what failure states it avoids.

## 🎯 Your Core Mission
- Actionable domains broken down into 4-6 operational areas with exact deliverables.

## 🚨 Critical Rules You Must Follow
- Negative constraints and non-negotiable boundaries (e.g., WCAG 2.1 AA compliance, sub-150ms interaction latency, zero unverified assumptions).

## 🛠️ Technical Deliverables & Code Artifacts
- Concrete code patterns, architectural styles, and structured outputs expected from this specialist.

## 📈 Success Metrics & Communication Style
- Precise voice attributes (e.g., concise, highly technical, uncompromising on quality) and quantitative KPIs.
```

---

## 4. Multi-Agent Orchestration: The NEXUS Strategy

Located in `strategy/nexus-strategy.md` and machine-readable in `strategy/runbooks.json`, the **NEXUS Strategy** provides procedural governance for multi-agent teams.

### 4.1 The 7-Phase Product Lifecycle
```
[Phase 0: Discovery] ──▶ [Phase 1: Strategy] ──▶ [Phase 2: Foundation]
                                                        │
[Phase 5: Launch]    ◀── [Phase 4: Hardening] ◀── [Phase 3: Build]
       │
       ▼
[Phase 6: Operate]
```

1. **Phase 0 (Discovery):** User Research Synthesizer + Market Synthesizer define user pain and constraints.
2. **Phase 1 (Strategy):** Product Sprint Prioritizer + Senior Project Manager define scope and milestone gates.
3. **Phase 2 (Foundation):** Software Architect + Backend Architect establish schemas, ADRs, and scaffolding.
4. **Phase 3 (Build):** Frontend Developer + Mobile App Builder + Backend Architect implement features.
5. **Phase 4 (Hardening):** Reality Checker + Evidence Collector + Application Security Specialist run security scans, stress tests, and verify zero regressions.
6. **Phase 5 (Launch):** Growth Hacker + Technical Copywriter deploy assets, release notes, and documentation.
7. **Phase 6 (Operate):** SRE + Incident Response Commander maintain telemetry, SLOs, and uptime.

### 4.2 Standard Scenario Runbooks (`runbooks.json`)

- **`startup-mvp` (Sprint Mode, 4–6 weeks):**
  - *Core Roster:* `agents-orchestrator`, `project-manager-senior`, `product-sprint-prioritizer`, `design-ux-architect`, `engineering-frontend-developer`, `engineering-backend-architect`, `engineering-devops-automator`, `testing-evidence-collector`, `testing-reality-checker`.
  - *Growth Team (Week 3+):* `marketing-growth-hacker`, `marketing-content-creator`.
- **`enterprise-feature` (Sprint Mode, 6–12 weeks):**
  - Strict compliance, security audits, and multi-stakeholder approval gates.
- **`scenario-marketing-campaign`:**
  - Multi-channel synchronized campaign creation (copywriting, paid ads, social engagement, analytics).
- **`scenario-incident-response`:**
  - Immediate triage, root-cause isolation, emergency remediation, and post-mortem generation.

---

## 5. Tool Transpilation & Installation Engine (`scripts/`)

The core engineering substance powering The Agency's portability lives in `scripts/`:

```
                    ┌────────────────────────────┐
                    │ Raw Agent Markdown (.md)   │
                    │ Frontmatter + Personality  │
                    └─────────────┬──────────────┘
                                  │
                                  ▼ scripts/convert.sh
       ┌──────────────────────────┴──────────────────────────┐
       │                                                     │
       ▼                                                     ▼
Claude Code (.claude/agents/)                   Cursor (.cursorrules & .mdc)
Google Antigravity (.agents/skills/)            OpenCode (opencode runtime)
Gemini CLI                                      GitHub Copilot
OpenClaw / Aider / Windsurf                     Codex / Osaurus / Hermes / Vibe / DSH
```

### Key Technical Scripts:
- **`scripts/convert.sh`:** Transpiles raw persona markdown files into native JSON, markdown, or config structures for 14 different AI client tools.
- **`scripts/install.sh`:** Interactive terminal installation wizard. Automatically detects which AI tools are installed on the user's system and allows selective installation by division (`--division engineering,security`) or by runbook roster (`--agents-file team.txt`).
- **`scripts/check-divisions.sh` & `check-runbooks.sh`:** CI validation scripts ensuring every division folder, catalog entry, and roster slug remains synchronized and valid.
- **`scripts/build-hermes-plugin.py`:** Generates self-contained plugin bundles for the Hermes agent framework.

---

## 6. Synergy with Other Workspace Systems

The Agency fits cleanly into the broader ecosystem alongside **Coucou** and **Vorssaint**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AI AGENT WORKSPACE TRIFECTA                     │
├────────────────────────────────────────────────────────────────────────┤
│ 1. THE BRAIN & WORKFORCE: Agency Agents (msitarzewski/agency-agents)  │
│    • 282 specialized AI developer personas (Frontend, SRE, Architect) │
│    • NEXUS multi-agent project runbooks and handoffs.                 │
│                                                                        │
│ 2. AMBIENT SUPERVISION & TELEMETRY: Coucou (Louis-CFM/coucou)          │
│    • Lives in the MacBook notch / Windows top bar.                    │
│    • Real-time diffs (+N -M), permission approvals (Allow/Deny),     │
│      and iOS Live Activity remote sync.                               │
│                                                                        │
│ 3. HARDWARE & LOCAL UTILITY HUB: Vorssaint (vorssaint-utils)           │
│    • System monitor, fan curves, memory pressure, window snapping.    │
│    • Dynamic Island agent token/cost meter for Claude & Codex.        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 7. SWOT & Engineering Assessment

### Strengths
1. **Unrivaled Breadth & Polish:** 282 specialized agents with genuine personality differentiation, domain-tailored constraints, and realistic workflow deliverables.
2. **True Tool-Agnostic Design:** Compiles and installs seamlessly across Claude Code, Antigravity, Cursor, Gemini CLI, OpenCode, Codex, Aider, and Windsurf.
3. **Structured Governance (NEXUS):** Solves the "blank canvas" multi-agent coordination problem by supplying battle-tested runbooks and handoff templates.
4. **Developer-Friendly Distribution:** Zero-friction desktop app (`agencyagents.app`) alongside comprehensive shell scripts for CLI power users.

### Considerations & Technical Gotchas
1. **Context Window Overhead:** Loading multiple complete agent personas simultaneously can consume significant context tokens; using the `--division` or `--agents-file` selective installer is essential.
2. **Runtime Agent Caps:** As noted in the documentation, runtimes like OpenCode cap total registered agents at ~119, requiring targeted division installs rather than loading all 282 at once.

---

## 8. Conclusion

`agency-agents` is the gold standard for **AI persona engineering and multi-agent coordination**. By turning vague AI instructions into 282 specialized, production-ready specialists with explicit deliverables, it transforms general LLMs into a coordinated, multi-department autonomous agency.
