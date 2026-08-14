# BRICS Bazaar 2026 — Static HTML + CSS Build

A concept / prototype website for **BRICS Bazaar 2026** — a craft exhibition bringing together artisans from India and the BRICS nations at the National Crafts Museum & Hastkala Academy, New Delhi.

> ⚠️ **This is a concept website.** Artisan names, stall assignments, exact timings, prices and some other details are **sample/demo data** and are clearly marked as such throughout the site. Nothing on this site should be treated as an official confirmation.

**This build contains zero JavaScript.** No `<script>` tags, no inline handlers, no `.js` files, no frameworks. Every interaction is native HTML or CSS.

## Event Details

**Event:** BRICS Bazaar 2026
**Theme:** Crafting Cultures, Connecting Peoples
**Dates:** 8–13 September 2026
**Venue:** National Crafts Museum & Hastkala Academy, New Delhi

## Technology

- HTML5
- CSS3 (no framework, no build step, no preprocessor)
- Google Fonts (Fraunces, Work Sans, IBM Plex Mono)
- GitHub Pages, or any static host

## Project Structure

```
brics-bazaar/
├── index.html      → all page content, including all 60 stalls and the site plan SVG
├── style.css       → all styling, responsive rules, and the CSS-only interaction layer
├── assets/
│   ├── images/
│   ├── icons/
│   └── fonts/
├── build/          → OPTIONAL developer tooling, not part of the website
└── README.md
```

`index.html` and `style.css` are the entire website. You can delete `build/` and the site still works.

## How to Run

Double-click `index.html`. That's it — there is nothing to install, compile or serve.

### Deploying to GitHub Pages

1. Create a repository and upload `index.html`, `style.css`, `assets/` and `README.md`.
2. **Settings → Pages → Branch:** `main` and `/ (root)`, then **Save**.
3. Your site appears at `https://yourusername.github.io/your-repo-name/`.

## What Replaced the JavaScript

| Feature | Previously | Now |
|---|---|---|
| Mobile menu | class toggle + click listeners | `:target` on the menu panel; following any nav link moves `:target` and closes it |
| Stall directory (60 cards) | generated from a data array at runtime | written out as static `<article>` elements |
| Directory filters | click handlers + array filtering | hidden radio inputs + `:checked ~` sibling selectors on `data-origin` / `data-cat` |
| Result counts | recalculated on every filter | one pre-computed line per filter, revealed by `:checked` |
| Stall detail modal | built and injected on click | 60 static modals revealed by `:target`, with prev/next links |
| Country wheel | nodes created and positioned in JS | static `<label>`s at pre-computed polar coordinates; radio + `:checked` reveals each panel |
| Venue site plan | SVG built element by element | hand-written SVG; all 60 markers are real `<a>` links to their stall modal |
| Map filters | class toggling | radio inputs + `:checked` dimming by `data-origin` |
| Event schedule tabs | click handlers re-rendering a panel | radio inputs + `:checked` showing the matching day panel |
| Mystery Box button | `scrollIntoView()` | `<a href="#box-tiers">` + `scroll-behavior: smooth` |
| Passport stamps | `Set` + re-render | checkboxes; collected styling via `:checked` |
| Passport count | manual text update | a **CSS counter** incremented by each checked stamp |
| Passport progress bar | JS-set inline width | one segment per stamp, each filling via `:checked` |
| Header scroll shadow | scroll event listener | scroll-driven CSS animation where supported, absent elsewhere |
| Scroll reveal | viewport observer | CSS entrance animation on load |
| Animated counters | rAF count-up | static numbers |
| Active nav link | scroll position detection | `:target` combined with `:has()` |

## What Could Not Be Replicated

These genuinely require JavaScript. They were removed rather than faked:

1. **Live text search.** Both the directory and "find my stall" inputs filtered as you typed. The directory search field is kept, styled identically and marked up as a real `<form method="get">` with a named input, so it can be pointed at a server-side search endpoint without any visual change. A note under it tells visitors to use the filters instead. The map's search input was removed; its "find my stall" job is now done by the category filters and by the markers being links.

2. **Persistent passport state.** Stamps toggle and the count and progress bar update correctly, but nothing is stored — reloading clears the selection. This is stated on the page itself. "Start Your Craft Journey" is a link to `index.html?start=1#passport`, which forces a fresh document load and therefore genuinely resets every stamp.

3. **Combining a filter with a search term.** Filters are mutually exclusive radio buttons. Stacking multiple independent conditions is not practical in pure CSS.

4. **Modal focus trapping and Escape-to-close.** Modals open, close via the ✕ or the backdrop, and close on the browser's Back button. Focus is not trapped inside them and Escape does not close them.

5. **Scroll-triggered reveal.** A scroll-driven CSS timeline was trialled, but such animations *scrub* rather than play once, so elements faded back out when scrolling upward. A one-shot entrance animation is used instead, so content is never left invisible.

## Two Bugs Fixed Along the Way

Both existed in the original stylesheet and were caught by browser testing:

- **Horizontal overflow below 860px.** The off-canvas menu is `position: fixed` and translated one full viewport to the right, which extended the scrollable width to 2× the viewport on every phone and tablet size. Fixed with `overflow-x: clip` at the root, which — unlike `hidden` — does not create a scroll container, so the sticky header still works.
- **Collapsed mobile menu panel.** `.site-header` uses `backdrop-filter`, which makes it the containing block for `position: fixed` descendants. The menu's `bottom: 0` therefore resolved against the 78px header instead of the viewport, collapsing the panel to 64px. Fixed with an explicit `height: calc(100dvh - var(--header-h))`.

## Updating Content

All content now lives in `index.html`. Colours and type are still defined once in `:root` at the top of `style.css`.

| What to change | Where |
|---|---|
| Stall / artisan details | search `class="stall-card"` — edit the card, then its matching `id="stall-NN"` modal |
| Country craft descriptions | search `class="country-panel"` |
| Event schedule | search `class="day-panel"` |
| Passport stamps | search `class="stamp-card"` |
| Site plan zones | search `class="map-zone"` in the inline SVG |
| Mystery Box tiers and prices | search `class="box-card"` |
| Visitor info and venue | search `VISITOR INFORMATION` and `THE VENUE` |
| Colours | `:root` in `style.css` |
| Logo | search `UPDATE LOGO HERE` (appears in the header and footer) |

Stall cards and their modals are separate blocks — edit both, or regenerate with the build script below.

### Adding or removing stalls

A stall needs three things kept in sync: its card, its modal, and its marker in the site-plan SVG. For small edits, do it by hand. For bulk changes, `build/gen.py` regenerates `index.html` from the data at the top of the file:

```bash
python3 build/gen.py      # rewrites index.html
python3 build/verify.py   # optional: browser checks (needs playwright)
```

`build/` is developer tooling only. It never ships to the browser and the site does not depend on it.

## Accessibility Notes

- Semantic landmarks throughout: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`, plus a skip link.
- All interactive controls are real focusable elements — radios, checkboxes and links. The hidden inputs driving filters and tabs stay keyboard-reachable, with visible focus rings on their labels.
- The closed mobile menu is `visibility: hidden`, so its links are not reachable by keyboard or screen reader until it is opened.
- Every stall marker on the site plan has an `aria-label` naming its stall and artisan.
- `prefers-reduced-motion` disables the entrance animation and progress transitions.

## Browser Support

Works in all current browsers. Two enhancements degrade gracefully:

- `:has()` drives the active nav underline and the menu open/close control swap. Without it the underline simply doesn't appear and the burger stays a burger — the menu still opens, and every nav link still closes it.
- Scroll-driven animation adds the header shadow on scroll. Without it there is no shadow.

Neither affects content, layout or navigation.
