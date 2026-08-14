# -*- coding: utf-8 -*-
"""Verification harness. Drives the built static site in a real browser and
asserts that every CSS-only interaction behaves. Build-time only."""
import os, sys
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "file://" + os.path.join(BASE, "index.html")
SHOTS = os.path.join(BASE, "build", "shots")
os.makedirs(SHOTS, exist_ok=True)

fails, checks = [], [0]

def ck(name, got, want):
    checks[0] += 1
    ok = got == want
    print(("  PASS  " if ok else "  FAIL  ") + "%-46s got=%r want=%r" % (name, got, want))
    if not ok:
        fails.append(name)

def ck_true(name, cond, detail=""):
    checks[0] += 1
    print(("  PASS  " if cond else "  FAIL  ") + "%-46s %s" % (name, detail))
    if not cond:
        fails.append(name)

with sync_playwright() as pw:
    browser = pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")

    # ---------------------------------------------------------------
    # A. Structural counts + CSS-only behaviour (desktop)
    # ---------------------------------------------------------------
    page = browser.new_page(viewport={"width": 1440, "height": 950})
    page.goto(URL)
    page.wait_for_timeout(900)

    print("\n[A] STRUCTURE")
    ck("stall cards in DOM", page.locator(".stall-card").count(), 60)
    ck("stall modals in DOM", page.locator(".stall-modal").count(), 60)
    ck("map stall markers", page.locator(".map-stall").count(), 60)
    ck("country nodes", page.locator(".country-node").count(), 11)
    ck("country panels", page.locator(".country-panel").count(), 11)
    ck("map zones", page.locator(".map-zone").count(), 13)
    ck("legend rows", page.locator(".map-legend li").count(), 13)
    ck("day tabs", page.locator(".day-tab").count(), 6)
    ck("day panels", page.locator(".day-panel").count(), 6)
    ck("event cards total", page.locator(".event-card").count(), 18)
    ck("stamp cards", page.locator(".stamp-card").count(), 6)
    ck("filter buttons", page.locator(".directory-controls .filter-btn").count(), 10)
    ck("script tags", page.locator("script").count(), 0)

    print("\n[B] REVEAL ANIMATION — nothing may stay invisible after scrolling")
    page.evaluate("""async () => {
        const step = window.innerHeight * 0.6;
        for (let y = 0; y < document.body.scrollHeight; y += step) {
            window.scrollTo(0, y);
            await new Promise(r => setTimeout(r, 45));
        }
        window.scrollTo(0, 0);
    }""")
    page.wait_for_timeout(1200)
    hidden = []
    for i in range(page.locator(".reveal").count()):
        el = page.locator(".reveal").nth(i)
        op = el.evaluate("e => getComputedStyle(e).opacity")
        if float(op) < 0.9:
            hidden.append((i, op))
    ck_true("all .reveal elements visible", not hidden, "hidden=%s" % hidden[:5])

    print("\n[C] DEFAULT STATES")
    ck_true("India panel shown by default",
            page.locator('.country-panel[data-country="0"]').is_visible())
    ck_true("Brazil panel hidden by default",
            not page.locator('.country-panel[data-country="1"]').is_visible())
    ck("visible results count", page.locator(".results-count:visible").inner_text(),
       "Showing 60 of 60 stalls")
    ck("visible stall cards (All)", page.locator(".stall-card:visible").count(), 60)
    ck_true("day 1 panel shown", page.locator('.day-panel[data-day="1"]').is_visible())
    ck_true("day 3 panel hidden", not page.locator('.day-panel[data-day="3"]').is_visible())
    page.locator("#passport").scroll_into_view_if_needed(); page.wait_for_timeout(700)
    page.locator(".passport-progress").screenshot(path=os.path.join(SHOTS, "passport-0.png"))

    print("\n[D] COUNTRY WHEEL (radio + :checked)")
    page.locator('.country-node[for="c-4"]').click()   # South Africa
    page.wait_for_timeout(250)
    ck_true("South Africa panel shown",
            page.locator('.country-panel[data-country="4"]').is_visible())
    ck_true("India panel now hidden",
            not page.locator('.country-panel[data-country="0"]').is_visible())
    ck("panel text", page.locator(".country-panel:visible p").inner_text(),
       "Beadwork, textiles, sculpture")

    print("\n[E] DIRECTORY FILTERS (radio + :checked)")
    for fid, want, label in [("indian", 40, "Showing 40 of 60 stalls"),
                             ("international", 20, "Showing 20 of 60 stalls"),
                             ("textiles", 25, "Showing 25 of 60 stalls"),
                             ("metal", 4, "Showing 4 of 60 stalls"),
                             ("food", 0, "Showing 0 of 60 stalls")]:
        page.locator('.filter-btn[for="f-%s"]' % fid).click()
        page.wait_for_timeout(150)
        ck("filter %-14s visible cards" % fid,
           page.locator(".stall-card:visible").count(), want)
        ck("filter %-14s count text" % fid,
           page.locator(".results-count:visible").inner_text(), label)
    ck_true("empty-category shows no-results message",
            page.locator(".no-results").is_visible())
    page.locator('.filter-btn[for="f-all"]').click()
    page.wait_for_timeout(150)
    ck_true("no-results hidden again", not page.locator(".no-results").is_visible())

    print("\n[F] STALL MODAL (:target)")
    ck_true("modal closed initially", not page.locator("#stall-01").is_visible())
    page.locator('.stall-card a[href="#stall-01"]').click()
    page.wait_for_timeout(400)
    ck_true("modal 01 open", page.locator("#stall-01").is_visible())
    ck("modal title", page.locator("#stall-01 h3").inner_text(),
       "Gujarat Artisan Collective 1")
    ck("modal craft row", page.locator("#stall-01 dd").nth(1).inner_text(),
       "Bandhani tie-dye textiles")
    page.locator("#stall-01 .modal-nav a").nth(2).click()   # next stall
    page.wait_for_timeout(400)
    ck_true("next-stall link opened 02", page.locator("#stall-02").is_visible())
    ck_true("stall 01 closed", not page.locator("#stall-01").is_visible())
    page.locator("#stall-02 .modal-close").click()
    page.wait_for_timeout(400)
    ck_true("modal closed via close button", not page.locator("#stall-02").is_visible())

    print("\n[G] MAP")
    page.locator('.map-stall-link[href="#stall-45"]').click()
    page.wait_for_timeout(400)
    ck_true("map marker opens stall modal", page.locator("#stall-45").is_visible())
    ck("map modal title", page.locator("#stall-45 h3").inner_text(), "China Craft Pavilion 3")
    page.locator("#stall-45 .modal-close").click()
    page.wait_for_timeout(300)
    page.locator('.map-controls .filter-btn[for="mf-indian"]').click()
    page.wait_for_timeout(300)
    dim = page.locator('.map-stall[data-origin="international"]').first
    ck_true("intl markers dimmed by India filter",
            float(dim.evaluate("e => getComputedStyle(e).opacity")) < 0.3,
            "opacity=%s" % dim.evaluate("e => getComputedStyle(e).opacity"))
    lit = page.locator('.map-stall[data-origin="indian"]').first
    ck_true("indian markers stay lit",
            float(lit.evaluate("e => getComputedStyle(e).opacity")) > 0.9)
    page.locator('.map-controls .filter-btn[for="mf-all"]').click()
    page.wait_for_timeout(200)

    print("\n[H] SCHEDULE TABS (radio + :checked)")
    page.locator('.day-tab[for="day-4"]').click()
    page.wait_for_timeout(250)
    ck_true("day 4 panel shown", page.locator('.day-panel[data-day="4"]').is_visible())
    ck_true("day 1 panel hidden", not page.locator('.day-panel[data-day="1"]').is_visible())
    ck("day 4 first event", page.locator('.day-panel[data-day="4"] h4').first.inner_text(),
       "Jewellery-Making Workshop")
    ck("day 4 event count",
       page.locator('.day-panel[data-day="4"] .event-card').count(), 3)

    print("\n[I] PASSPORT (checkbox + CSS counter)")
    page.locator('.stamp-card[data-stamp="0"]').click()
    page.wait_for_timeout(900)
    page.locator(".passport-progress").screenshot(path=os.path.join(SHOTS, "passport-1.png"))
    filled = page.evaluate("""() => [...document.querySelectorAll('.progress-seg')]
        .filter(s => new DOMMatrix(getComputedStyle(s).transform).a > 0.95).length""")
    ck("progress segments filled after 1 stamp", filled, 1)
    ck("stamp 0 label swapped", page.locator('.stamp-card[data-stamp="0"] .stamp-btn').inner_text(),
       "Stamp Collected")
    for i in (1, 2, 3):
        page.locator('.stamp-card[data-stamp="%d"]' % i).click()
    page.wait_for_timeout(250)
    page.wait_for_timeout(900)
    page.locator(".passport-progress").screenshot(path=os.path.join(SHOTS, "passport-4.png"))
    filled = page.evaluate("""() => [...document.querySelectorAll('.progress-seg')]
        .filter(s => new DOMMatrix(getComputedStyle(s).transform).a > 0.95).length""")
    ck("progress segments filled after 4 stamps", filled, 4)
    page.locator('.stamp-card[data-stamp="0"]').click()   # toggle back off
    page.wait_for_timeout(250)
    page.wait_for_timeout(900)
    page.locator(".passport-progress").screenshot(path=os.path.join(SHOTS, "passport-3.png"))

    print("\n[J] HORIZONTAL OVERFLOW (desktop)")
    ow = page.evaluate("() => document.documentElement.scrollWidth")
    ck_true("no horizontal overflow @1440", ow <= 1440, "scrollWidth=%d" % ow)

    page.screenshot(path=os.path.join(SHOTS, "desktop-full.png"), full_page=False)
    page.locator("#stalls").scroll_into_view_if_needed(); page.wait_for_timeout(600)
    page.screenshot(path=os.path.join(SHOTS, "desktop-directory.png"))
    page.locator("#map").scroll_into_view_if_needed(); page.wait_for_timeout(600)
    page.screenshot(path=os.path.join(SHOTS, "desktop-map.png"))
    page.locator("#brics-connection").scroll_into_view_if_needed(); page.wait_for_timeout(600)
    page.screenshot(path=os.path.join(SHOTS, "desktop-wheel.png"))
    page.goto(URL + "#stall-07"); page.wait_for_timeout(700)
    page.screenshot(path=os.path.join(SHOTS, "desktop-modal.png"))
    page.close()

    # ---------------------------------------------------------------
    # K. Mobile + JavaScript fully DISABLED in the browser
    # ---------------------------------------------------------------
    print("\n[K] MOBILE @390 WITH BROWSER JAVASCRIPT DISABLED")
    ctx = browser.new_context(viewport={"width": 390, "height": 844},
                              java_script_enabled=False)
    m = ctx.new_page()
    m.goto(URL)
    m.wait_for_timeout(900)
    ck("mobile: stall cards render", m.locator(".stall-card").count(), 60)
    ck_true("mobile: menu closed initially", not m.locator("#navLinks").is_visible())
    m.locator(".nav-toggle").click()
    m.wait_for_timeout(500)
    ck_true("mobile: menu opens on toggle", m.locator("#navLinks").is_visible())
    m.screenshot(path=os.path.join(SHOTS, "mobile-menu-open.png"))
    m.locator('#navLinks a[href="#schedule"]').click()
    m.wait_for_timeout(600)
    ck_true("mobile: menu auto-closes on nav link", not m.locator("#navLinks").is_visible())
    m.locator('.day-tab[for="day-6"]').click()
    m.wait_for_timeout(300)
    ck_true("mobile: schedule tabs work with JS off",
            m.locator('.day-panel[data-day="6"]').is_visible())
    m.locator('.filter-btn[for="f-jewellery"]').click()
    m.wait_for_timeout(300)
    ck("mobile: jewellery filter with JS off",
       m.locator(".stall-card:visible").count(), 5)
    m.screenshot(path=os.path.join(SHOTS, "mobile-directory.png"))
    m.goto(URL); m.wait_for_timeout(500)
    m.screenshot(path=os.path.join(SHOTS, "mobile-hero.png"))
    m.locator("#map").scroll_into_view_if_needed(); m.wait_for_timeout(600)
    m.screenshot(path=os.path.join(SHOTS, "mobile-map.png"))
    ctx.close()

    # ---------------------------------------------------------------
    # L. Tablet overflow sweep
    # ---------------------------------------------------------------
    print("\n[L] RESPONSIVE OVERFLOW SWEEP")
    for w, h in [(320, 700), (390, 844), (768, 1024), (1024, 768), (1280, 800), (1920, 1080)]:
        p2 = browser.new_page(viewport={"width": w, "height": h})
        p2.goto(URL); p2.wait_for_timeout(500)
        sw = p2.evaluate("() => document.documentElement.scrollWidth")
        ck_true("no h-overflow @%dpx" % w, sw <= w + 1, "scrollWidth=%d" % sw)
        if w in (768, 1024):
            p2.screenshot(path=os.path.join(SHOTS, "tablet-%d.png" % w))
        p2.close()

    browser.close()

print("\n" + "=" * 62)
print("%d checks run, %d failed" % (checks[0], len(fails)))
if fails:
    print("FAILED:")
    for f in fails:
        print("  - " + f)
    sys.exit(1)
print("ALL CHECKS PASSED")
