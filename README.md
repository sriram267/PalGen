# PalGen — Universal AI Agent Multimodal Suite & Marketing ERP

Welcome to the **PalGen** repository — combining the **Universal Multimodal End-to-End Analysis Suite** (2,499+ verified agent skills, routing engine, and visual/audio/web analyzers) with the **PalGen Sales & Marketing ERP** and its ambient interface **Pal**.

---

## 📁 Repository Structure

```
Skills/
├── setup/                         # Environment Bootstrap, Onboarding & Canonical Rules
│   ├── CONTEXT.md                 # Full workspace orientation guide
│   ├── README.md                  # Detailed environment setup documentation
│   ├── rules/                     # Canonical agent rules (AGENTS.md, GEMINI.md, CLAUDE.md)
│   ├── config/mcp_config.json     # Master MCP configuration
│   └── scripts/                   # Cross-platform bootstraps (setup.sh, setup.bat)
│
├── master-skiller/                # Universal Agent Skill Router & Pipeline Orchestrator
│   ├── SKILL.md                   # Master orchestrator instructions & domain taxonomy
│   ├── catalog.json               # Fast searchable index of all 2,499+ verified skills
│   ├── taxonomy.json              # 15 domain classifications & lifecycle phases
│   └── scripts/router.py          # Sub-second CLI query engine & DAG pipeline generator
│
├── core/                          # All Executable Substance & Curated Toolkits
│   ├── skills/                    # 2,499+ Curated & Deduplicated Specialized Skills
│   ├── analyzers/                 # Multimodal Analysis Toolkits
│   │   ├── image-analyzer/        # Image & Document analysis (Pillow, Tesseract, Poppler)
│   │   ├── video-analyzer/        # Video & Audio analysis (FFmpeg, Whisper, OCR)
│   │   └── website-analyzer/      # Web audit engine (Puppeteer, Lighthouse, SEO)
│   └── launchers/                 # Cross-Platform CLI Runners (analyze.py, route.sh)
│
├── product/                       # PalGen Product Strategy, Roadmap & Prototypes
│   ├── roadmap/                   # Canonical Product Baseline (v2.0)
│   │   ├── README.md              # Project roadmap & source-of-truth rules
│   │   ├── product_strategy.md    # Product layers, monetization & lead-readiness contract
│   │   ├── implementation_roadmap.md # Evidence-gated execution phases (P0–P8, Track D)
│   │   ├── architecture_decisions.md # Decision register (D-001 through D-022)
│   │   ├── ux_information_architecture.md # Navigation, shared surfaces & UX design
│   │   └── erp_production_system_design.md # Modular monolith & channel orchestration design
│   ├── Palgen/                    # Ambient Interface Web Prototype (Vite + React + Vanilla CSS)
│   └── req/                       # Requirements & UI/UX Research (Apple HIG, Coucou, Agency Agents)
│
└── .agents/                       # Agent auto-discovery symlinks (rules & showcase skills)
```

---

## 🚀 Quick Start & Environment Setup

```bash
# macOS / Linux bootstrap
bash setup/scripts/setup.sh

# Windows (Command Prompt as Administrator)
setup\scripts\setup.bat

# Verify environment binaries
python core/launchers/analyze.py doctor
```

---

## 🧠 Master Skill Routing & Multimodal Analysis

Query the 2,499+ skills catalog and generate an ordered multi-stage execution pipeline:

```bash
# Query skills router
python core/launchers/analyze.py route "<your prompt>"

# Multimodal analyzers
python core/launchers/analyze.py image <path-to-image>
python core/launchers/analyze.py video <path-to-video>
python core/launchers/analyze.py website <url>
```

---

## 🧭 PalGen Product Architecture

- **Canonical Product Strategy**: See [`product/roadmap/product_strategy.md`](product/roadmap/product_strategy.md)
- **Implementation Sequencing**: See [`product/roadmap/implementation_roadmap.md`](product/roadmap/implementation_roadmap.md)
- **Architecture Register**: See [`product/roadmap/architecture_decisions.md`](product/roadmap/architecture_decisions.md)
- **UX Information Architecture**: See [`product/roadmap/ux_information_architecture.md`](product/roadmap/ux_information_architecture.md)
- **Ambient Prototype**: Run `cd product/Palgen && npm install && npm run dev` to launch the Coucou-inspired Dynamic Island ambient interface.
