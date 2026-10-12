# Image End-to-End Analyzer Suite

An enterprise multimodal analysis toolkit for AI agents and human engineers. Provides deterministic, zero-hallucination image analysis combining visual token inspection, dimensional and EXIF telemetry, color palette extraction, Tesseract OCR, and document layout parsing via IBM Docling and Microsoft MarkItDown.

---

## Architecture & Components

```
image-analyzer/
├── SKILL.md                  # Autonomous agent instructions, schemas & zero-hallucination rules
├── README.md                 # Complete toolkit overview and usage documentation
├── scripts/
│   └── image_analyzer.py     # Standalone CLI tool for metadata, palette & OCR extraction
└── mcp/
    └── mcp_config.json       # MCP configuration for Claude Desktop, Antigravity, Gemini & Cursor
```

---

## Key Capabilities

1. **Native Multimodal Vision Grounding**: Direct inspection using `view_file` loads visual tokens into the AI model's context for spatial balance, UI aesthetics, and typography assessment.
2. **Deterministic Color Palettes**: Extracts top 5 dominant colors with exact HEX codes (`#RRGGBB`), RGB values, coverage percentage, and relative luminance assessment (Light/Dark tone).
3. **High-Precision Local OCR**: Uses local Tesseract OCR to extract exact text, button labels, numbers, and code snippets without hallucination.
4. **Deep Document & Table Parsing**: Integrates with IBM Docling MCP and Microsoft MarkItDown MCP to recover multi-column layouts and export complex nested/borderless tables into clean Markdown.
5. **Vector & Multi-Page PDF Support**: Renders 300 DPI high-resolution page previews with Poppler (`pdftoppm`).

---

## Quick Start & CLI Usage

### 1. Run Complete Image Analysis
```bash
python3 core/analyzers/image-analyzer/scripts/image_analyzer.py /path/to/image.png
```

### 2. Extract Color Palette Only
```bash
python3 core/analyzers/image-analyzer/scripts/image_analyzer.py /path/to/image.png --palette-only
```

### 3. Output as JSON or Export to File
```bash
python3 core/analyzers/image-analyzer/scripts/image_analyzer.py /path/to/image.png --json
python3 core/analyzers/image-analyzer/scripts/image_analyzer.py /path/to/image.png -o /path/to/report.md
```

---

## MCP Server Integration

Add the contents of `mcp/mcp_config.json` to your AI agent client (Antigravity IDE, Claude Desktop, or Cursor):
- `media_deep_analyzer`: Image telemetry, color extraction, and OCR.
- `docling`: Document table extraction, reading order reconstruction, and layout parsing.
- `markitdown`: Fast text conversion and metadata extraction.
