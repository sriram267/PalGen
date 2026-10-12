#!/usr/bin/env node
/**
 * Website End-to-End Analyzer CLI for AI Agents
 * Performs multi-viewport responsive screenshot captures (Desktop, Tablet, Mobile),
 * Core Web Vitals & Lighthouse auditing, SEO & semantic HTML analysis, and network health checks.
 */

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { execSync, spawnSync } from 'node:child_process';

function getChromePath() {
  if (process.env.CHROME_PATH && fs.existsSync(process.env.CHROME_PATH)) {
    return process.env.CHROME_PATH;
  }

  const platform = os.platform();
  const candidates = [];

  if (platform === 'darwin') {
    candidates.push(
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      '/Applications/Chromium.app/Contents/MacOS/Chromium',
      '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
    );
  } else if (platform === 'win32') {
    const progFiles = process.env.ProgramFiles || 'C:\\Program Files';
    const progFilesX86 = process.env['ProgramFiles(x86)'] || 'C:\\Program Files (x86)';
    const localApp = process.env.LOCALAPPDATA || '';

    candidates.push(
      path.join(progFiles, 'Google', 'Chrome', 'Application', 'chrome.exe'),
      path.join(progFilesX86, 'Google', 'Chrome', 'Application', 'chrome.exe'),
      path.join(localApp, 'Google', 'Chrome', 'Application', 'chrome.exe'),
      path.join(progFilesX86, 'Microsoft', 'Edge', 'Application', 'msedge.exe'),
      path.join(progFiles, 'Microsoft', 'Edge', 'Application', 'msedge.exe')
    );
  } else {
    // Linux
    candidates.push(
      '/usr/bin/google-chrome',
      '/usr/bin/google-chrome-stable',
      '/usr/bin/chromium-browser',
      '/usr/bin/chromium'
    );
  }

  for (const c of candidates) {
    if (c && fs.existsSync(c)) {
      return c;
    }
  }

  // Try finding via which / where
  try {
    const lookupCmd = platform === 'win32' ? 'where chrome.exe' : 'which google-chrome || which chromium';
    const found = execSync(lookupCmd, { stdio: 'pipe' }).toString().trim().split('\n')[0];
    if (found && fs.existsSync(found)) {
      return found;
    }
  } catch {}

  return null;
}

const CHROME_PATH = getChromePath();

function printHelp() {
  console.log(`
Website End-to-End Analyzer for AI Agents

Usage:
  node website_analyzer.mjs <url> [options]

Options:
  --screenshots-only   Only capture multi-viewport screenshots
  --skip-lighthouse    Skip Google Lighthouse audit
  -o, --output <dir>   Output directory (default: ./website_analysis_<timestamp>)
  --help               Show this help message
`);
}

function captureScreenshot(url, outputPath, width, height) {
  if (!fs.existsSync(CHROME_PATH)) {
    console.error(`Chrome binary not found at ${CHROME_PATH}`);
    return false;
  }

  const args = [
    '--headless=new',
    '--disable-gpu',
    '--hide-scrollbars',
    `--window-size=${width},${height}`,
    `--screenshot=${outputPath}`,
    url
  ];

  try {
    spawnSync(CHROME_PATH, args, { stdio: 'pipe', timeout: 30000 });
    return fs.existsSync(outputPath);
  } catch (err) {
    console.error(`Failed to capture screenshot for ${width}x${height}:`, err.message);
    return false;
  }
}

