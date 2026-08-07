---
type: workflow
status: active
owner:
trigger_phrase: ship idea to live website
tags: [workflow, website-factory, launch, cloudflare, vite, industrialization]
---

# Workflow - Ship Idea to Live Website (Factory Sprint)

## Purpose
Turn a raw website idea into a live domain quickly and repeatably, while capturing launch learnings for scale.

## Default stack (factory baseline)
- Frontend: Vite (default for speed).
- Hosting: Cloudflare Pages.
- Domain registrar: variable (GoDaddy, Route53, etc.).
- Auth on launch page: optional and usually skipped for v1.

## Use this when
- You want to test demand fast with a public website.
- You need a repeatable launch path that can scale to many sites.

## Timeboxed sprint (120 min)

### Phase 0 (5 min): Define launch card
- Site name
- Domain
- ICP + one-line promise
- Primary CTA (usually repo/demo)
- Secondary CTA (usually waitlist/contact)
- Success signal in first 7 days

### Phase 1 (20 min): Generate prompt + site variant
1. Turn the launch card into a concise implementation brief covering content hierarchy, visual direction, and CTA behavior.
2. Generate 1-3 variants quickly.
3. Pick one based on readability and CTA clarity, not visual novelty.

### Phase 2 (20 min): Local build and conversion wiring
1. Run local build and preview.
2. Ensure two CTA paths are working.
3. Add waitlist handler and analytics hooks (`site_id` scoped).

### Phase 3 (25 min): Repo and deployment
1. Push to dedicated website repo.
2. Cloudflare Pages config:
   - Framework preset: `None` (unless exact framework preset exists)
   - Build command: `npm run build`
   - Output directory: `dist`
3. Deploy and test `*.pages.dev`.

### Phase 4 (25 min): Domain and TLS
1. Add custom domain in Cloudflare Pages.
2. Configure DNS at registrar.
3. Resolve common DNS issues:
   - `www` record conflicts (remove/replace old `www` A/CNAME records)
   - root forwarding loop (never forward root to itself)
4. Validate HTTPS and redirect behavior.

### Phase 5 (25 min): Post-launch and logging
1. Publish one LinkedIn post.
2. Send first 10 targeted shares.
3. Log launch run summary and learnings in project/todo.
4. Check costs and free-tier exposure.

## Decision gate: Vite vs Next.js
- Use Vite when:
  - static marketing page,
  - speed matters,
  - lowest ops friction.
- Use Next.js when:
  - SSR is required,
  - app-style dynamic routes are required,
  - server-side content/personalization is needed.

## Factory anti-failure checklist
- [ ] Framework preset is correct (do not choose VitePress for standard Vite site).
- [ ] Output directory is `dist`.
- [ ] Domain root forwarding points to `www` (or canonical), not itself.
- [ ] Waitlist flow tested in production.
- [ ] Analytics events firing with `site_id`.

## Output
- Live website on custom domain.
- Launch run log with what worked and what broke.
- Reusable improvements fed back into factory workflows.

## Related
- [[Workflow - Launch Max OS Website in 90 Minutes]]
