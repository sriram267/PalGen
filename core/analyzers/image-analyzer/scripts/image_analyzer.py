#!/usr/bin/env python3
"""
Image End-to-End Analyzer CLI for AI Agents
Cross-Platform: Windows, macOS, and Linux
Extracts comprehensive visual telemetry, EXIF data, dominant HEX/RGB palettes,
and Tesseract OCR text from image files.
"""

import os
import sys
import json
import shutil
import argparse
import platform
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional


def find_binary(name: str) -> Optional[str]:
    """Find binary executable across Windows, macOS, and Linux."""
    # 1. Standard PATH check
    found = shutil.which(name)
    if found:
        return found
    if platform.system() == "Windows":
        found = shutil.which(f"{name}.exe")
        if found:
            return found

    # 2. Well-known OS specific paths
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

        if name == "tesseract":
            candidates = [
                os.path.join(prog_files, "Tesseract-OCR", "tesseract.exe"),
                os.path.join(prog_files_x86, "Tesseract-OCR", "tesseract.exe"),
                os.path.join(local_app, "Programs", "Tesseract-OCR", "tesseract.exe"),
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


# Auto re-exec with uv if Pillow is not installed
try:
    from PIL import Image, ExifTags
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


def get_image_metadata(img: Image.Image, file_path: Path) -> Dict[str, Any]:
    """Extract file telemetry and EXIF metadata."""
    width, height = img.size
    aspect_ratio = round(width / height, 3) if height > 0 else 0
    file_size_kb = round(file_path.stat().st_size / 1024, 2)

    exif_data = {}
    if hasattr(img, "_getexif") and img._getexif():
        raw_exif = img._getexif()
        if raw_exif:
            for tag_id, value in raw_exif.items():
                tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                if isinstance(value, (str, int, float)):
                    exif_data[tag_name] = value

    return {
        "file_name": file_path.name,
        "format": img.format or file_path.suffix.upper().replace(".", ""),
        "mode": img.mode,
        "width": width,
        "height": height,
        "aspect_ratio": f"{aspect_ratio}:1 ({width}x{height})",
        "file_size_kb": file_size_kb,
        "os_platform": platform.system(),
        "exif": exif_data
    }


def extract_dominant_palette(img: Image.Image, num_colors: int = 5) -> List[Dict[str, Any]]:
    """Quantize image colors and extract dominant HEX & RGB values."""
    rgb_img = img.convert("RGB")
    thumb = rgb_img.resize((150, 150))
    quantized = thumb.quantize(colors=num_colors)
    palette_raw = quantized.getpalette()[: num_colors * 3]
    color_counts = quantized.getcolors()

    if not color_counts:
        return []

    color_counts.sort(key=lambda x: x[0], reverse=True)
    total_pixels = sum(count for count, _ in color_counts)

    palette_list = []
    for count, idx in color_counts:
        r = palette_raw[idx * 3]
        g = palette_raw[idx * 3 + 1]
        b = palette_raw[idx * 3 + 2]
        hex_code = f"#{r:02x}{g:02x}{b:02x}".upper()
        pct = round((count / total_pixels) * 100, 1)

        luminance = round(0.2126 * r + 0.7152 * g + 0.0722 * b, 1)
        is_dark = luminance < 128

        palette_list.append({
            "hex": hex_code,
            "rgb": [r, g, b],
            "percentage": pct,
            "luminance": luminance,
            "tone": "Dark" if is_dark else "Light"
        })

    return palette_list


def run_tesseract_ocr(file_path: Path) -> str:
    """Run local Tesseract OCR on the target image cross-platform."""
    tesseract_bin = find_binary("tesseract")
    if not tesseract_bin:
        return "[Tesseract binary not found on PATH or standard install locations]"

    try:
        res = subprocess.run(
            [tesseract_bin, str(file_path), "stdout", "--oem", "1"],
            capture_output=True,
            text=True,
            check=True
        )
        text = res.stdout.strip()
        return text if text else "[No text detected by OCR]"
    except Exception as e:
        return f"[OCR Error: {str(e)}]"


def generate_markdown_report(metadata: Dict[str, Any], palette: List[Dict[str, Any]], ocr_text: str) -> str:
    """Format structured analysis into a clean Markdown report for AI agents."""
    lines = [
        f"# End-to-End Image Analysis Report: {metadata['file_name']}",
        "",
        "## 1. Visual & Dimensional Telemetry",
        f"- **Platform**: `{metadata['os_platform']}`",
        f"- **Dimensions**: `{metadata['width']} × {metadata['height']} px`",
        f"- **Aspect Ratio**: `{metadata['aspect_ratio']}`",
        f"- **Format & Color Mode**: `{metadata['format']}` / `{metadata['mode']}`",
        f"- **File Size**: `{metadata['file_size_kb']} KB`",
        ""
    ]

    if metadata["exif"]:
        lines.append("### EXIF Metadata")
        for k, v in list(metadata["exif"].items())[:8]:
            lines.append(f"- **{k}**: `{v}`")
        lines.append("")

    lines.append("## 2. Dominant Color Palette (HEX & RGB)")
    lines.append("| Swatch | HEX | RGB | % Coverage | Tone |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    for c in palette:
        lines.append(f"| `{c['hex']}` | `{c['hex']}` | `rgb({c['rgb'][0]}, {c['rgb'][1]}, {c['rgb'][2]})` | {c['percentage']}% | {c['tone']} |")
    lines.append("")

    lines.append("## 3. High-Precision OCR Extracted Text")
    lines.append("```text")
    lines.append(ocr_text)
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("*Generated by Image End-to-End Analyzer for AI Agents.*")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Image End-to-End Analyzer for AI Agents (Cross-Platform)")
    parser.add_argument("image_path", help="Path to image file (PNG, JPG, WebP, SVG, etc.)")
    parser.add_argument("--no-ocr", action="store_true", help="Skip Tesseract OCR")
    parser.add_argument("--palette-only", action="store_true", help="Only extract color palette")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of Markdown")
    parser.add_argument("-o", "--output", help="Write report to specified output path")

    args = parser.parse_args()
    img_path = Path(args.image_path).resolve()

    if not img_path.exists():
        print(f"Error: Image path does not exist: {img_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with Image.open(img_path) as img:
            metadata = get_image_metadata(img, img_path)
            palette = extract_dominant_palette(img)
    except Exception as e:
        print(f"Error reading image: {e}", file=sys.stderr)
        sys.exit(1)

    ocr_text = "" if args.no_ocr or args.palette_only else run_tesseract_ocr(img_path)

    if args.json:
        data = {
            "metadata": metadata,
            "palette": palette,
            "ocr_text": ocr_text
        }
        output_str = json.dumps(data, indent=2)
    else:
        output_str = generate_markdown_report(metadata, palette, ocr_text)

    if args.output:
        out_file = Path(args.output).resolve()
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(output_str, encoding="utf-8")
        print(f"Analysis saved to: {out_file}")
    else:
        print(output_str)


if __name__ == "__main__":
    main()
