---
name: website-analyzer
description: Autonomous end-to-end website auditing and inspection suite for AI agents. Combines Google Chrome DevTools MCP, headless Chrome multi-viewport screenshot capture, Google Lighthouse Core Web Vitals auditing, WCAG accessibility validation, SEO/semantic hierarchy parsing, and runtime console/network error diagnostics.
---

# Website End-to-End Analyzer Skill for AI Agents

This skill provides an autonomous, end-to-end framework for analyzing, auditing, and inspecting any website or web application (local dev servers like `http://localhost:3000`, `http://localhost:5173`, or public URLs).

AI agents must never guess website responsiveness, UI rendering, Core Web Vitals performance, accessibility compliance, or console errors. This skill equips agents with a deterministic, multi-layer web auditing suite that combines automated multi-viewport visual captures with deep technical diagnostic telemetry.

---

## 1. When to Activate This Skill

Activate this skill immediately whenever:
- The user provides or asks to inspect a **Website URL** or **Web App** (`http://localhost:*`, staging, or production URL).
- The user asks to audit **Responsiveness & Mobile Layout** across different device viewports.
- The user asks to audit **Performance**, **Speed**, or **Core Web Vitals** (LCP, CLS, INP, FCP, TBT).
- The user asks to audit **Accessibility (A11y)**, WCAG contrast, or screen-reader usability.
- The user asks to audit **SEO**, meta tags, heading structures, or semantic HTML.
- The user asks to diagnose **Console Errors**, broken network calls, or JavaScript runtime crashes.

---

## 2. Integrated Tool Suite

| Engine | Technology | Primary Function |
| :--- | :--- | :--- |
| **Chrome DevTools MCP** | `chrome-devtools-mcp` | Interactive browser control, page navigation, DOM snapshots, script evaluation, and live console/network monitoring. |
| **Multi-Viewport Visual Engine** | Google Chrome Headless | Automated full-page screenshots at Desktop (1920×1080), Tablet (768×1024), and Mobile (375×812) viewports. |
| **Lighthouse Audit Engine** | Google Lighthouse 13.5 | Industry-standard scoring (0-100) for Performance, Accessibility, Best Practices, and SEO. |
| **Core Web Vitals Telemetry** | Chrome Performance / Lighthouse | Millisecond-accurate extraction of LCP, CLS, TBT, FCP, and Speed Index. |
| **DOM & SEO Inspector** | Automated DOM Parser | Validates title, meta description, OpenGraph tags, H1-H6 hierarchy, missing image alt tags, and interactive form elements. |

---

## 3. Mandatory Autonomous 5-Step Execution Protocol

When any website URL is provided or under review, the AI agent must execute this workflow:

```
[Target URL / Web App]
        │
        ├──► Step 1: Responsive Visual Capture (Multi-Viewport)
        │            Capture Desktop (1920px), Tablet (768px), and Mobile (375px) screenshots.
        │            Call view_file on captured screenshots for multimodal visual inspection.
        │
        ├──► Step 2: Core Web Vitals & Performance Audit
        │            Extract Lighthouse Performance score, LCP, CLS, TBT, and payload size.
        │
        ├──► Step 3: Accessibility (A11y) & WCAG Compliance Audit
        │            Audit color contrast ratios, touch targets, ARIA roles, and form labels.
        │
        ├──► Step 4: SEO, Meta Tags & Semantic Document Hierarchy
        │            Inspect title, meta description, OG tags, single H1 rule, and missing alt attributes.
        │
        └──► Step 5: Network Diagnostics & Console Runtime Errors
                     Detect failed requests (4xx/5xx), slow API responses, and uncaught JS errors.
```

### Step 1: Responsive Visual Capture & Multimodal Inspection
Run the website analyzer script:
```bash
node /Users/waffor/Desktop/Skills/website-analyzer/scripts/website_analyzer.mjs <url>
```
The script renders:
- `desktop_1920x1080.png`
- `tablet_768x1024.png`
- `mobile_375x812.png`

**MANDATORY**: Call `view_file` on the generated screenshots!
- Inspect desktop layout balance and grid structures.
- Verify mobile responsiveness: check for horizontal overflow, crushed flex containers, overlapping buttons, or unreadable small typography.

### Step 2: Core Web Vitals & Performance Audit
Review the audit metrics:
- **LCP (Largest Contentful Paint)**: Must be `< 2.5s` (Good). Over `4.0s` is Poor.
- **CLS (Cumulative Layout Shift)**: Must be `< 0.1` (Good). Over `0.25` is Poor.
- **TBT (Total Blocking Time)**: Must be `< 200ms`.
- **FCP (First Contentful Paint)**: Must be `< 1.8s`.

### Step 3: Accessibility (A11y) Audit
- Ensure text contrast meets WCAG AA (minimum 4.5:1 for normal text, 3:1 for large text).
- Check that all interactive inputs have associated `<label>` elements.
- Verify touch targets on mobile are at least 44×44px or 48×48px.
- Confirm all images possess meaningful `alt` attributes.

### Step 4: SEO & Semantic Hierarchy
- Verify exactly one `<h1>` tag exists on the page.
- Check heading progression (no skipping from `<h1>` to `<h3>`).
- Confirm `<title>` tag and `<meta name="description">` are descriptive and non-empty.
- Verify OpenGraph (`og:title`, `og:image`, `og:url`) tags for social sharing.

### Step 5: Network & Runtime Console Errors
- Verify all HTTP status codes are 200/304. Flag any 404, 500, or CORS errors.
- Inspect console logs for unhandled promise rejections, React warnings, or CSS layout errors.

---

## 4. Chrome DevTools MCP Tool Reference

When using the `chrome-devtools` MCP server for interactive workflows:

### Navigate to page
```json
{
  "ServerName": "chrome_devtools",
  "ToolName": "navigate_page",
  "Arguments": {
    "url": "http://localhost:5173"
  }
}
```

### Take Snapshot (DOM & Accessibility Tree)
```json
{
  "ServerName": "chrome_devtools",
  "ToolName": "take_snapshot",
  "Arguments": {}
}
```

### Capture Viewport Screenshot
```json
{
  "ServerName": "chrome_devtools",
  "ToolName": "take_screenshot",
  "Arguments": {
    "filePath": "/path/to/screenshot.png"
  }
}
```

---

## 5. CLI Utility Usage

The bundled CLI tool is located at `scripts/website_analyzer.mjs`:

```bash
# Full end-to-end audit (screenshots, Lighthouse, SEO, DOM, network)
node /Users/waffor/Desktop/Skills/website-analyzer/scripts/website_analyzer.mjs https://example.com

# Audit a local development server
node /Users/waffor/Desktop/Skills/website-analyzer/scripts/website_analyzer.mjs http://localhost:5173

# Screenshots only (fast visual capture across Desktop, Tablet, Mobile)
node /Users/waffor/Desktop/Skills/website-analyzer/scripts/website_analyzer.mjs https://example.com --screenshots-only

# Output report to specific folder
node /Users/waffor/Desktop/Skills/website-analyzer/scripts/website_analyzer.mjs https://example.com -o ./audit_report
```

---

## 6. Zero-Hallucination Quality Gate

Before providing any review or recommendations for a web application:
1. **Never guess rendering**: Inspect the actual multi-viewport screenshots via `view_file`.
2. **Never guess performance scores**: Always cite the exact Lighthouse and Core Web Vitals values.
3. **Never guess accessibility compliance**: Verify against the WCAG contrast and ARIA audit results.
4. **Always provide actionable fixes**: Reference the exact DOM elements or CSS classes that failed audit rules.
