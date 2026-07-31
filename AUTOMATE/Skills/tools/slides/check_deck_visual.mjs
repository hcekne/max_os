#!/usr/bin/env node
/*
 * Headless visual QA for Max OS HTML slide decks.
 *
 * Checks every .slide at native render size, captures per-slide screenshots,
 * detects scroll/bounds/footer overflow, and writes a JSON report plus contact
 * sheets under .maxos/visual-check/screenshots/.
 */

import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

async function loadPlaywright() {
  const localPath = path.resolve(process.cwd(), ".maxos/visual-check/node_modules/playwright/index.js");
  if (fs.existsSync(localPath)) {
    return import(pathToFileURL(localPath).href);
  }
  return import("playwright");
}

function parseArgs(argv) {
  const args = { deck: "", outDir: "" };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--out") {
      args.outDir = argv[i + 1] || "";
      i += 1;
      continue;
    }
    if (!args.deck) args.deck = arg;
  }
  if (!args.deck) {
    console.error("Usage: node AUTOMATE/Skills/tools/slides/check_deck_visual.mjs <deck.html> [--out <dir>]");
    process.exit(2);
  }
  return args;
}

function slugify(value) {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "") || "deck";
}

async function screenshotContactSheet(browser, outDir, names, sheetIndex) {
  const sheetHtml = path.join(outDir, `contact-${String(sheetIndex).padStart(2, "0")}.html`);
  const figures = names.map((name) => {
    const slideNo = name.match(/slide-(\d+)\.png/)?.[1] || "";
    return `<figure><img src="${name}"><figcaption>Slide ${Number(slideNo)}</figcaption></figure>`;
  });
  const html = `<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { margin: 0; background: #d8d8d8; font-family: Arial, sans-serif; padding: 18px; }
    .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px; }
    figure { margin: 0; background: #fff; padding: 8px; box-shadow: 0 2px 12px rgba(0,0,0,.16); }
    img { display: block; width: 100%; height: auto; }
    figcaption { font-size: 13px; color: #333; margin-top: 6px; font-weight: 700; }
  </style>
</head>
<body><div class="grid">${figures.join("\n")}</div></body>
</html>
`;
  fs.writeFileSync(sheetHtml, html);

  const page = await browser.newPage({ viewport: { width: 1360, height: 1600 }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(sheetHtml).href);
  await page.screenshot({ path: path.join(outDir, `contact-${String(sheetIndex).padStart(2, "0")}.png`), fullPage: true });
  await page.close();
}

const args = parseArgs(process.argv.slice(2));
const deckAbs = path.resolve(process.cwd(), args.deck);
const deckDir = path.dirname(deckAbs);
const outDir = path.resolve(
  process.cwd(),
  args.outDir || path.join(".maxos/visual-check/screenshots", slugify(path.basename(deckDir))),
);
fs.mkdirSync(outDir, { recursive: true });

const playwright = await loadPlaywright();
const { chromium } = playwright.default || playwright;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(deckAbs).href, { waitUntil: "networkidle" });
await page.waitForTimeout(800);

const slideCount = await page.locator(".slide").count();
const results = [];
const screenshotNames = [];

