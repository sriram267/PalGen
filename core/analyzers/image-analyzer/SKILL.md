---
name: image-analyzer
description: Comprehensive end-to-end image and document analysis engine for AI agents. Integrates high-resolution multimodal vision inspection, EXIF & dimensional telemetry, dominant color palette extraction (HEX/RGB), Tesseract OCR, Poppler vector rendering, and IBM Docling / Microsoft MarkItDown structural layout & table reconstruction.
---

# Image End-to-End Analyzer Skill for AI Agents

This skill provides an autonomous, end-to-end framework for analyzing any image, graphic, diagram, screenshot, or document file (`.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`, `.tiff`, `.heic`, `.pdf`).

AI agents must never guess image dimensions, color palettes, on-screen text, chart values, or table layouts. This skill equips agents with a deterministic, multi-layer extraction pipeline that guarantees zero hallucination, spatial grounding, and multimodal precision.

---

## 1. When to Activate This Skill

Activate this skill immediately whenever:
- The user provides, references, or links an **Image** (`.png`, `.jpg`, `.webp`, `.svg`, `.heic`, `.tiff`).
- The user provides a **UI Screenshot**, mock, wireframe, or design specification.
- The user provides an **Infographic**, chart, diagram, or architecture schematic.
- The user provides a **Scanned Document** or PDF page requiring OCR or table extraction.
- The user asks to audit visual aesthetics, extract color schemes, read fine text, or extract tables from graphics.

---

## 2. Integrated Tool Suite

The Image End-to-End Analyzer unifies 4 top-tier technologies:

| Engine | Primary Function | Ideal Use Cases |
| :--- | :--- | :--- |
| **Media Deep Analyzer (Image Engine)** | EXIF metadata, dimension telemetry, dominant HEX/RGB palette extraction, and local Tesseract OCR. | UI screenshots, photographs, color audits, quick OCR. |
| **IBM Docling** | Advanced layout recovery, multi-column reading order reconstruction, and complex table-to-markdown extraction. | Invoices, financial reports, multi-column articles, dense tabular images. |
| **Microsoft MarkItDown** | Fast multi-format text & metadata extraction with automated OCR. | Quick markdown conversions of images and slides. |
| **Poppler & Tesseract** | Direct 300 DPI vector rendering (`pdftoppm`), spatial text layout (`pdftotext -layout`), and embedded raster extraction (`pdfimages`). | High-precision vector graphics, PDFs, fine-detail typography. |

---

## 3. Mandatory Autonomous Execution Protocol

When any image file is encountered, the AI agent must execute this 4-step pipeline:

```
[Input Image / Asset]
        │
        ├──► Step 1: Direct Multimodal Vision Inspection (view_file)
        │            Load native visual tokens into model context for aesthetics & layout.
        │
        ├──► Step 2: Deep Metadata & Color Palette Extraction
        │            Get exact dimensions, aspect ratio, EXIF, and dominant HEX/RGB palette.
        │
        ├──► Step 3: High-Precision OCR & Text Extraction
        │            Run Tesseract OCR for 100% exact character strings without guessing.
        │
        └──► Step 4: Structural Document & Table Parsing (if tabular/document)
                     Run IBM Docling / MarkItDown for nested tables and reading order.
```

### Step 1: Direct Multimodal Vision Inspection
Always invoke `view_file` on the target image path. This directly injects native vision tokens into context:
- Observe visual hierarchy, margins, whitespace, balance, typography hierarchy, and UI state.
- Form an immediate holistic understanding of the visual content.

### Step 2: Deep Metadata & Palette Extraction
Invoke the `media_deep_analyzer` MCP tool `deep_analyze_image` or run the CLI:
```bash
python3 core/analyzers/image-analyzer/scripts/image_analyzer.py <path-to-image> --palette
```
- **Dimensions**: Exact width × height, aspect ratio, color mode (RGBA/RGB/CMYK).
- **Dominant Palette**: Top 5 HEX codes and RGB tuples with coverage percentage and perceived luminance.
- **EXIF Data**: Timestamp, camera/device specs, GPS (if present), software used.

### Step 3: High-Precision OCR & Text Extraction
Never transcribe text from memory or rough vision guesses. Use Tesseract OCR:
```bash
python3 core/analyzers/image-analyzer/scripts/image_analyzer.py <path-to-image> --ocr
```
- Extracts exact label names, button text, error messages, code snippets, and numbers.
- Prevents typos and hallucinations on small fonts or subtle UI labels.

### Step 4: Complex Table & Layout Parsing (Docling & MarkItDown)
For dense documents, receipts, invoices, or multi-column slides:
- Use IBM Docling MCP `convert_document_into_docling_document` followed by `export_docling_document_to_markdown`.
- Use Microsoft MarkItDown MCP `convert_to_markdown` for quick textual extraction.

---

## 4. MCP Tool Reference

### `media_deep_analyzer:deep_analyze_image`
```json
{
  "ServerName": "media_deep_analyzer",
  "ToolName": "deep_analyze_image",
  "Arguments": {
    "image_path": "/absolute/path/to/image.png",
    "perform_ocr": true,
    "extract_palette": true
  }
}
```

### `docling:convert_document_into_docling_document`
```json
{
  "ServerName": "docling",
  "ToolName": "convert_document_into_docling_document",
  "Arguments": {
    "source": "/absolute/path/to/document_or_image.pdf"
  }
}
```

### `markitdown:convert_to_markdown`
```json
{
  "ServerName": "markitdown",
  "ToolName": "convert_to_markdown",
  "Arguments": {
    "uri": "/absolute/path/to/image.png"
  }
}
```

---

## 5. CLI Utility Usage

The bundled CLI tool is located at `scripts/image_analyzer.py`:

```bash
# Full analysis (metadata, palette, OCR)
python3 core/analyzers/image-analyzer/scripts/image_analyzer.py /path/to/image.png

# Extract only palette
python3 core/analyzers/image-analyzer/scripts/image_analyzer.py /path/to/image.png --palette-only

# Save analysis to markdown report
python3 core/analyzers/image-analyzer/scripts/image_analyzer.py /path/to/image.png -o /path/to/report.md
```

---

## 6. Zero-Hallucination Quality Gate

Before providing any final answer, code, or design feedback:
1. **Dimensions**: Verify exact width and height from telemetry.
2. **Colors**: Use the exact extracted HEX values, never arbitrary approximated color names.
3. **Labels & Text**: Ensure all strings match the OCR output word-for-word.
4. **Tables**: Verify row and column alignment using Docling Markdown output.