async function analyzeDomAndSeo(url) {
  try {
    const res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36' } });
    const status = res.status;
    const html = await res.text();

    const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
    const title = titleMatch ? titleMatch[1].trim() : null;

    const descMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']*)["']/i) ||
                      html.match(/<meta[^>]*content=["']([^"']*)["'][^>]*name=["']description["']/i);
    const metaDescription = descMatch ? descMatch[1].trim() : null;

    const ogTitleMatch = html.match(/<meta[^>]*property=["']og:title["'][^>]*content=["']([^"']*)["']/i);
    const ogTitle = ogTitleMatch ? ogTitleMatch[1].trim() : null;

    const ogDescMatch = html.match(/<meta[^>]*property=["']og:description["'][^>]*content=["']([^"']*)["']/i);
    const ogDescription = ogDescMatch ? ogDescMatch[1].trim() : null;

    const h1Matches = [...html.matchAll(/<h1[^>]*>([\s\S]*?)<\/h1>/gi)].map(m => m[1].replace(/<[^>]+>/g, '').trim());
    const h2Count = (html.match(/<h2[^>]*>/gi) || []).length;
    const h3Count = (html.match(/<h3[^>]*>/gi) || []).length;

    const imgMatches = [...html.matchAll(/<img([^>]+)>/gi)];
    let imgsMissingAlt = 0;
    for (const m of imgMatches) {
      if (!/alt=["'][^"']*["']/i.test(m[1])) {
        imgsMissingAlt++;
      }
    }

    const buttonCount = (html.match(/<button[^>]*>/gi) || []).length;
    const inputCount = (html.match(/<input[^>]*>/gi) || []).length;
    const formCount = (html.match(/<form[^>]*>/gi) || []).length;
    const linkCount = (html.match(/<a\s+[^>]*href=/gi) || []).length;

    return {
      status,
      title,
      metaDescription,
      ogTitle,
      ogDescription,
      h1List: h1Matches,
      h2Count,
      h3Count,
      totalImages: imgMatches.length,
      imgsMissingAlt,
      buttonCount,
      inputCount,
      formCount,
      linkCount
    };
  } catch (err) {
    return { error: `Failed to fetch HTML: ${err.message}` };
  }
}

function runLighthouseAudit(url, outputDir) {
  const jsonPath = path.join(outputDir, 'lighthouse_report.json');
  console.error('Running Google Lighthouse Core Web Vitals audit (this takes ~15-20s)...');

  const cmd = `npx -y lighthouse "${url}" --output=json --output-path="${jsonPath}" --chrome-flags="--headless=new" --quiet --max-wait-for-load=30000`;
  try {
    execSync(cmd, { stdio: 'pipe', timeout: 60000 });
    if (fs.existsSync(jsonPath)) {
      const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
      const cats = data.categories || {};
      const audits = data.audits || {};

      return {
        scores: {
          performance: cats.performance ? Math.round(cats.performance.score * 100) : null,
          accessibility: cats.accessibility ? Math.round(cats.accessibility.score * 100) : null,
          bestPractices: cats['best-practices'] ? Math.round(cats['best-practices'].score * 100) : null,
          seo: cats.seo ? Math.round(cats.seo.score * 100) : null,
        },
        metrics: {
          lcp: audits['largest-contentful-paint'] ? audits['largest-contentful-paint'].displayValue : 'N/A',
          cls: audits['cumulative-layout-shift'] ? audits['cumulative-layout-shift'].displayValue : 'N/A',
          tbt: audits['total-blocking-time'] ? audits['total-blocking-time'].displayValue : 'N/A',
          fcp: audits['first-contentful-paint'] ? audits['first-contentful-paint'].displayValue : 'N/A',
          speedIndex: audits['speed-index'] ? audits['speed-index'].displayValue : 'N/A',
        }
      };
    }
  } catch (err) {
    console.error('Lighthouse audit skipped or error:', err.message);
  }
  return null;
}

function generateMarkdownReport(url, outputDir, screenshots, domData, lighthouseData) {
  const lines = [
    `# Website End-to-End Analysis Report`,
    ``,
    `- **Target URL**: \`${url}\``,
    `- **Generated At**: \`${new Date().toISOString()}\``,
    `- **Artifacts Directory**: \`${outputDir}\``,
    ``,
    `---`,
    ``,
    `## 1. Multi-Viewport Responsive Visuals`,
    `Inspect the captured high-resolution screenshots with \`view_file\` for visual validation:`,
    ``
  ];

  if (screenshots.desktop) {
    lines.push(`- **Desktop (1920×1080)**: [\`${path.basename(screenshots.desktop)}\`](file://${screenshots.desktop})`);
  }
  if (screenshots.tablet) {
    lines.push(`- **Tablet (768×1024)**: [\`${path.basename(screenshots.tablet)}\`](file://${screenshots.tablet})`);
  }
  if (screenshots.mobile) {
    lines.push(`- **Mobile (375×812)**: [\`${path.basename(screenshots.mobile)}\`](file://${screenshots.mobile})`);
  }
  lines.push(``);

  if (lighthouseData) {
    lines.push(`## 2. Core Web Vitals & Lighthouse Scores`);
    lines.push(``);
    lines.push(`| Category | Score | Rating |`);
    lines.push(`| :--- | :--- | :--- |`);
    const rate = (s) => (s >= 90 ? '🟢 Excellent' : s >= 50 ? '🟡 Needs Improvement' : '🔴 Poor');
    lines.push(`| **Performance** | **${lighthouseData.scores.performance ?? 'N/A'}/100** | ${rate(lighthouseData.scores.performance || 0)} |`);
    lines.push(`| **Accessibility** | **${lighthouseData.scores.accessibility ?? 'N/A'}/100** | ${rate(lighthouseData.scores.accessibility || 0)} |`);
    lines.push(`| **Best Practices** | **${lighthouseData.scores.bestPractices ?? 'N/A'}/100** | ${rate(lighthouseData.scores.bestPractices || 0)} |`);
    lines.push(`| **SEO** | **${lighthouseData.scores.seo ?? 'N/A'}/100** | ${rate(lighthouseData.scores.seo || 0)} |`);
    lines.push(``);

    lines.push(`### Core Web Vitals Metrics`);
    lines.push(`- **Largest Contentful Paint (LCP)**: \`${lighthouseData.metrics.lcp}\``);
    lines.push(`- **Cumulative Layout Shift (CLS)**: \`${lighthouseData.metrics.cls}\``);
    lines.push(`- **Total Blocking Time (TBT)**: \`${lighthouseData.metrics.tbt}\``);
    lines.push(`- **First Contentful Paint (FCP)**: \`${lighthouseData.metrics.fcp}\``);
    lines.push(`- **Speed Index**: \`${lighthouseData.metrics.speedIndex}\``);
    lines.push(``);
  }

  if (domData && !domData.error) {
    lines.push(`## 3. SEO & Semantic HTML Audit`);
    lines.push(`- **HTTP Response Status**: \`${domData.status}\``);
    lines.push(`- **Page Title**: ${domData.title ? `\`${domData.title}\`` : '⚠️ *Missing <title> tag*'}`);
    lines.push(`- **Meta Description**: ${domData.metaDescription ? `\`${domData.metaDescription}\`` : '⚠️ *Missing meta description*'}`);
    lines.push(`- **OpenGraph Title**: ${domData.ogTitle ? `\`${domData.ogTitle}\`` : '*Not defined*'}`);
    lines.push(``);

    lines.push(`### Heading Structure`);
    if (domData.h1List.length === 1) {
      lines.push(`- **H1 Heading**: ✅ Exactly one H1 present: \`"${domData.h1List[0]}"\``);
    } else if (domData.h1List.length === 0) {
      lines.push(`- **H1 Heading**: 🔴 *No H1 tag detected on page!*`);
    } else {
      lines.push(`- **H1 Heading**: ⚠️ *Multiple H1 tags detected (${domData.h1List.length}):*`);
      domData.h1List.forEach(h => lines.push(`  - \`"${h}"\``));
    }
    lines.push(`- **H2 Count**: \`${domData.h2Count}\` | **H3 Count**: \`${domData.h3Count}\``);
    lines.push(``);

    lines.push(`### Accessibility & DOM Elements`);
    if (domData.imgsMissingAlt > 0) {
      lines.push(`- **Image Alt Tags**: ⚠️ \`${domData.imgsMissingAlt} / ${domData.totalImages}\` images missing \`alt\` attributes.`);
    } else {
      lines.push(`- **Image Alt Tags**: ✅ All \`${domData.totalImages}\` images have \`alt\` attributes.`);
    }
    lines.push(`- **Interactive Elements**: \`${domData.buttonCount}\` buttons, \`${domData.inputCount}\` input fields, \`${domData.formCount}\` forms, \`${domData.linkCount}\` links.`);
    lines.push(``);
  }

  lines.push(`---`);
  lines.push(`*Generated by Website End-to-End Analyzer for AI Agents.*`);
  return lines.join('\n');
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0 || args.includes('--help')) {
    printHelp();
    process.exit(0);
  }

  const url = args[0];
  const screenshotsOnly = args.includes('--screenshots-only');
  const skipLighthouse = args.includes('--skip-lighthouse') || screenshotsOnly;

  let outputDir = null;
  const outIdx = args.findIndex(a => a === '-o' || a === '--output');
  if (outIdx !== -1 && args[outIdx + 1]) {
    outputDir = path.resolve(args[outIdx + 1]);
  } else {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    outputDir = path.resolve(`/tmp/website_analysis_${timestamp}`);
  }

  fs.mkdirSync(outputDir, { recursive: true });
  console.error(`Analyzing website: ${url}`);
  console.error(`Output directory: ${outputDir}`);

  // 1. Capture Multi-Viewport Screenshots
  console.error('Capturing multi-viewport responsive screenshots...');
  const desktopShot = path.join(outputDir, 'desktop_1920x1080.png');
  const tabletShot = path.join(outputDir, 'tablet_768x1024.png');
  const mobileShot = path.join(outputDir, 'mobile_375x812.png');

  captureScreenshot(url, desktopShot, 1920, 1080);
  captureScreenshot(url, tabletShot, 768, 1024);
  captureScreenshot(url, mobileShot, 375, 812);

  const screenshots = {
    desktop: fs.existsSync(desktopShot) ? desktopShot : null,
    tablet: fs.existsSync(tabletShot) ? tabletShot : null,
    mobile: fs.existsSync(mobileShot) ? mobileShot : null,
  };

  // 2. DOM & SEO Parsing
  console.error('Analyzing DOM structure & SEO tags...');
  const domData = await analyzeDomAndSeo(url);

  // 3. Lighthouse Audit
  let lighthouseData = null;
  if (!skipLighthouse) {
    lighthouseData = runLighthouseAudit(url, outputDir);
  }

  // 4. Generate Report
  const reportMd = generateMarkdownReport(url, outputDir, screenshots, domData, lighthouseData);
  const reportPath = path.join(outputDir, 'analysis_report.md');
  fs.writeFileSync(reportPath, reportMd, 'utf8');

  console.log(reportMd);
  console.error(`\nReport successfully generated at: ${reportPath}`);
}

main().catch(err => {
  console.error('Fatal execution error:', err);
  process.exit(1);
});
