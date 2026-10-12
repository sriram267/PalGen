#!/usr/bin/env python3
"""
Video End-to-End Analyzer CLI for AI Agents
Cross-Platform: Windows, macOS, and Linux
Performs video container/stream telemetry (FFprobe), temporal keyframe extraction (FFmpeg),
single-turn visual storyboard contact sheet generation (Pillow),
audio speech transcription (faster-whisper), and on-screen OCR (Tesseract).
"""

import os
import sys
import json
import math
import shutil
import argparse
import platform
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional


def find_binary(name: str) -> Optional[str]:
    """Find binary executable across Windows, macOS, and Linux."""
    found = shutil.which(name)
    if found:
        return found
    if platform.system() == "Windows":
        found = shutil.which(f"{name}.exe")
        if found:
            return found

    system = platform.system()
    candidates = []

    if system == "Darwin":
        candidates = [
            f"/opt/homebrew/bin/{name}",
            f"/usr/local/bin/{name}",
            f"/usr/bin/{name}"
        ]
    elif system == "Windows":
        prog_files = os.environ.get("ProgramFiles", "C:\\Program Files")
        prog_files_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
        local_app = os.environ.get("LOCALAPPDATA", "")
        user_prof = os.environ.get("USERPROFILE", "")

        if name in ("ffmpeg", "ffprobe"):
            candidates = [
                f"C:\\ffmpeg\\bin\\{name}.exe",
                os.path.join(prog_files, "ffmpeg", "bin", f"{name}.exe"),
                os.path.join(local_app, "Microsoft", "WinGet", "Links", f"{name}.exe"),
                os.path.join(user_prof, "scoop", "shims", f"{name}.exe")
            ]
        elif name == "tesseract":
            candidates = [
                os.path.join(prog_files, "Tesseract-OCR", "tesseract.exe"),
                os.path.join(prog_files_x86, "Tesseract-OCR", "tesseract.exe"),
            ]
        elif name == "uv":
            candidates = [
                os.path.join(user_prof, ".cargo", "bin", "uv.exe"),
                os.path.join(local_app, "uv", "uv.exe"),
                os.path.join(prog_files, "uv", "uv.exe")
            ]
    else:  # Linux
        candidates = [
            f"/usr/bin/{name}",
            f"/usr/local/bin/{name}",
            f"/snap/bin/{name}"
        ]

    for p in candidates:
        if p and Path(p).exists():
            return str(p)
    return None


# Auto re-exec with uv if Pillow is missing
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    if os.environ.get("_UV_REEXEC"):
        print("Error: Pillow is required. Run 'pip install Pillow' or install 'uv'.", file=sys.stderr)
        sys.exit(1)
    uv_bin = find_binary("uv")
    if uv_bin:
        os.environ["_UV_REEXEC"] = "1"
        cmd = [uv_bin, "run", "--with", "Pillow", "python", str(Path(__file__).resolve())] + sys.argv[1:]
        if platform.system() == "Windows":
            subprocess.run(cmd)
            sys.exit(0)
        else:
            os.execv(uv_bin, cmd)
    else:
        print("Error: Pillow is required. Run 'pip install Pillow' or install 'uv'.", file=sys.stderr)
        sys.exit(1)


