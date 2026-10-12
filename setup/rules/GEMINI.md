# Antigravity & Gemini Workspace Instructions

This workspace contains the **Universal Multimodal End-to-End Analysis Suite** for Images, Videos, and Websites.

Please refer to [AGENTS.md](file:///Users/waffor/Desktop/Skills/setup/rules/AGENTS.md) for complete instructions, autonomous execution protocols, and CLI reference.

### Core Autonomous Rules:
1. **Images/Documents**: Run `python core/launchers/analyze.py image <path>` and inspect via `view_file`.
2. **Videos/Screencasts**: Run `python core/launchers/analyze.py video <path>` and inspect `video_storyboard.jpg` via `view_file`.
3. **Websites/URLs**: Run `python core/launchers/analyze.py website <url>` and inspect multi-viewport screenshots via `view_file`.
4. **Environment Check**: Run `python core/launchers/analyze.py doctor` to verify system binaries across Windows, macOS, or Linux.
5. **Skill Orchestration**: Run `python core/launchers/analyze.py route "<prompt>"` or query `master-skiller/scripts/router.py` to get recommended skills and chronological execution pipelines.
