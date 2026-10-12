#!/usr/bin/env python3
"""
Universal Multimodal End-to-End Analyzer CLI
Single Entry Point for Image, Video, and Website Analysis.
Works seamlessly across Windows, macOS, and Linux.
"""

import os
import sys
import shutil
import argparse
import platform
import subprocess
from pathlib import Path

CORE_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_ROOT = CORE_DIR.parent
IMAGE_SCRIPT = CORE_DIR / "analyzers" / "image-analyzer" / "scripts" / "image_analyzer.py"
VIDEO_SCRIPT = CORE_DIR / "analyzers" / "video-analyzer" / "scripts" / "video_analyzer.py"
WEBSITE_SCRIPT = CORE_DIR / "analyzers" / "website-analyzer" / "scripts" / "website_analyzer.mjs"
ROUTER_SCRIPT = WORKSPACE_ROOT / "master-skiller" / "scripts" / "router.py"



def find_binary(name: str):
    """Find binary across Windows, macOS, Linux."""
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
        candidates = [f"/opt/homebrew/bin/{name}", f"/usr/local/bin/{name}", f"/usr/bin/{name}"]
    elif system == "Windows":
        prog = os.environ.get("ProgramFiles", "C:\\Program Files")
        prog_x86 = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
        local = os.environ.get("LOCALAPPDATA", "")
        if name in ("ffmpeg", "ffprobe"):
            candidates = [f"C:\\ffmpeg\\bin\\{name}.exe", os.path.join(prog, "ffmpeg", "bin", f"{name}.exe")]
        elif name == "tesseract":
            candidates = [os.path.join(prog, "Tesseract-OCR", "tesseract.exe")]
        elif name == "uv":
            candidates = [os.path.join(local, "uv", "uv.exe")]
    else:
        candidates = [f"/usr/bin/{name}", f"/usr/local/bin/{name}"]

    for c in candidates:
        if c and Path(c).exists():
            return c
    return None


