# AI Agent Multimodal End-to-End Analysis Workspace

Welcome, AI Agent. This repository is the **Universal Multimodal End-to-End Analysis Suite**, engineered to provide deterministic, zero-hallucination analysis for **Images**, **Videos**, and **Websites** across Windows, macOS, and Linux.

---

## 📁 Workspace Architecture (Read This First)

```
Skills/
├── .agents/              ← IDE auto-discovery (symlinks → setup/ & core/)
│   ├── rules/            ← Symlinks → setup/rules/ (canonical source)
│   └── skills/           ← Curated showcase skills for IDE pickup
│
├── setup/                ← START HERE — Onboarding, context, rules, bootstrap
│   ├── CONTEXT.md           Full workspace map & orientation guide
│   ├── rules/               CANONICAL rules (AGENTS.md, GEMINI.md, CLAUDE.md)
│   ├── config/              MCP configuration (mcp_config.json)
│   └── scripts/             Cross-platform bootstrap (setup.sh / setup.bat)
│
├── master-skiller/       ← Routing brain — translates prompts into skill pipelines
│   ├── SKILL.md             How to use the orchestrator
│   ├── catalog.json         2,499+ indexed skills (name, description, tags, domain)
│   ├── taxonomy.json        15 domain classifications & lifecycle phases
│   └── scripts/router.py   Python query engine
│
└── core/                 ← All executable substance lives here
    ├── skills/              2,499+ curated, deduplicated skills
    ├── analyzers/
    │   ├── image-analyzer/  Image & PDF analysis toolkit
    │   ├── video-analyzer/  Video & audio analysis toolkit
    │   └── website-analyzer/ Web audit toolkit
    └── launchers/
        ├── analyze.py       Unified cross-platform CLI (image/video/website/route/doctor)
        ├── analyze.sh/.bat  Shell convenience wrappers
        └── route.sh/.bat    Skill routing convenience wrappers
```

> **Rule**: `setup/rules/` is the canonical source for all agent rules. `.agents/rules/` files are symlinks — edit in `setup/rules/`, changes propagate instantly.

---

## ⚡ Autonomous Agent Protocol (Zero-Prompt Trigger)

Whenever the user provides, references, attaches, or links any media or website in their prompt:
**DO NOT GUESS. DO NOT HALLUCINATE.** Execute the appropriate analyzer immediately on your very first turn.

```
                  ┌───────────────────────────────────────────────┐
                  │             USER INPUT / TARGET               │
                  └───────────────────────┬───────────────────────┘
                                          │
            ┌─────────────────────────────┼─────────────────────────────┐
            ▼                             ▼                             ▼
   [Image / Document]              [Video / Screencast]           [Website / Web App]
   (.png, .jpg, .webp, .pdf)       (.mp4, .mov, .webm, .mkv)     (localhost:*, https://*)
            │                             │                             │
            ▼                             ▼                             ▼
    core/analyzers/               core/analyzers/               core/analyzers/
    image-analyzer/               video-analyzer/               website-analyzer/
   `python core/launchers/analyze.py image`  `python core/launchers/analyze.py video`  `python core/launchers/analyze.py website`
```

---

## 🛠️ Execution Commands (Cross-Platform)

### 1. Image & Document Analysis
- **Unified CLI**: `python core/launchers/analyze.py image <path-to-image>`
- **Direct Script**: `python core/analyzers/image-analyzer/scripts/image_analyzer.py <path-to-image>`
- **Telemetry**: Width × height, EXIF data, dominant color palette (HEX, RGB), Tesseract OCR.
- **Multimodal**: Always invoke `view_file` on the image or 300 DPI Poppler render.

### 2. Video & Screen Recording Analysis
- **Unified CLI**: `python core/launchers/analyze.py video <path-to-video>`
- **Direct Script**: `python core/analyzers/video-analyzer/scripts/video_analyzer.py <path-to-video>`
- **Telemetry**: Codecs, framerate, keyframes, **Storyboard Contact Sheet** (`video_storyboard.jpg`), Whisper transcript.
- **MANDATORY**: Call `view_file` on `video_storyboard.jpg` for full chronological scene inspection.

### 3. Website & Web App Analysis
- **Unified CLI**: `python core/launchers/analyze.py website <url>`
- **Direct Script**: `node core/analyzers/website-analyzer/scripts/website_analyzer.mjs <url>`
- **Telemetry**: Responsive screenshots (Desktop/Tablet/Mobile), Lighthouse CWV, SEO meta, heading hierarchy.
- **Visual Grounding**: Call `view_file` on captured screenshots before answering.

### 4. Master Skill Orchestration (Prompt → Pipeline)
- **Unified CLI**: `python core/launchers/analyze.py route "<user prompt or task brief>"`
- **Direct Script**: `python master-skiller/scripts/router.py "<prompt>" --top 4 --json`
- **Output**: Sub-second matching across 2,499+ indexed skills, relevance scores, ordered pipeline (Analysis → Design → Implementation → Testing → Security → Growth/Audit).
- **Mandate**: For complex tasks, run the router first, then invoke recommended skills sequentially via `view_file` on their `SKILL.md`.

---

## 🔍 System Verification & Diagnostics

When running on a new machine or environment, run:
```bash
python core/launchers/analyze.py doctor
```
This tests for `python`, `node`, `uv`, `ffmpeg`, `tesseract`, and `chrome` on Windows, macOS, or Linux, reporting any missing dependencies with exact install commands.

**Bootstrap from scratch:**
```bash
# macOS / Linux
bash setup/scripts/setup.sh

# Windows (run as Administrator)
setup\scripts\setup.bat
```

---

## 🛡️ Zero-Hallucination Mandate
- **Colors**: Always quote extracted `#RRGGBB` hex values from the analyzer report.
- **Text & OCR**: Match strings word-for-word against the OCR output.
- **Video Timecodes**: Quote exact timestamps (`01:24`) from the storyboard or Whisper transcript.
- **Web Layout**: Validate against captured responsive screenshots before answering.
- **Skills**: Always query `master-skiller/scripts/router.py` before selecting skills for complex tasks.
