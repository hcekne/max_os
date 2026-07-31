---
type: workflow
status: active
owner:
trigger_phrase: launch max os website in 90 minutes
tags: [workflow, max-os, website, launch, vite, cloudflare, godaddy, domain]
---

# Workflow - Launch Max OS Website in 90 Minutes

## Goal
Publish a conversion-ready Max OS landing page in under 90 minutes with:
- dual CTA (GitHub + waitlist),
- custom domain,
- TLS,
- analytics events with `site_id=max-os`.

## Strategic defaults (already decided)
- Frontend: Vite static build.
- Hosting: Cloudflare Pages.
- Domain DNS/Registrar: GoDaddy (`maxos.online`).
- Auth: skip gated auth on launch page (v1).
- CTA model:
  - Primary: open-source GitHub path.
  - Secondary: managed app waitlist.

## Domain record (current)
- Domain: `maxos.online`
- Registrar: GoDaddy
- Auto-renew: On
- Renewal date: 2028-03-08
- Renewal cost: €47.37/year

## Renewal policy (recommended)
- Keep auto-renew **On** during launch/validation to avoid accidental domain loss.
- Add a calendar reminder for 2028-02-01 to decide keep/cancel based on traction.
- If project is inactive by then, disable auto-renew before billing cycle.

## Inputs
- Max OS source positioning: `README.md`
- Prompt inspiration: `KNOWLEDGE/Notes/Note - Prompt v03 - Pricing Precision Landing Page - Nordic Minimal Performance.md`
- Waitlist implementation reference: `KNOWLEDGE/Notes/Note - Max OS Waitlist Schema and Frontend Submit Pattern (Vite) (2026-03-07).md`
- Domain: `maxos.online` in GoDaddy
- GitHub repo URL for Max OS

## 90-minute execution plan

### Block 1 (0-20 min): Generate and local-check site
1. Pick one launch prompt variant from `KNOWLEDGE/Notes/Note - Prompt Pack - Max OS Launch Site (Vite, 3 Styles) (2026-03-07).md`.
2. Generate Vite page with your one-shot workflow.
3. Ensure required sections exist:
   - Hero + value promise,
   - How Max OS works,
   - two CTA paths,
   - waitlist email capture,
   - trust/FAQ/footer.
4. Local sanity check:
   - CTA 1 opens GitHub repo,
   - CTA 2 opens waitlist form/modal,
   - mobile readability is acceptable.

### Block 2 (20-45 min): Add waitlist + analytics hooks
1. Implement waitlist capture quickly using one of these patterns:
   - Option A (fastest): Formspree/Tally/Typeform embed.
   - Option B: custom API endpoint if already available.
   - Use the exact payload and submit handler from `KNOWLEDGE/Notes/Note - Max OS Waitlist Schema and Frontend Submit Pattern (Vite) (2026-03-07).md`.
2. Minimum waitlist fields:
   - email,
   - optional “What would you want managed for you?”
3. Add analytics events with `site_id=max-os`:
   - `maxos_github_click`
   - `maxos_waitlist_open`
   - `maxos_waitlist_submit`
4. Include UTM capture for inbound traffic attribution.

### Block 3 (45-70 min): Deploy to Cloudflare Pages
1. Push site to GitHub repo.
2. In Cloudflare Pages:
   - Create project from repo,
   - Build command: `npm run build`,
   - Output directory: `dist`.
3. Deploy and test the `*.pages.dev` URL.
4. Verify both CTAs and waitlist flow in production preview.

### Block 4 (70-90 min): Attach domain + TLS + smoke test
1. In Cloudflare Pages, add custom domain.
2. In GoDaddy DNS, set records as instructed by Cloudflare.
3. Wait for DNS/TLS provisioning.
4. Run smoke tests:
   - home loads fast,
   - HTTPS valid,
   - GitHub CTA works,
   - waitlist submit works,
   - analytics events appear.

## GoDaddy + Cloudflare DNS quick notes
- Keep Cloudflare as serving layer for Pages and SSL.
- GoDaddy remains registrar (and optionally DNS host).
- Create exactly the DNS target Cloudflare Pages gives you for your project.

## Technical DNS path (GoDaddy -> Cloudflare Pages)

### Option A (fastest/safest launch): use `www.maxos.online` as canonical
1. In Cloudflare Pages, add `www.maxos.online` custom domain.
2. In GoDaddy DNS, create/update `CNAME`:
   - Host: `www`
   - Points to: `<your-pages-project>.pages.dev` (exact value from Cloudflare)
3. In GoDaddy forwarding, set root `maxos.online` to forward (301) to `https://www.maxos.online`.
4. Verify in Cloudflare Pages that domain status is Active and SSL certificate is issued.

### Option B (apex domain on Cloudflare DNS)
1. Add `maxos.online` to Cloudflare as a zone.
2. In GoDaddy registrar settings, switch nameservers to Cloudflare nameservers.
3. In Cloudflare DNS, set records for Pages project (including apex/root).
4. In Pages, set `maxos.online` as primary and optionally redirect `www` to root.

### Launch recommendation
- For speed today, use **Option A** (`www` canonical + root forward).
- Migrate to full Cloudflare DNS zone later if needed for broader platform automation.

## Launch checklist
- [ ] Site live on custom domain with HTTPS
- [ ] GitHub CTA working
- [ ] Waitlist submit working
- [ ] `site_id=max-os` analytics events firing
- [ ] Mobile pass complete

## Latest run status (2026-03-08)
- [x] Cloudflare Pages project connected and deployed from GitHub.
- [x] Custom domain `www.maxos.online` resolving to Cloudflare Pages.
- [x] Root domain forwarding configured: `maxos.online` -> `https://www.maxos.online` (301).
- [ ] Waitlist submit flow validated in production.
- [ ] Analytics events validated in production.
- [ ] Mobile pass + Lighthouse sanity check logged.

## Cost and billing reality (Cloudflare + GoDaddy)
- Cloudflare Pages can run on a free tier for static sites, which is why hosting may currently show as free.
- Cost typically starts when usage or features exceed free limits (or when other paid Cloudflare products are enabled).
- Domain cost is already active through GoDaddy renewal terms.
- Action: review Cloudflare billing pages and set alerts/limits before traffic grows.

## Output
- Live Max OS launch page with active dual CTA funnel.

## Follow-up (same day or next day)
- Share launch page on LinkedIn.
- Send 10-15 targeted messages with link + waitlist CTA.
- Track click-to-waitlist conversion and iterate copy.
