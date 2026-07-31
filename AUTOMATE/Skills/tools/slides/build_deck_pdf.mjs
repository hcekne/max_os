#!/usr/bin/env node
/*
 * Build a PDF of a Max OS slide deck.
 *
 * Usage:
 *   node build_deck_pdf.mjs <deck.html> [<out.pdf>] [--raster | --truevector]
 *
 * Default mode: HYBRID — looks EXACTLY like the HTML in every PDF viewer AND
 * keeps crisp, selectable VECTOR text. This is the one you want.
 *
 *   Two passes over the deck:
 *     1. Hide all text, then screenshot each slide. The screenshot therefore
 *        carries only the things that MUST be raster to render correctly in
 *        every viewer — soft card box-shadows, Chart.js canvases, logos, fills.
 *     2. Put that screenshot behind the slide as the visible backdrop, hide the
 *        now-redundant fills/borders/shadows/images, and let the slide's REAL
 *        text render on top as true vector. Result: shadows/charts/logos are
 *        pixel-identical to the browser preview, while text stays crisp at any
 *        zoom, selectable, searchable and copyable — exactly like PowerPoint→PDF.
 *        Typical output is well under 1 MB.
 *
 * Why not pure `page.pdf()` vector (available as --truevector):
 *
 *   Chromium's `page.pdf()` emits each CSS box-shadow as a separate PDF
 *   soft-mask. Poppler (pdftoppm) composites these cleanly, but macOS Quartz
 *   (Preview, Quick Look, the VS Code PDF viewer) and some others DOUBLE-DARKEN
 *   the seam where two adjacent cards' shadow masks meet — drawing an ugly hard
 *   grey/black band down the inner edge of every card except the first. The PDF
 *   looks fine in one renderer and broken in another. The hybrid sidesteps this
 *   entirely: the visible layer is a flat raster, so there are no soft-masks for
 *   a viewer to misrender. --truevector keeps true vector text and a tiny file
 *   but WILL show the shadow-seam artifact in Quartz-based viewers; only use it
 *   for decks with no card shadows, or when file size matters more than fidelity.
 *
 *   --raster is the old behaviour: screenshots only, NO selectable text.
 *
 * IMPORTANT for anyone verifying this tool: render the OUTPUT PDF with a
 * Quartz-based engine (`sips -s format png page.pdf --out x.png`) or Quick Look,
 * NOT just poppler/pdftoppm. Poppler hides the exact seam artifact this file
 * exists to avoid, so a poppler-only check will tell you a broken PDF is fine.
 */

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

// Playwright is typically installed per-deck under `.maxos/visual-check/`
// (the same install that `check_deck_visual.mjs` uses). Resolve it from the
// caller's CWD first, then fall back to a global install.
async function loadPlaywright() {
  const localPath = path.resolve(process.cwd(), ".maxos/visual-check/node_modules/playwright/index.js");
  if (fs.existsSync(localPath)) {
    return import(pathToFileURL(localPath).href);
  }
  return import("playwright");
}
const playwright = await loadPlaywright();
const { chromium } = playwright.default || playwright;

const SLIDE_W = 1280;
const SLIDE_H = 720;
const SCALE = 3; // High-DPI capture (~288 DPI at print size). Crisp text + shadows.

// Strip the browser-preview chrome: grey gutters between slides, page bg, and
// the slide's own preview drop-shadow (which would otherwise be captured).
const PREVIEW_CHROME_CSS = `
  html, body { background: #fff !important; }
  .deck { gap: 0 !important; padding: 0 !important; }
  .slide { box-shadow: none !important; margin: 0 !important; }
`;

function parseArgs(argv) {
  const positional = argv.filter((a) => !a.startsWith("--"));
  const flags = new Set(argv.filter((a) => a.startsWith("--")));
  const deckPath = positional[0];
  if (!deckPath) {
    console.error("Usage: node build_deck_pdf.mjs <deck.html> [<out.pdf>] [--raster | --truevector]");
    process.exit(2);
  }
  const resolvedDeck = path.resolve(deckPath);
  const outPath =
    positional[1] ?? path.join(path.dirname(resolvedDeck), path.basename(resolvedDeck, ".html") + ".pdf");
  const mode = flags.has("--raster") ? "raster" : flags.has("--truevector") ? "truevector" : "hybrid";
  return { deckPath: resolvedDeck, outPath: path.resolve(outPath), mode };
}

async function openDeck() {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: SLIDE_W, height: SLIDE_H },
    deviceScaleFactor: SCALE,
  });
  const page = await context.newPage();
  return { browser, page };
}

// CSS that hides text during the screenshot pass (layout preserved). Scoped to
// html.__capture so it can be toggled on for capture, off for the vector pass.
const HIDE_TEXT_CSS = `
  html.__capture .slide * {
    color: transparent !important;
    -webkit-text-fill-color: transparent !important;
    text-shadow: none !important;
  }
`;

// Runs INSIDE the page (pass 2). Puts each slide's text-free screenshot behind
// the slide as the visible backdrop, then hides the now-redundant visual styling
// (fills, borders, shadows, images, charts — all already in the screenshot) so
// only the real, vector text paints on top.
function compositeVectorText(shotUrls) {
  const slides = [...document.querySelectorAll(".slide")];
  slides.forEach((sl, i) => {
    sl.style.position = "relative";
    sl.style.overflow = "hidden";
    const img = document.createElement("img");
    img.src = shotUrls[i];
    img.className = "__bgshot";
    img.style.cssText = "position:absolute;left:0;top:0;width:100%;height:100%;z-index:0;";
    sl.insertBefore(img, sl.firstChild);
  });
  const style = document.createElement("style");
  style.textContent = `
    .slide > *:not(.__bgshot) { position: relative; z-index: 1; }
    .slide *:not(.__bgshot) {
      box-shadow: none !important;
      border-color: transparent !important;
      background-color: transparent !important;
      background-image: none !important;
    }
    .slide img:not(.__bgshot), .slide canvas, .slide svg { opacity: 0 !important; }
  `;
  document.head.appendChild(style);
}

