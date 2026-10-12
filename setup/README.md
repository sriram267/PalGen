# Universal AI Agent Multimodal End-to-End Analysis Suite
### Cross-Platform Support: Windows, macOS, and Linux

A production-grade, zero-hallucination analysis suite and skill orchestrator engineered for autonomous AI agents (Gemini, Claude, Antigravity, Cursor, Copilot) and human developers.

---

## 📁 Repository Structure

```
Skills/
├── setup/                         # Environment Bootstrap, Onboarding & Canonical Rules
│   ├── CONTEXT.md                 # Full workspace orientation guide
│   ├── README.md                  # Comprehensive documentation
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
└── core/                          # All Executable Substance & Curated Toolkits
    ├── skills/                    # 2,499+ Curated & Deduplicated Specialized Skills
    ├── analyzers/                 # Multimodal Analysis Toolkits
    │   ├── image-analyzer/        # Image & Document analysis (Pillow, Tesseract, Poppler)
    │   ├── video-analyzer/        # Video & Audio analysis (FFmpeg, Whisper, OCR)
    │   └── website-analyzer/      # Web audit engine (Puppeteer, Lighthouse, SEO)
    └── launchers/                 # Cross-Platform CLI Runners
        ├── analyze.py             # Unified CLI (image, video, website, route, doctor)
        ├── analyze.sh / .bat      # Interactive menu launchers
        └── route.sh / .bat        # Skill routing CLI shortcuts
```

---

## 🚀 One-Click Setup (New Machine or Fresh Clone)

```bash
# macOS / Linux
bash setup/scripts/setup.sh

# Windows (Command Prompt as Administrator)
setup\scripts\setup.bat
```

To recreate IDE auto-discovery symlinks only:
```bash
bash setup/scripts/setup.sh --symlinks-only
```

Verify everything is installed:
```bash
python core/launchers/analyze.py doctor
```

---

## 🧠 Master Skill Routing

Query the 2,499+ skills catalog and generate an ordered multi-stage execution pipeline:

```bash
# Using Python CLI
python core/launchers/analyze.py route "<your prompt>"

# Or using the route convenience script
bash core/launchers/route.sh "<your prompt>"
```

---

## 🛠️ Multimodal Analyzers

```bash
# Image / Document Analysis (EXIF, dominant palette, OCR)
python core/launchers/analyze.py image <path-to-image>

# Video / Screencast Analysis (Telemetry, Storyboard contact sheet, Whisper transcript)
python core/launchers/analyze.py video <path-to-video>

# Website / Web App Audit (Mobile/Tablet/Desktop screenshots, Core Web Vitals, SEO)
python core/launchers/analyze.py website <url>
```