for (let index = 0; index < slideCount; index += 1) {
  const slide = page.locator(".slide").nth(index);
  const slideNo = index + 1;
  const screenshotName = `slide-${String(slideNo).padStart(2, "0")}.png`;
  const screenshot = path.join(outDir, screenshotName);
  screenshotNames.push(screenshotName);
  await slide.screenshot({ path: screenshot });

  const metrics = await slide.evaluate((el) => {
    const slideRect = el.getBoundingClientRect();
    const body = el.querySelector(".slide__body");
    const footer = el.querySelector(".slide__footer");
    const bodyRect = body ? body.getBoundingClientRect() : null;
    const footerRect = footer ? footer.getBoundingClientRect() : null;

    const visibleDescendants = Array.from(el.querySelectorAll("*")).filter((node) => {
      const style = window.getComputedStyle(node);
      if (style.display === "none" || style.visibility === "hidden" || Number(style.opacity) === 0) return false;
      if (node.tagName === "SCRIPT" || node.tagName === "STYLE") return false;
      const rect = node.getBoundingClientRect();
      return rect.width > 0 && rect.height > 0;
    });

    const outside = [];
    const footerOverlaps = [];
    for (const node of visibleDescendants) {
      const rect = node.getBoundingClientRect();
      const classes = typeof node.className === "string" ? node.className.trim().replace(/\s+/g, ".") : "";
      const name = classes ? `${node.tagName.toLowerCase()}.${classes}` : node.tagName.toLowerCase();
      if (
        rect.left < slideRect.left - 0.5 ||
        rect.right > slideRect.right + 0.5 ||
        rect.top < slideRect.top - 0.5 ||
        rect.bottom > slideRect.bottom + 0.5
      ) {
        outside.push({ name, top: rect.top - slideRect.top, bottom: rect.bottom - slideRect.top });
      }
      if (body && footerRect && body.contains(node) && rect.bottom > footerRect.top - 8) {
        footerOverlaps.push({ name, bottom: rect.bottom - slideRect.top, footerTop: footerRect.top - slideRect.top });
      }
    }

    return {
      slide: Number(el.getAttribute("data-slide")),
      slideHeight: el.clientHeight,
      slideScrollHeight: el.scrollHeight,
      slideWidth: el.clientWidth,
      slideScrollWidth: el.scrollWidth,
      bodyHeight: body ? body.clientHeight : 0,
      bodyScrollHeight: body ? body.scrollHeight : 0,
      bodyWidth: body ? body.clientWidth : 0,
      bodyScrollWidth: body ? body.scrollWidth : 0,
      outside,
      footerOverlaps,
      title: el.querySelector(".slide__title, .title-headline")?.textContent?.trim() ?? "",
    };
  });

  const issues = [];
  if (metrics.slideScrollHeight > metrics.slideHeight + 1) issues.push(`slide vertical overflow ${metrics.slideScrollHeight}/${metrics.slideHeight}`);
  if (metrics.slideScrollWidth > metrics.slideWidth + 1) issues.push(`slide horizontal overflow ${metrics.slideScrollWidth}/${metrics.slideWidth}`);
  if (metrics.bodyScrollHeight > metrics.bodyHeight + 1) issues.push(`body vertical overflow ${metrics.bodyScrollHeight}/${metrics.bodyHeight}`);
  if (metrics.bodyScrollWidth > metrics.bodyWidth + 1) issues.push(`body horizontal overflow ${metrics.bodyScrollWidth}/${metrics.bodyWidth}`);
  if (metrics.outside.length) issues.push(`${metrics.outside.length} visible element(s) outside slide bounds`);
  if (metrics.footerOverlaps.length) issues.push(`${metrics.footerOverlaps.length} body element(s) overlap footer zone`);

  results.push({ slide: slideNo, title: metrics.title, screenshot, issues, metrics });
}

await page.close();

for (let i = 0; i < screenshotNames.length; i += 6) {
  await screenshotContactSheet(browser, outDir, screenshotNames.slice(i, i + 6), i / 6 + 1);
}

await browser.close();

const report = {
  deck: deckAbs,
  slideCount,
  checkedAt: new Date().toISOString(),
  failures: results.filter((r) => r.issues.length),
  screenshotDir: outDir,
  results,
};
fs.writeFileSync(path.join(outDir, "report.json"), JSON.stringify(report, null, 2));

for (const result of results) {
  const status = result.issues.length ? "FAIL" : "PASS";
  console.log(`[${status}] ${String(result.slide).padStart(2, "0")} ${result.title}`);
  for (const issue of result.issues) console.log(`  - ${issue}`);
}
console.log(`Screenshots: ${outDir}`);

if (report.failures.length) process.exit(1);