async function pdf(page, outPath) {
  await page.pdf({
    path: outPath,
    width: "13.333in",
    height: "7.5in",
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
    preferCSSPageSize: true,
  });
}

// HYBRID (default): text-free screenshot backdrop + real vector text on top.
async function buildHybridPdf(deckPath, outPath) {
  const { browser, page } = await openDeck();
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "deck-hybrid-"));
  await page.goto(pathToFileURL(deckPath).href, { waitUntil: "networkidle" });
  await page.waitForTimeout(400); // let Chart.js settle
  await page.addStyleTag({ content: PREVIEW_CHROME_CSS });
  await page.addStyleTag({ content: HIDE_TEXT_CSS });

  // Pass 1: hide text, screenshot fills/shadows/charts/logos only.
  await page.evaluate(() => document.documentElement.classList.add("__capture"));
  const count = await page.locator(".slide").count();
  const shotUrls = [];
  for (let i = 0; i < count; i += 1) {
    const f = path.join(tmpDir, `s${String(i).padStart(2, "0")}.png`);
    const handle = await page.locator(".slide").nth(i).elementHandle();
    await handle.screenshot({ path: f });
    shotUrls.push(pathToFileURL(f).href);
  }
  await page.evaluate(() => document.documentElement.classList.remove("__capture"));

  // Pass 2: composite screenshot behind, paint real vector text on top.
  await page.evaluate(compositeVectorText, shotUrls);
  // Wait for every backdrop <img> to finish decoding before printing. Without
  // this, page.pdf() can fire before the (many, large) backdrop images have
  // loaded, so the PDF captures blank slides with no fills/shadows/charts. The
  // race only bites on larger decks (it was latent until the deck grew past a
  // few dozen slides), so await decode explicitly rather than a fixed timeout.
  await page.evaluate(async () => {
    const shots = [...document.querySelectorAll("img.__bgshot")];
    await Promise.all(shots.map((img) =>
      img.complete && img.naturalWidth > 0
        ? Promise.resolve()
        : new Promise((res) => { img.onload = res; img.onerror = res; })));
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
  });
  await page.waitForTimeout(150);
  await pdf(page, outPath);
  await browser.close();
  fs.rmSync(tmpDir, { recursive: true, force: true });
  return count;
}

// TRUEVECTOR: plain page.pdf(). True vector text, tiny file — but card box-shadows
// may render as dark seams in Quartz-based viewers (Preview/Quick Look). See header.
async function buildTrueVectorPdf(deckPath, outPath) {
  const { browser, page } = await openDeck();
  await page.goto(pathToFileURL(deckPath).href, { waitUntil: "networkidle" });
  await page.waitForTimeout(400);
  await page.addStyleTag({ content: `html, body { background: #fff !important; } .deck { gap: 0 !important; padding: 0 !important; }` });
  await pdf(page, outPath);
  await browser.close();
}

// RASTER (legacy): screenshots stitched one-per-page. No selectable text.
async function buildRasterPdf(deckPath, outPath) {
  const { browser, page } = await openDeck();
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "deck-raster-"));
  await page.goto(pathToFileURL(deckPath).href, { waitUntil: "networkidle" });
  await page.addStyleTag({ content: PREVIEW_CHROME_CSS });
  const count = await page.locator(".slide").count();
  const imgTags = [];
  for (let i = 0; i < count; i += 1) {
    const f = path.join(tmpDir, `s${String(i).padStart(2, "0")}.png`);
    const handle = await page.locator(".slide").nth(i).elementHandle();
    await handle.screenshot({ path: f });
    imgTags.push(`<img src="${pathToFileURL(f).href}">`);
  }
  const stitch = `<!doctype html><html><head><style>
@page { size: 13.333in 7.5in; margin: 0; }
* { margin: 0; padding: 0; }
html, body { background: #fff; }
img { display: block; width: 13.333in; height: 7.5in; page-break-after: always; break-after: page; }
img:last-child { page-break-after: auto; break-after: auto; }
</style></head><body>${imgTags.join("\n")}</body></html>`;
  const stitchPath = path.join(tmpDir, "stitch.html");
  fs.writeFileSync(stitchPath, stitch);
  await page.goto(pathToFileURL(stitchPath).href, { waitUntil: "networkidle" });
  await page.pdf({
    path: outPath,
    width: "13.333in",
    height: "7.5in",
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
    preferCSSPageSize: false,
  });
  await browser.close();
  fs.rmSync(tmpDir, { recursive: true, force: true });
  return count;
}

async function main() {
  const { deckPath, outPath, mode } = parseArgs(process.argv.slice(2));
  if (!fs.existsSync(deckPath)) {
    console.error(`Deck HTML not found: ${deckPath}`);
    process.exit(1);
  }
  try {
    if (mode === "raster") {
      const n = await buildRasterPdf(deckPath, outPath);
      console.log(`Built PDF: ${outPath} (${n} slides, raster — NOT selectable)`);
    } else if (mode === "truevector") {
      await buildTrueVectorPdf(deckPath, outPath);
      console.log(`Built PDF: ${outPath} (true vector — small + selectable, but card shadows may show seams in Quartz/Preview)`);
    } else {
      const n = await buildHybridPdf(deckPath, outPath);
      console.log(`Built PDF: ${outPath} (${n} slides, hybrid — pixel-identical to HTML in every viewer + selectable text)`);
    }
  } catch (err) {
    console.error("PDF build failed:", err);
    process.exit(1);
  }
}

main();
