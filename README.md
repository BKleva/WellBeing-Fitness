# WellBeing Fitness: website

Static, SEO-first site for WellBeing Fitness (Westford & Groton, MA). Built by `tools/build.py` from content in `tools/data.py`.

```
python tools/build.py            # regenerate every page, sitemap.xml, robots.txt, netlify.toml
python tools/audit.py            # QA: broken links/anchors/assets, title + description lengths, H1 count
python tools/prep_images.py      # (rarely) re-export /images from assets/raw
```

Preview locally: launch config **WellBeingFitness** (port 8095). Deploy: drag the folder to Netlify or connect the repo (publish dir `.`).

## Where things live
| What | Where |
| --- | --- |
| Team bios, class styles, services copy, FAQs, studios, Pilates pricing | `tools/data.py` |
| Page templates, nav, footer, schema.org JSON-LD, redirects from the old Wix URLs | `tools/build.py` |
| External systems (Mindbody schedule, Wix pass checkout/login, Bonfire) | constants at the top of `tools/build.py` |
| Design | `css/styles.css` (tokens at the top) |

## Memberships "Plan Studio"
`/memberships/` is an interactive plan finder (`js/plans.js`, `css/plans.css`): a classes-per-month slider prices every option and flags the best value, with a membership-card summary and a checkout button. Prices live in `PLANS_*` in `tools/data.py`, copied from the studio's Mindbody online store (site 729963). Checkout links to that store; packages not sold online (private 1/6/12) route to the contact form. If Mindbody prices change, edit `data.py` and rebuild.

## Fit Shop / Shopify
The live site's "Fit Shop" is a link to a **Bonfire** merch store (no Shopify store was found), so the shop page currently shows the real Bonfire apparel with links out.
When a Shopify store exists:
```
python tools/sync_shopify.py yourstore.myshopify.com
python tools/build.py
```
This pulls the public product feed, renders products into static HTML + Product schema (indexable), and turns on the in-page bag. Checkout hands off to Shopify through a cart permalink, so no API keys are needed. Re-run after catalog changes (or wire a Netlify build hook).

## Before launch
- Confirm the **Reformer Pilates 6/12-session and single prices** (`REFORMER_*`, `PLANS_PRIVATE` in `data.py`); they come from an "intro sale" flyer. The $360/$680 monthly and $1,800 24-pack match Mindbody.
- Mindbody contracts say "every month for 12 months", while the old policies page says a 3-month commitment. The page says "terms shown before you confirm"; confirm which is right.
- In Netlify: Forms -> add a notification to info@wellbeing-fitness.com for the `home-consult` and `contact` forms.
- Class registration and pass purchase still run on Mindbody / Wix. If the domain moves off Wix, point `PASSES_URL`, `ACCOUNT_URL` and `EVENTS_URL` at wherever those live.
- `netlify.toml` 301-redirects the old Wix URLs (e.g. `/private-fitness` -> `/personal-training/`) so existing search rankings carry over.
- Add Google Business Profile / Search Console, then submit `sitemap.xml`.