def format_time(seconds: float) -> str:
    """Format seconds into HH:MM:SS or MM:SS."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    hours = int(mins // 60)
    mins = int(mins % 60)
    if hours > 0:
        return f"{hours:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"


def get_ffprobe_data(file_path: Path, ffprobe_bin: str) -> Dict[str, Any]:
    """Inspect media file with ffprobe."""
    cmd = [
        ffprobe_bin,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(file_path)
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(res.stdout)
    except Exception as e:
        return {"error": str(e)}


def extract_keyframes(video_path: Path, output_dir: Path, ffmpeg_bin: str, duration: float, max_frames: int = 16) -> List[Dict[str, Any]]:
    """Extract uniform keyframes across video duration."""
    output_dir.mkdir(parents=True, exist_ok=True)
    frames = []

    step = duration / (max_frames + 1) if duration > 0 else 1.0
    timestamps = [min(duration - 0.1 if duration > 0 else 10.0, (i + 1) * step) for i in range(max_frames)]

    for idx, ts in enumerate(timestamps, start=1):
        time_tag = format_time(ts).replace(":", "m") + "s"
        frame_name = f"keyframe_{idx:02d}_{time_tag}.jpg"
        frame_path = output_dir / frame_name

        cmd = [
            ffmpeg_bin,
            "-ss", str(ts),
            "-i", str(video_path),
            "-vframes", "1",
            "-q:v", "2",
            "-y",
            str(frame_path)
        ]
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            if frame_path.exists():
                frames.append({
                    "index": idx,
                    "timestamp_sec": ts,
                    "timecode": format_time(ts),
                    "path": str(frame_path)
                })
        except Exception:
            continue

    return frames


def build_storyboard_contact_sheet(frames: List[Dict[str, Any]], output_path: Path, columns: int = 4) -> Optional[str]:
    """Compile keyframes into a single contact sheet with burned-in timestamps."""
    if not frames:
        return None

    loaded_images = []
    for f in frames:
        p = Path(f["path"])
        if p.exists():
            try:
                img = Image.open(p).convert("RGB")
                loaded_images.append((img, f["timecode"]))
            except Exception:
                pass

    if not loaded_images:
        return None

    orig_w, orig_h = loaded_images[0][0].size
    target_w = 480
    target_h = int(orig_h * (target_w / orig_w)) if orig_w > 0 else 270

    num_frames = len(loaded_images)
    cols = min(columns, num_frames)
    rows = math.ceil(num_frames / cols)

    sheet_w = cols * target_w
    sheet_h = rows * target_h
    sheet = Image.new("RGB", (sheet_w, sheet_h), color=(15, 23, 42))

    for idx, (img, timecode) in enumerate(loaded_images):
        col = idx % cols
        row = idx // cols
        x = col * target_w
        y = row * target_h

        resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(resized)

        # Draw timestamp badge
        badge_text = f" {timecode} "
        badge_w = len(badge_text) * 9
        badge_h = 24
        draw.rectangle([10, 10, 10 + badge_w, 10 + badge_h], fill=(0, 0, 0, 200))
        draw.text((14, 14), badge_text, fill=(255, 255, 255))

        sheet.paste(resized, (x, y))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, "JPEG", quality=88)
    return str(output_path)


def run_transcription(media_path: Path) -> List[Dict[str, Any]]:
    """Transcribe speech using faster-whisper if installed."""
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(str(media_path), beam_size=1)
        transcripts = []
        for s in segments:
            transcripts.append({
                "start": s.start,
                "end": s.end,
                "timestamp": f"[{format_time(s.start)} -> {format_time(s.end)}]",
                "text": s.text.strip()
            })
        return transcripts
    except Exception as e:
        return [{"timestamp": "[N/A]", "text": f"(Whisper transcription skipped: {e})"}]


def run_tesseract_ocr(frame_path: str, tesseract_bin: Optional[str]) -> str:
    """Run OCR on a keyframe."""
    if not tesseract_bin:
        return ""
    try:
        res = subprocess.run([tesseract_bin, frame_path, "stdout"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return ""


def main():
    parser = argparse.ArgumentParser(description="Video End-to-End Analyzer for AI Agents (Cross-Platform)")
    parser.add_argument("video_path", help="Path to video file (.mp4, .mov, .mkv, .webm, etc.)")
    parser.add_argument("--max-frames", type=int, default=16, help="Maximum keyframes to extract (default: 16)")
    parser.add_argument("--storyboard-only", action="store_true", help="Only generate visual storyboard sheet")
    parser.add_argument("--no-transcribe", action="store_true", help="Skip speech audio transcription")
    parser.add_argument("--no-ocr", action="store_true", help="Skip OCR on keyframes")
    parser.add_argument("-o", "--output", help="Write report to specified output path")

    args = parser.parse_args()
    vid_path = Path(args.video_path).resolve()

    if not vid_path.exists():
        print(f"Error: Video file does not exist: {vid_path}", file=sys.stderr)
        sys.exit(1)

    ffmpeg_bin = find_binary("ffmpeg")
    ffprobe_bin = find_binary("ffprobe")
    tesseract_bin = find_binary("tesseract")

    if not ffmpeg_bin or not ffprobe_bin:
        print("Error: ffmpeg and ffprobe must be installed on your system.", file=sys.stderr)
        print("  Windows: winget install Gyan.FFmpeg", file=sys.stderr)
        print("  macOS:   brew install ffmpeg", file=sys.stderr)
        print("  Linux:   sudo apt install ffmpeg", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing video: {vid_path.name} on {platform.system()}...", file=sys.stderr)

    # 1. Telemetry
    probe = get_ffprobe_data(vid_path, ffprobe_bin)
    format_info = probe.get("format", {})
    duration = float(format_info.get("duration", 0.0))
    file_size_mb = round(float(format_info.get("size", 0.0)) / (1024 * 1024), 2)

    video_streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "video"]
    audio_streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "audio"]

    v_stream = video_streams[0] if video_streams else {}
    a_stream = audio_streams[0] if audio_streams else {}

    v_codec = v_stream.get("codec_name", "unknown")
    v_width = v_stream.get("width", 0)
    v_height = v_stream.get("height", 0)
    v_fps = v_stream.get("r_frame_rate", "unknown")
    a_codec = a_stream.get("codec_name", "none")

    # Working dir for keyframes
    cache_dir = Path.home() / ".cache" / "video_analyzer" / vid_path.stem
    cache_dir.mkdir(parents=True, exist_ok=True)

    # 2. Keyframes
    frames = extract_keyframes(vid_path, cache_dir, ffmpeg_bin, duration, max_frames=args.max_frames)

    # 3. Storyboard
    sb_path = cache_dir / "video_storyboard.jpg"
    build_storyboard_contact_sheet(frames, sb_path)

    # 4. Transcription
    transcripts = []
    if not args.no_transcribe and not args.storyboard_only and audio_streams:
        print("Running speech transcription...", file=sys.stderr)
        transcripts = run_transcription(vid_path)

    # 5. Keyframe OCR
    ocr_results = {}
    if not args.no_ocr and not args.storyboard_only and tesseract_bin:
        print("Running keyframe OCR...", file=sys.stderr)
        for f in frames[:6]:  # OCR top sample frames
            txt = run_tesseract_ocr(f["path"], tesseract_bin)
            if txt:
                ocr_results[f["timecode"]] = txt

    # 6. Build Report
    lines = [
        f"# Video End-to-End Analysis: {vid_path.name}",
        "",
        f"- **Platform**: `{platform.system()}`",
        f"- **Duration**: `{format_time(duration)}` ({round(duration, 2)}s)",
        f"- **Resolution**: `{v_width} × {v_height}` | **FPS**: `{v_fps}`",
        f"- **Video Codec**: `{v_codec}` | **Audio Codec**: `{a_codec}`",
        f"- **File Size**: `{file_size_mb} MB`",
        "",
        "## 1. Visual Storyboard Contact Sheet (Single-Turn Grounding)",
        f"Inspect the complete visual timeline: [`video_storyboard.jpg`](file://{sb_path})",
        "",
        "## 2. Keyframe Timeline",
        "| Frame # | Timestamp | Image Link |",
        "| :--- | :--- | :--- |"
    ]

    for f in frames:
        p = Path(f["path"])
        lines.append(f"| {f['index']} | `{f['timecode']}` | [`{p.name}`](file://{f['path']}) |")
    lines.append("")

    if transcripts:
        lines.append("## 3. Timestamped Speech Audio Transcript")
        for t in transcripts:
            lines.append(f"- **{t['timestamp']}**: {t['text']}")
        lines.append("")

    if ocr_results:
        lines.append("## 4. Keyframe On-Screen OCR Text")
        for tc, text in ocr_results.items():
            lines.append(f"### At Timestamp `{tc}`")
            lines.append("```text")
            lines.append(text)
            lines.append("```")
        lines.append("")

    lines.append("---")
    lines.append("*Generated by Video End-to-End Analyzer for AI Agents.*")
    report = "\n".join(lines)

    if args.output:
        out_file = Path(args.output).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(report, encoding="utf-8")
        print(f"Report saved to: {out_file}")
    else:
        print(report)


if __name__ == "__main__":
    main()