def run_doctor():
    """System health check and diagnostic tool."""
    print("=" * 60)
    print("  Multimodal Analyzer Suite — System Environment Doctor")
    print("=" * 60)
    print(f"  Operating System : {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"  Python Version   : {sys.version.split()[0]} ({sys.executable})")
    print("-" * 60)

    checks = [
        ("node", "Node.js (for Website Analyzer)", "winget install OpenJS.NodeJS", "brew install node", "sudo apt install nodejs npm"),
        ("uv", "uv Python Manager (Fast deps)", "winget install astral-sh.uv", "brew install uv", "curl -LsSf https://astral.sh/uv/install.sh | sh"),
        ("ffmpeg", "FFmpeg (for Video Telemetry)", "winget install Gyan.FFmpeg", "brew install ffmpeg", "sudo apt install ffmpeg"),
        ("ffprobe", "FFprobe (for Video Streams)", "winget install Gyan.FFmpeg", "brew install ffmpeg", "sudo apt install ffmpeg"),
        ("tesseract", "Tesseract OCR (for On-Screen Text)", "winget install UB-Mannheim.TesseractOCR", "brew install tesseract", "sudo apt install tesseract-ocr"),
    ]

    all_ok = True
    for bin_name, desc, win_fix, mac_fix, linux_fix in checks:
        bin_path = find_binary(bin_name)
        if bin_path:
            print(f"  ✅ {desc:<35} : Found ({bin_path})")
        else:
            all_ok = False
            print(f"  ⚠️  {desc:<35} : NOT FOUND")
            if platform.system() == "Windows":
                print(f"      Install via: {win_fix}")
            elif platform.system() == "Darwin":
                print(f"      Install via: {mac_fix}")
            else:
                print(f"      Install via: {linux_fix}")

    # Check Chrome
    chrome_found = False
    if platform.system() == "Darwin":
        chrome_found = Path("/Applications/Google Chrome.app").exists()
    elif platform.system() == "Windows":
        prog = os.environ.get("ProgramFiles", "C:\\Program Files")
        local = os.environ.get("LOCALAPPDATA", "")
        chrome_found = any(Path(p).exists() for p in [
            os.path.join(prog, "Google", "Chrome", "Application", "chrome.exe"),
            os.path.join(local, "Google", "Chrome", "Application", "chrome.exe")
        ])
    else:
        chrome_found = bool(find_binary("google-chrome") or find_binary("chromium"))

    if chrome_found:
        print(f"  ✅ {'Google Chrome (for Web Visuals)':<35} : Installed")
    else:
        print(f"  ⚠️  {'Google Chrome (for Web Visuals)':<35} : Not detected in standard location")

    print("=" * 60)
    if all_ok:
        print("  🎉 All core binaries are verified! The suite is ready to run.")
    else:
        print("  💡 Tip: Run the install commands above for any missing tools.")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Universal Multimodal End-to-End Analyzer Suite (Cross-Platform)"
    )
    subparsers = parser.add_subparsers(dest="command", help="Target analysis domain")

    # Image parser
    img_p = subparsers.add_parser("image", help="Analyze an image or document (PNG, JPG, WebP, PDF)")
    img_p.add_argument("path", help="Path to image file")
    img_p.add_argument("--palette-only", action="store_true", help="Extract color palette only")
    img_p.add_argument("--no-ocr", action="store_true", help="Skip Tesseract OCR")
    img_p.add_argument("--json", action="store_true", help="Output JSON format")
    img_p.add_argument("-o", "--output", help="Save report to file")

    # Video parser
    vid_p = subparsers.add_parser("video", help="Analyze a video file (.mp4, .mov, .mkv, .webm)")
    vid_p.add_argument("path", help="Path to video file")
    vid_p.add_argument("--max-frames", type=int, default=16, help="Max keyframes (default: 16)")
    vid_p.add_argument("--storyboard-only", action="store_true", help="Only build storyboard contact sheet")
    vid_p.add_argument("--no-transcribe", action="store_true", help="Skip speech audio transcription")
    vid_p.add_argument("--no-ocr", action="store_true", help="Skip keyframe OCR")
    vid_p.add_argument("-o", "--output", help="Save report to file")

    # Website parser
    web_p = subparsers.add_parser("website", help="Analyze a website or dev server URL (e.g. localhost:5173)")
    web_p.add_argument("url", help="Target website URL")
    web_p.add_argument("--screenshots-only", action="store_true", help="Capture Desktop, Tablet, Mobile shots only")
    web_p.add_argument("--skip-lighthouse", action="store_true", help="Skip Lighthouse audit")
    web_p.add_argument("-o", "--output", help="Output directory")

    # Route parser (Master Skiller)
    route_p = subparsers.add_parser("route", help="Master Skiller: query skills and generate execution pipelines")
    route_p.add_argument("query", nargs="*", help="Task prompt or query")
    route_p.add_argument("--top", type=int, default=5, help="Number of top skills (default: 5)")
    route_p.add_argument("--domain", help="Filter by specific domain")
    route_p.add_argument("--json", action="store_true", help="Output JSON format")
    route_p.add_argument("--list-domains", action="store_true", help="List all indexed domains")

    # Doctor parser
    subparsers.add_parser("doctor", help="Run system environment diagnostics")

    args, unknown = parser.parse_known_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "doctor":
        run_doctor()
        return

    if args.command == "route":
        cmd = [sys.executable, str(ROUTER_SCRIPT)]
        if args.list_domains:
            cmd.append("--list-domains")
        if args.top != 5:
            cmd.extend(["--top", str(args.top)])
        if args.domain:
            cmd.extend(["--domain", args.domain])
        if args.json:
            cmd.append("--json")
        if args.query:
            cmd.extend(args.query)
        subprocess.run(cmd)

    elif args.command == "image":
        cmd = [sys.executable, str(IMAGE_SCRIPT), args.path]
        if args.palette_only:
            cmd.append("--palette-only")
        if args.no_ocr:
            cmd.append("--no-ocr")
        if args.json:
            cmd.append("--json")
        if args.output:
            cmd.extend(["-o", args.output])
        subprocess.run(cmd)

    elif args.command == "video":
        cmd = [sys.executable, str(VIDEO_SCRIPT), args.path]
        if args.max_frames != 16:
            cmd.extend(["--max-frames", str(args.max_frames)])
        if args.storyboard_only:
            cmd.append("--storyboard-only")
        if args.no_transcribe:
            cmd.append("--no-transcribe")
        if args.no_ocr:
            cmd.append("--no-ocr")
        if args.output:
            cmd.extend(["-o", args.output])
        subprocess.run(cmd)

    elif args.command == "website":
        node_bin = find_binary("node") or "node"
        cmd = [node_bin, str(WEBSITE_SCRIPT), args.url]
        if args.screenshots_only:
            cmd.append("--screenshots-only")
        if args.skip_lighthouse:
            cmd.append("--skip-lighthouse")
        if args.output:
            cmd.extend(["-o", args.output])
        subprocess.run(cmd)



if __name__ == "__main__":
    main()
