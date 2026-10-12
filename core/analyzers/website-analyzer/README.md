# Website End-to-End Analyzer Suite

An enterprise website auditing and inspection toolkit for AI agents and human engineers. Provides deterministic, zero-hallucination web evaluation combining Chrome DevTools MCP, headless Chrome multi-viewport screenshot captures (Desktop, Tablet, Mobile), Google Lighthouse Core Web Vitals telemetry, WCAG accessibility validation, SEO/semantic hierarchy parsing, and runtime console/network error diagnostics.

---

## Architecture & Components

```
website-analyzer/
├── SKILL.md                  # Autonomous agent instructions, schemas & zero-hallucination rules
├── README.md                 # Complete toolkit overview and usage documentation
├── package.json              # NPM metadata & quick scripts
├── scripts/
│   └── website_analyzer.mjs  # Standalone CLI tool for multi-viewport screenshots, CWV & SEO audits
└── mcp/
    └── mcp_config.json       # MCP configuration for Chrome DevTools MCP
```

---

## Key Capabilities

1. **Multi-Viewport Responsive Visuals**: Automatically renders full-page screenshots at Desktop (1920×1080), Tablet (768×1024), and Mobile (375×812) viewports. The AI agent inspects these images via `view_file` to audit real visual layout, responsive collapsing, and typography.
2. **Core Web Vitals & Lighthouse Scores**: Integrates with Google Lighthouse 13.5 to extract numerical scores (0-100) for Performance, Accessibility, Best Practices, and SEO, plus exact millisecond metrics for LCP, CLS, TBT, and FCP.
3. **Accessibility (A11y) & WCAG Validation**: Audits missing image `alt` attributes, form `<label>` associations, color contrast, and touch target sizing.
4. **SEO & Semantic Hierarchy**: Validates `<title>`, meta description, OpenGraph tags, and strict single-`<h1>` heading hierarchy.
5. **Interactive Chrome DevTools MCP**: Allows live interactive browsing, clicks, DOM snapshots, JS execution, and performance tracing via `chrome-devtools-mcp`.

---

## Quick Start & CLI Usage

### 1. Full End-to-End Audit (Visuals + Lighthouse + SEO)
```bash
node core/analyzers/website-analyzer/scripts/website_analyzer.mjs https://example.com
```

### 2. Audit a Local Development Server
```bash
node core/analyzers/website-analyzer/scripts/website_analyzer.mjs http://localhost:5173
```

### 3. Responsive Screenshots Only (Fast Capture)
```bash
node core/analyzers/website-analyzer/scripts/website_analyzer.mjs https://example.com --screenshots-only
```

### 4. Output to Custom Directory
```bash
node core/analyzers/website-analyzer/scripts/website_analyzer.mjs https://example.com -o ./my_audit_folder
```

---

## MCP Server Integration

Add `mcp/mcp_config.json` to your AI client configuration:
- Tools provided by `chrome_devtools`: `navigate_page`, `take_snapshot`, `take_screenshot`, `evaluate_script`, `performance_trace`, `network_requests`.
