# Dominate Solutions — Social Graphics (Instagram + Facebook)

23 branded slides across 10 posts. Format: **1080 × 1350 (4:5 portrait)** — the
best-performing size for both Instagram and Facebook feeds. Pair each with the
caption in [`../posts/`](../posts).

| # | Post | Format | Files |
|---|------|--------|-------|
| 1 | Website = your #1 salesperson | Single | `01-website-salesperson.png` |
| 2 | Google Business Profile tips | **Carousel · 6** | `02-google-business-profile/01–06.png` |
| 3 | Before → After glow-up | **Carousel · 3** | `03-before-after/01–03.png` |
| 4 | 3-second speed stat | Single | `04-site-speed.png` |
| 5 | Client win / testimonial | Single | `05-client-win.png` |
| 6 | Google Ads + Local Service Ads | Single | `06-google-ads.png` |
| 7 | 5 things that convert | **Carousel · 7** | `07-conversion-checklist/01–07.png` |
| 8 | Custom, not cookie-cutter | Single | `08-custom-not-template.png` |
| 9 | Tampa Bay local pride | Single | `09-tampa-local.png` |
| 10 | Free audit offer | Single | `10-free-audit.png` |

**Carousels:** upload the numbered slides in order (01, 02, 03 …) as a single
multi-image post. Slide 01 is the hook; the last slide is the call-to-action.

## Before you publish
- **Post 5 (client win)** uses a placeholder quote, result, and name — swap in a
  real testimonial before posting.
- CTAs use DM/comment keywords ("WEBSITE", "ADS", "AUDIT", "SPEED"). Adjust to
  match how you actually capture leads, or add your booking link.

## Editing & rebuilding
All slides are generated from templates in `build_posts.py` (shares the brand
fonts + logo in `../brand-assets/assets`). To change copy or colors:
```bash
pip install playwright
python3 build_posts.py    # re-renders every slide
```
