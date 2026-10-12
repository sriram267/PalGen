---
name: video-analyzer
description: Production-grade end-to-end video analysis suite for AI agents. Performs container and stream telemetry (FFprobe), temporal keyframe extraction (FFmpeg), single-turn visual storyboard contact sheet generation (video_storyboard.jpg), timestamped speech transcription (faster-whisper), and on-screen OCR.
---

# Video End-to-End Analyzer Skill for AI Agents

This skill provides an autonomous, end-to-end framework for analyzing any video or screen recording file (`.mp4`, `.mov`, `.mkv`, `.webm`, `.avi`, `.flv`).

Video files present a high-density challenge for AI models: they combine continuous visual scene transitions across time with synchronized audio/speech and on-screen code or text. AI agents cannot watch videos via text prompts alone. This skill enforces a structured 4-step multimodal extraction pipeline that guarantees temporal grounding, single-turn visual comprehension, and zero hallucination.

---

## 1. When to Activate This Skill

Activate this skill immediately whenever:
- The user provides, references, or links a **Video File** (`.mp4`, `.mov`, `.mkv`, `.webm`, etc.).
- The user provides a **Screen Recording** of a bug, UI interaction, workflow, or software demo.
- The user asks to audit visual animations, transitions, speech dialogue, on-screen text, or temporal bugs.
- The user asks for a video summary, chapter breakdown, or subtitle/transcript extraction.

---

## 2. Integrated Tool Suite

| Component | Technology | Primary Function |
| :--- | :--- | :--- |
| **Stream & Container Telemetry** | `ffprobe` | Extracts exact container specs, duration, video codecs (H.264, HEVC, VP9, AV1), framerate, resolution, audio sample rates, and bitrates. |
| **Temporal Keyframe Extractor** | `ffmpeg` | Uniformly extracts keyframes across the video duration or at custom intervals. |
| **Visual Storyboard Engine** | `Pillow` + Burned-in Badges | Compiles all keyframes into a single high-density **Storyboard Contact Sheet** (`video_storyboard.jpg`) with burned-in timestamps. |
| **Speech-to-Text Transcription** | `faster-whisper` | Generates word-level and phrase-level timestamped transcripts (`[HH:MM:SS -> HH:MM:SS]`) from audio tracks. |
| **On-Screen Text OCR** | `tesseract` | Detects and transcribes on-screen code, terminal commands, buttons, and error messages from keyframes. |

---

## 3. Mandatory Autonomous 4-Step Protocol

When any video file is detected, the AI agent must autonomously execute this pipeline:

```
[Input Video File]
        │
        ├──► Step 1: Deep Video Telemetry & Extraction
        │            Run deep_analyze_video or CLI video_analyzer.py.
        │            Extracts specs, keyframes, storyboard, transcript, and OCR.
        │
        ├──► Step 2: Direct Visual Storyboard Inspection (view_file)
        │            MANDATORY: Call view_file on video_storyboard.jpg.
        │            View the entire chronological video progression in 1 multimodal turn!
        │
        ├──► Step 3: Targeted Scene & Keyframe Precision Inspection
        │            If an exact second has code or UI bugs, call view_file on keyframe_XX.jpg.
        │
        └──► Step 4: Correlate Audio & Speech with Visual Transitions
                     Align Whisper transcript timestamps with keyframe visual events.
```

### Step 1: Execute Video Deep Analysis
Call MCP tool `deep_analyze_video` or run CLI `video_analyzer.py`:
```bash
python3 /Users/waffor/Desktop/Skills/video-analyzer/scripts/video_analyzer.py <path-to-video.mp4>
```
This automatically produces:
1. Video telemetry (duration, resolution, fps, codecs).
2. Keyframes directory (`keyframe_01.jpg`, `keyframe_02.jpg`, etc.).
3. High-density **Storyboard Contact Sheet** (`video_storyboard.jpg`).
4. Whisper audio transcript with timestamps.
5. OCR text detected on extracted keyframes.

### Step 2: Direct Multimodal Storyboard Inspection (MANDATORY)
**Call `view_file` on `video_storyboard.jpg`.**
- Because video files cannot be directly read as text, the Storyboard Contact Sheet is the primary visual bridge.
- Seeing all frames arranged in a grid with burned-in timestamp badges allows the AI model to observe the entire timeline in a single prompt turn without context overflow.

### Step 3: Targeted Keyframe Inspection
When inspecting fine details (e.g. reading a terminal error, analyzing a subtle animation bug, or inspecting an input field), identify the timestamp from the storyboard and call `view_file` on the corresponding individual keyframe (e.g. `keyframe_03_00m45s.jpg`).

### Step 4: Ground Audio Transcript with Visual Progression
Cross-reference spoken words with visual actions:
- Match when a speaker says "Now clicking submit" with the keyframe where the modal appears.
- Ensure audio explanations and visual actions are synchronized in your technical analysis.

---

## 4. MCP Tool Reference

### `media_deep_analyzer:deep_analyze_video`
```json
{
  "ServerName": "media_deep_analyzer",
  "ToolName": "deep_analyze_video",
  "Arguments": {
    "video_path": "/absolute/path/to/video.mp4",
    "max_keyframes": 16,
    "sample_interval": null,
    "transcribe": true,
    "perform_ocr": true
  }
}
```

### `media_deep_analyzer:generate_video_storyboard`
```json
{
  "ServerName": "media_deep_analyzer",
  "ToolName": "generate_video_storyboard",
  "Arguments": {
    "video_path": "/absolute/path/to/video.mp4",
    "columns": 4,
    "max_frames": 16
  }
}
```

### `media_deep_analyzer:transcribe_media_audio`
```json
{
  "ServerName": "media_deep_analyzer",
  "ToolName": "transcribe_media_audio",
  "Arguments": {
    "media_path": "/absolute/path/to/video.mp4",
    "model_size": "tiny"
  }
}
```

---

## 5. CLI Utility Usage

The bundled CLI tool is located at `scripts/video_analyzer.py`:

```bash
# Complete end-to-end video analysis
python3 /Users/waffor/Desktop/Skills/video-analyzer/scripts/video_analyzer.py /path/to/video.mp4

# Extract storyboard only
python3 /Users/waffor/Desktop/Skills/video-analyzer/scripts/video_analyzer.py /path/to/video.mp4 --storyboard-only

# Skip audio transcription (faster for silent screen captures)
python3 /Users/waffor/Desktop/Skills/video-analyzer/scripts/video_analyzer.py /path/to/video.mp4 --no-transcribe

# Save report to markdown
python3 /Users/waffor/Desktop/Skills/video-analyzer/scripts/video_analyzer.py /path/to/video.mp4 -o /path/to/report.md
```

---

## 6. Zero-Hallucination Quality Gate

Before providing any answers about video content:
1. **Never guess timestamps**: Always quote the exact timecode (`01:24`) from the storyboard or Whisper transcript.
2. **Never guess spoken words**: Always quote directly from the Whisper speech-to-text transcript.
3. **Never assume visual state**: If the storyboard is ambiguous, inspect the full-resolution keyframe using `view_file`.
