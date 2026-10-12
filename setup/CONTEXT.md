# Workspace Context — Universal Multimodal Analysis & Skill Orchestration Suite

> **For any AI Agent or human developer:** Read this document before doing anything else.
> This file is the single source of truth for understanding what this workspace is, how it's structured, and how to use every system in it.

---

## 🎯 What This Workspace Is

This is a **portable, cross-platform AI agent capability hub** designed to:

1. **Analyze anything** — Images, videos, PDFs, and websites with zero hallucination.
2. **Orchestrate skills** — Route complex user prompts to the right skill pipelines from a catalog of 2,499+ verified skills.
3. **Bootstrap any machine** — One command gets every dependency installed on macOS, Linux, or Windows.
4. **Auto-configure any AI IDE** — Rules, skills, and MCP configs are auto-discovered by Antigravity, Cursor, Claude Code, and others.

---

## 📁 Folder Map

| Folder | Purpose |
|--------|---------|
| `setup/` | **You are here.** Onboarding, canonical rules, MCP config, bootstrap scripts. |
| `master-skiller/` | Routing brain. Translates any prompt into an ordered skill execution pipeline. |
| `core/` | All executable substance: 2,499+ skills, analyzer toolkits, and CLI launchers. |
| `.agents/` | IDE auto-discovery root. Rules and curated skills here are symlinked from `setup/` and `core/`. |
| `.cursor/` | Cursor IDE configuration. |

---

## 🔗 Symlink Architecture (How Auto-Discovery Works)

Rules and curated skills are **stored canonically in `setup/`** and **symlinked into `.agents/`** for zero-lag IDE auto-discovery:

```
setup/rules/AGENTS.md                  ──symlink──▶  .agents/rules/AGENTS.md                 (Antigravity)
setup/rules/GEMINI.md                  ──symlink──▶  .agents/rules/GEMINI.md                  (Gemini)
setup/rules/CLAUDE.md                  ──symlink──▶  .agents/rules/CLAUDE.md                  (Claude)
setup/rules/agent-instructions.mdc     ──symlink──▶  .cursor/rules/agent-instructions.mdc     (Cursor)
```

**Edit rule files in `setup/rules/` only.** Changes propagate instantly to all IDE locations.
The workspace root contains NO visible loose files — only the 3 primary directories (`setup/`, `master-skiller/`, `core/`) plus hidden IDE dot-folders.

---

## 🚀 Quick Start — New Machine Setup

```bash
# macOS / Linux
bash setup/scripts/setup.sh

# Windows (PowerShell as Administrator)
.\setup\scripts\setup.bat
```

After setup, verify all dependencies:
```bash
python core/launchers/analyze.py doctor
```

---

## 🧠 Core Capabilities

### Analyzer Toolkit (`core/analyzers/`)

| Analyzer | Command | What It Does |
|----------|---------|-------------|
| **Image** | `python core/launchers/analyze.py image <path>` | EXIF, color palette, OCR, 300 DPI render |
| **Video** | `python core/launchers/analyze.py video <path>` | Storyboard, Whisper transcript, keyframe OCR |
| **Website** | `python core/launchers/analyze.py website <url>` | Lighthouse CWV, responsive screenshots, SEO |

### Master Skiller (`master-skiller/`)

Routes any prompt to an ordered pipeline of skills:
```bash
python core/launchers/analyze.py route "build a SaaS landing page with dark mode"
# → Returns: [frontend-design → uiux-designer → copywriting → a11y-debugging]
```

---

## 📋 Agent Rules Summary

| Rule | Location |
|------|---------|
| `AGENTS.md` | Universal agent protocol — analyzers, routing, zero-hallucination mandate |
| `GEMINI.md` | Gemini-specific trigger rules |
| `CLAUDE.md` | Claude-specific trigger rules |
| `agent-instructions.mdc` | Cursor workspace behavior rules |

All rules are in `setup/rules/`. `.agents/rules/` and `.cursor/rules/` contain only symlinks.

---

## 🌐 Portability

This workspace is designed to be copied to any machine and work immediately:

- **No hardcoded paths** — all scripts use relative paths from workspace root.
- **Cross-platform** — `.py` launchers auto-detect OS; `.sh`/`.bat` wrappers provided for both.
- **MCP config** — `setup/config/mcp_config.json` is portable and IDE-agnostic.
- **Symlinks** — Recreate them on new machine with: `bash setup/scripts/setup.sh --symlinks-only`

---

## 📦 Skills Catalog Stats

| Metric | Value |
|--------|-------|
| Total skills in `core/skills/` | 2,499+ |
| Curated showcase in `.agents/skills/` | ~18 flagship skills |
| Domains covered | 15 (see `master-skiller/taxonomy.json`) |
| Catalog index | `master-skiller/catalog.json` |

---

## 🔍 Diagnostics & Troubleshooting

```bash
# Check all dependencies (python, node, ffmpeg, tesseract, chrome)
python core/launchers/analyze.py doctor

# Test skill routing
python master-skiller/scripts/router.py "analyze a user flow video" --top 3

# Rebuild symlinks (e.g., after copying to a new machine)
bash setup/scripts/setup.sh --symlinks-only
```
