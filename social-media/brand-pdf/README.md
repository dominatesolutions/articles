# Dominate Solutions — Brand PDF (Company & Services Overview)

A 6-page, on-brand capabilities brochure for Dominate Solutions, built from the
real brand assets (logo + palette) and content pulled from dominatesolutions.com
and its public profiles.

**Deliverable:** [`Dominate-Solutions-Overview.pdf`](./Dominate-Solutions-Overview.pdf) · US Letter (8.5×11")

## Pages
1. **Cover** — logo, positioning headline, value proposition
2. **Who We Are** — story, founder quote (Nate Denson), stat row
3. **What We Offer** — 6 services (Web Design, Local SEO, Google Ads, Local Service Ads, Branding, Hosting)
4. **What Makes Us Different** — 5 differentiators
5. **Our Process** — 4-step Discover → Design & Build → Launch & Optimize → Grow & Dominate
6. **Call to Action** — free audit offer + contact

## Brand palette used
| Role | Hex |
|------|-----|
| Cream (background) | `#F7F5F1` |
| Gold (accent) | `#D4A94F` |
| Light gold | `#E0B45E` |
| Warm gray | `#A8A49C` |
| Brown-gray (secondary text) | `#767269` |
| Dark section | `#1A1204` |
| Near-black / footer | `#0D0C0B` |
| Black (text) | `#000000` |

Fonts: **Montserrat** (headings/body) + **Oswald** (labels, numerals) — matches the wordmark.

## Editing & rebuilding
1. Edit `index.html` (all copy and layout live there).
2. Rebuild the PDF:
   ```bash
   pip install playwright
   python3 build.py
   ```
   The script auto-detects a local Chromium; otherwise Playwright's bundled
   browser is used.

## Assets
- `assets/logo-trans.png` — transparent-background lockup (for dark sections)
- `assets/logo-full-black.jpeg` — original logo on black (source)
- `assets/fonts/ttf/` — Montserrat + Oswald web fonts

## Notes / to confirm before external use
- The three client names (Protecting Angels, Tampa Deck Builders, Captured by
  Mallary) came from public press releases — confirm they're OK to feature.
- Swap the "Book Yours →" CTA for your real booking link/phone if desired.
