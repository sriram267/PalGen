# Video End-to-End Analyzer Suite

An enterprise multimodal video analysis toolkit for AI agents and human engineers. Provides deterministic, zero-hallucination video comprehension by combining FFprobe telemetry, FFmpeg keyframe extraction, single-turn visual storyboard contact sheet compilation (`video_storyboard.jpg`), Whisper timestamped speech transcription, and on-screen Tesseract OCR.

---

## Architecture & Components

```
video-analyzer/
├── SKILL.md                  # Autonomous agent instructions, schemas & zero-hallucination rules
├── README.md                 # Complete toolkit overview and usage documentation
├── scripts/
│   └── video_analyzer.py     # Standalone CLI tool for full video pipeline execution
└── mcp/
    └── mcp_config.json       # MCP configuration for Claude Desktop, Antigravity, Gemini & Cursor
```

---

## Key Capabilities

1. **Single-Turn Multimodal Visual Inspection**: Instead of sending hundreds of video frames, the engine compiles a high-density **Storyboard Contact Sheet** (`video_storyboard.jpg`) with burned-in timestamp badges. The AI agent inspects this single image via `view_file` to "watch" the entire timeline in one multimodal turn.
2. **Container & Stream Telemetry**: Uses `ffprobe` to determine precise duration, video codecs (H.264, VP9, AV1, ProRes), framerate, resolution, audio channels, and bitrates.
3. **Temporal Speech-to-Text Transcription**: Powered by `faster-whisper` to generate exact timestamped transcript lines (`[00:01:23 -> 00:01:35] Spoken words`).
4. **On-Screen Code & Text OCR**: Runs local Tesseract OCR on extracted keyframes to read terminal commands, browser URLs, button labels, and code snippets shown on screen.
5. **Precision Keyframe Deep Dives**: When a specific second contains a bug or code, individual high-res keyframes (`keyframe_04_01m20s.jpg`) can be inspected directly.

---

## Quick Start & CLI Usage

### 1. Run Complete Video Deep Analysis
```bash
python3 core/analyzers/video-analyzer/scripts/video_analyzer.py /path/to/video.mp4
```

### 2. Generate Storyboard Contact Sheet Only
```bash
python3 core/analyzers/video-analyzer/scripts/video_analyzer.py /path/to/video.mp4 --storyboard-only
```

### 3. Skip Speech Transcription (Faster for Silent Screencasts)
```bash
python3 core/analyzers/video-analyzer/scripts/video_analyzer.py /path/to/video.mp4 --no-transcribe
```

### 4. Save Markdown Report to File
```bash
python3 core/analyzers/video-analyzer/scripts/video_analyzer.py /path/to/video.mp4 -o /path/to/report.md
```

---

## MCP Server Integration

Add the contents of `mcp/mcp_config.json` to your AI client configuration:
- Tools provided: `deep_analyze_video`, `generate_video_storyboard`, `extract_video_keyframes`, `transcribe_media_audio`.
