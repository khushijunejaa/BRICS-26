# -*- coding: utf-8 -*-
"""
BRICS BAZAAR 2026 — static build script.

This is a BUILD-TIME tool only. It runs on a developer machine to expand the
data that used to live in script.js into hand-written static HTML.
It is NOT shipped to the browser and the site has zero JavaScript at runtime.
"""
import math, os, html

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =====================================================================
# DATA — ported verbatim from the original script.js
# =====================================================================
COUNTRIES = [
    {"name": "India", "host": True, "crafts": "Textiles, embroidery, metalwork, pottery"},
    {"name": "Brazil", "crafts": "Textiles, basketry, indigenous crafts"},
    {"name": "Russia", "crafts": "Lacquer art, textiles, woodcraft"},
    {"name": "China", "crafts": "Ceramics, silk, paper arts"},
    {"name": "South Africa", "crafts": "Beadwork, textiles, sculpture"},
    {"name": "Egypt", "crafts": "Weaving, textiles, traditional crafts"},
    {"name": "Ethiopia", "crafts": "Textiles, basketry, jewellery"},
    {"name": "Iran", "crafts": "Carpets, ceramics, metalwork"},
    {"name": "Indonesia", "crafts": "Batik, weaving, wood carving"},
    {"name": "Saudi Arabia", "crafts": "Textiles, palm-leaf crafts, metalwork"},
    {"name": "United Arab Emirates", "crafts": "Textiles, ceramics, traditional crafts"},
]

CATEGORIES = ["Textiles", "Pottery & Ceramics", "Jewellery", "Wood & Bamboo",
              "Metal", "Craft Objects", "Food"]

INDIAN_POOL = [
    ("Gujarat", "Bandhani tie-dye textiles"), ("Rajasthan", "Blue pottery"),
    ("West Bengal", "Dokra metal casting"), ("Uttar Pradesh", "Chikankari embroidery"),
    ("Odisha", "Pattachitra painting & craft objects"), ("Kashmir", "Pashmina weaving"),
    ("Tamil Nadu", "Bronze sculpture"), ("Assam", "Bamboo & cane craft"),
    ("Madhya Pradesh", "Gond art objects"), ("Kerala", "Coir & craft objects"),
    ("Punjab", "Phulkari embroidery"), ("Bihar", "Madhubani painting"),
    ("Karnataka", "Channapatna wooden toys"), ("Maharashtra", "Warli art objects"),
    ("Himachal Pradesh", "Woollen textiles"), ("Andhra Pradesh", "Kalamkari textiles"),
    ("Delhi", "Zardozi embroidery"), ("Nagaland", "Naga tribal jewellery"),
    ("Manipur", "Handloom textiles"), ("Goa", "Terracotta pottery"),
]
INDIAN_CATS = ["Textiles","Pottery & Ceramics","Metal","Textiles","Craft Objects","Textiles","Metal","Wood & Bamboo","Craft Objects","Craft Objects","Textiles","Craft Objects","Wood & Bamboo","Craft Objects","Textiles","Textiles","Textiles","Jewellery","Textiles","Pottery & Ceramics"]
INDIAN_PRODUCTS = ["Scarves & stoles","Table & decorative ware","Figurines & décor","Kurtas & fabric yardage","Wall art & scrolls","Shawls & wraps","Statues & décor pieces","Baskets & home accents","Canvas & paper art","Mats & storage baskets","Dupattas & bedcovers","Framed paintings","Toys & décor objects","Painted panels & décor","Stoles & blankets","Yardage & cushion covers","Bridal & festive wear","Necklaces & earrings","Stoles & yardage","Planters & tableware"]

INTL_POOL = [
    ("Brazil", "Woven basketry"), ("Brazil", "Cotton hammock weaving"),
    ("Russia", "Matryoshka & lacquer art"), ("Russia", "Hand-painted shawls"),
    ("China", "Blue-and-white ceramics"), ("China", "Silk & paper-cut art"),
    ("South Africa", "Ndebele beadwork"), ("South Africa", "Wire & bead sculpture"),
    ("Egypt", "Khayamiya appliqué textiles"), ("Egypt", "Hand-woven kilims"),
    ("Ethiopia", "Handwoven cotton textiles"), ("Ethiopia", "Silver filigree jewellery"),
    ("Iran", "Hand-knotted carpets"), ("Iran", "Turquoise ceramics"),
    ("Indonesia", "Batik textile art"), ("Indonesia", "Wood carving"),
    ("Saudi Arabia", "Palm-leaf weaving"), ("Saudi Arabia", "Silver Bedouin jewellery"),
    ("United Arab Emirates", "Talli hand-braiding textiles"),
    ("United Arab Emirates", "Traditional pottery"),
]
INTL_CATS = ["Wood & Bamboo","Textiles","Craft Objects","Textiles","Pottery & Ceramics","Textiles","Jewellery","Craft Objects","Textiles","Textiles","Textiles","Jewellery","Textiles","Pottery & Ceramics","Textiles","Wood & Bamboo","Wood & Bamboo","Jewellery","Textiles","Pottery & Ceramics"]
INTL_PRODUCTS = ["Baskets & mats","Hammocks & cord work","Nesting dolls & boxes","Painted shawls","Vases & tableware","Scarves & wall panels","Beaded jewellery & décor","Wire sculptures & décor","Wall hangings & cushions","Rugs & runners","Shawls & table linen","Necklaces & cuffs","Carpets & rugs","Bowls & tiles","Wall art & garments","Carved panels & figures","Baskets & mats","Necklaces & anklets","Braided trims & textiles","Bowls & décor ware"]

ZONE_IN, ZONE_INTL = "Indian Stall Zone", "International Stall Zone"

STALLS = []
for i in range(40):
    region, craft = INDIAN_POOL[i % len(INDIAN_POOL)]
    STALLS.append({
        "id": i + 1, "country": "India", "origin": "indian",
        "name": "%s Artisan Collective %d" % (region, i // len(INDIAN_POOL) + 1),
        "craft": craft, "category": INDIAN_CATS[i % len(INDIAN_CATS)],
        "desc": "A demonstration stall from %s, showcasing %s through live demonstration and finished pieces." % (region, craft[0].lower() + craft[1:]),
        "products": INDIAN_PRODUCTS[i % len(INDIAN_PRODUCTS)], "zone": ZONE_IN,
    })
for i in range(20):
    country, craft = INTL_POOL[i % len(INTL_POOL)]
    STALLS.append({
        "id": 41 + i, "country": country, "origin": "international",
        "name": "%s Craft Pavilion %d" % (country, i // 2 + 1),
        "craft": craft, "category": INTL_CATS[i % len(INTL_CATS)],
        "desc": "A stall representing %s, presenting %s to Bazaar visitors." % (country, craft[0].lower() + craft[1:]),
        "products": INTL_PRODUCTS[i % len(INTL_PRODUCTS)], "zone": ZONE_INTL,
    })

SCHEDULE = [
    ("8 SEP", [("10:00 AM","Opening Ceremony","CEREMONY","Formal inauguration of BRICS Bazaar 2026."),
               ("12:00 PM","Cultural Performance","CULTURAL","Performances marking the opening day."),
               ("3:00 PM","Craft Demonstration Walkthrough","EXPERIENCE","Guided first look at participating stalls.")]),
    ("9 SEP", [("11:00 AM","Textile Workshop","WORKSHOP","Hands-on session on traditional weaving techniques."),
               ("2:00 PM","Artisan Talk","TALK","A participating artisan shares their craft journey."),
               ("5:00 PM","International Craft Exchange","CULTURAL","Cross-country artisan interaction session.")]),
    ("10 SEP",[("11:00 AM","Pottery Demonstration","WORKSHOP","Live demonstration of shaping and glazing techniques."),
               ("1:00 PM","Buyer–Seller Interaction","BUSINESS","Structured interaction session for trade visitors."),
               ("4:00 PM","Craft Storytelling","EXPERIENCE","Stories behind featured crafts, told by artisans.")]),
    ("11 SEP",[("11:00 AM","Jewellery-Making Workshop","WORKSHOP","Introductory session on traditional jewellery techniques."),
               ("2:00 PM","Heritage Walk","EXPERIENCE","Guided walk through the venue's craft heritage."),
               ("6:00 PM","Cultural Performance","CULTURAL","Evening performance by visiting cultural groups.")]),
    ("12 SEP",[("11:00 AM","Wood & Bamboo Craft Demonstration","WORKSHOP","Live carving and weaving demonstration."),
               ("1:00 PM","Food & Craft Experience","EXPERIENCE","Pairing regional food with craft traditions."),
               ("4:00 PM","Artisan Talk","TALK","Conversation with an international participating artisan.")]),
    ("13 SEP",[("11:00 AM","Final Craft Demonstrations","EXPERIENCE","Last chance to see live demonstrations across zones."),
               ("4:00 PM","Cultural Performance","CULTURAL","Closing cultural showcase."),
               ("6:00 PM","Closing Ceremony","CEREMONY","Formal closing of BRICS Bazaar 2026.")]),
]

STAMPS = [("🧵","India","Textiles"), ("🏺","China","Ceramics"), ("🪵","Indonesia","Wood Carving"),
          ("💍","Ethiopia","Jewellery"), ("🧺","Brazil","Basketry"), ("🎨","Iran","Carpets")]

MAP_ZONES = [
    ("entrance","Main Entrance",430,590,140,34,"var(--deep-blue)"),
    ("reception","Reception",430,520,140,50,"var(--royal-blue)"),
    ("indian","Indian Stall Zone",40,90,430,300,"var(--saffron)"),
    ("intl","International Stall Zone",520,90,430,300,"var(--royal-blue)"),
    ("demo","Craft Demonstration Area",40,410,260,90,"var(--leaf-green)"),
    ("stage","Performance / Open Stage",320,410,260,90,"var(--chili-red)"),
    ("workshop","Workshop Area",600,410,200,90,"var(--sun-yellow)"),
    ("food","Food Area",820,410,140,90,"var(--saffron)"),
    ("info","Information Desk",40,30,150,40,"var(--royal-blue)"),
    ("vip","VIP Area",810,30,150,40,"var(--deep-blue)"),
    ("rest","Rest / Pause Zone",820,520,140,50,"var(--leaf-green)"),
    ("washrooms","Washrooms",40,520,120,40,"#8a8272"),
    ("logistics","Logistics / Service Entrance",190,520,200,40,"#8a8272"),
]

# =====================================================================
# HELPERS
# =====================================================================
def e(s):
    return html.escape(str(s), quote=True)

def slug(s):
    out = s.lower().replace("&", " ").replace("/", " ")
    return "-".join(p for p in out.replace("-", " ").split() if p)

def sid(n):
    return "stall-%02d" % n

CAT_SLUGS = {c: slug(c) for c in CATEGORIES}

FILTERS = ([("all", "All", None, None), ("indian", "Indian", "origin", "indian"),
            ("international", "International", "origin", "international")] +
           [(CAT_SLUGS[c], c, "cat", CAT_SLUGS[c]) for c in CATEGORIES])

def filter_count(kind, val):
    if kind is None:
        return len(STALLS)
    if kind == "origin":
        return sum(1 for s in STALLS if s["origin"] == val)
    return sum(1 for s in STALLS if CAT_SLUGS[s["category"]] == val)

# =====================================================================
# FRAGMENT BUILDERS
# =====================================================================
def build_wheel():
    inputs, nodes, panels = [], [], []
    radius = 44.0
    for i, c in enumerate(COUNTRIES):
        ang = (i / len(COUNTRIES)) * 2 * math.pi - math.pi / 2
        x = 50 + radius * math.cos(ang)
        y = 50 + radius * math.sin(ang)
        cid = "c-%d" % i
        checked = " checked" if i == 0 else ""
        inputs.append('      <input class="ui-input" type="radio" name="country" id="%s"%s>' % (cid, checked))
        host = " host" if c.get("host") else ""
        nodes.append('          <label class="country-node%s" for="%s" style="left:%.3f%%;top:%.3f%%">%s</label>'
                     % (host, cid, x, y, e(c["name"])))
        title = e(c["name"]) + (" · Host Nation" if c.get("host") else "")
        panels.append('        <div class="country-panel" data-country="%d">\n'
                      '          <h3>%s</h3>\n          <p>%s</p>\n        </div>' % (i, title, e(c["crafts"])))
    return "\n".join(inputs), "\n".join(nodes), "\n".join(panels)


def build_stall_cards():
    out = []
    for s in STALLS:
        out.append(
            '        <article class="stall-card" data-origin="%s" data-cat="%s">\n'
            '          <div class="stall-card-top"><span class="stall-num">STALL %02d</span></div>\n'
            '          <span class="stall-tag">%s</span>\n'
            '          <h3>%s</h3>\n'
            '          <p class="stall-desc">%s</p>\n'
            '          <p class="stall-products">Example products: %s</p>\n'
            '          <span class="stall-zone">%s · %s</span>\n'
            '          <a class="stall-view-btn" href="#%s">View Stall<span class="visually-hidden"> %s</span></a>\n'
            '        </article>' % (s["origin"], CAT_SLUGS[s["category"]], s["id"], e(s["category"]),
                                    e(s["name"]), e(s["desc"]), e(s["products"]), e(s["country"]),
                                    e(s["zone"]), sid(s["id"]), e(s["name"])))
    return "\n".join(out)


def build_modals():
    out = []
    n = len(STALLS)
    for idx, s in enumerate(STALLS):
        prev_s = STALLS[idx - 1] if idx > 0 else STALLS[n - 1]
        next_s = STALLS[idx + 1] if idx < n - 1 else STALLS[0]
        out.append(
            '  <div class="stall-modal" id="%s" role="dialog" aria-labelledby="%s-title">\n'
            '    <a class="stall-modal-backdrop" href="#stalls" tabindex="-1" aria-hidden="true"></a>\n'
            '    <div class="stall-modal-card">\n'
            '      <a class="modal-close" href="#stalls" aria-label="Close stall details">&times;</a>\n'
            '      <p class="sample-flag">Sample stall information — final artisan details to be updated.</p>\n'
            '      <span class="stall-num">STALL %02d</span>\n'
            '      <h3 id="%s-title">%s</h3>\n'
            '      <p class="stall-zone">%s · %s</p>\n'
            '      <p>%s</p>\n'
            '      <dl>\n'
            '        <dt>Country</dt><dd>%s</dd>\n'
            '        <dt>Craft</dt><dd>%s</dd>\n'
            '        <dt>Category</dt><dd>%s</dd>\n'
            '        <dt>Example products</dt><dd>%s</dd>\n'
            '      </dl>\n'
            '      <p class="modal-nav">\n'
            '        <a href="#%s">&larr; Stall %02d</a>\n'
            '        <a href="#map">See on map</a>\n'
            '        <a href="#%s">Stall %02d &rarr;</a>\n'
            '      </p>\n'
            '    </div>\n'
            '  </div>' % (sid(s["id"]), sid(s["id"]), s["id"], sid(s["id"]), e(s["name"]),
                          e(s["country"]), e(s["zone"]), e(s["desc"]), e(s["country"]),
                          e(s["craft"]), e(s["category"]), e(s["products"]),
                          sid(prev_s["id"]), prev_s["id"], sid(next_s["id"]), next_s["id"]))
    return "\n".join(out)


def build_map_svg():
    parts = ['        <rect x="0" y="0" width="1000" height="640" rx="18" fill="#FBF7EF" stroke="rgba(32,27,20,0.12)"/>']
    for key, label, x, y, w, h, color in MAP_ZONES:
        parts.append(
            '        <g class="map-zone">\n'
            '          <rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" fill-opacity="0.16" stroke="%s" stroke-width="1.5"/>\n'
            '          <text x="%d" y="%d" class="map-zone-label">%s</text>\n'
            '        </g>' % (x, y, w, h, color, color, x + 10, y + 18, e(label)))
    parts.append('        <path d="M500,590 L500,520 M280,240 L500,240 L720,240" stroke="rgba(32,27,20,0.18)" '
                 'stroke-width="2" stroke-dasharray="6 6" fill="none"/>')

    zmap = {z[0]: z for z in MAP_ZONES}
    for s in STALLS:
        zone = zmap["indian"] if s["origin"] == "indian" else zmap["intl"]
        zx, zy, zw, zh = zone[2], zone[3], zone[4], zone[5]
        local = s["id"] - 1 if s["origin"] == "indian" else s["id"] - 41
        per_row = 8 if s["origin"] == "indian" else 5
        rows = 5 if s["origin"] == "indian" else 4
        col, row = local % per_row, local // per_row
        pad_x, pad_y = 28, 40
        gap_x = (zw - pad_x * 2) / (per_row - 1)
        gap_y = (zh - pad_y * 2) / (rows - 1)
        cx = zx + pad_x + col * gap_x
        cy = zy + pad_y + row * gap_y
        fill = "var(--saffron)" if s["origin"] == "indian" else "var(--royal-blue)"
        parts.append(
            '        <a href="#%s" class="map-stall-link" aria-label="Stall %d, %s">'
            '<circle cx="%.2f" cy="%.2f" r="9" class="map-stall" data-origin="%s" fill="%s" stroke="#fff" stroke-width="1.5"/></a>'
            % (sid(s["id"]), s["id"], e(s["name"]), cx, cy, s["origin"], fill))
    return "\n".join(parts)


def build_legend():
    return "\n".join(
        '          <li><span class="legend-swatch" style="background:%s"></span>%s</li>' % (color, e(label))
        for _, label, _, _, _, _, color in MAP_ZONES)


def build_schedule():
    inputs, tabs, panels = [], [], []
    for i, (label, events) in enumerate(SCHEDULE, start=1):
        did = "day-%d" % i
        checked = " checked" if i == 1 else ""
        inputs.append('      <input class="ui-input" type="radio" name="day" id="%s"%s>' % (did, checked))
        tabs.append('        <label class="day-tab" for="%s">%s</label>' % (did, e(label)))
        cards = []
        for time, title, tag, desc in events:
            cards.append(
                '          <article class="event-card">\n'
                '            <span class="event-tag tag-%s">%s</span>\n'
                '            <span class="event-time">%s</span>\n'
                '            <h4>%s</h4>\n'
                '            <p>%s</p>\n'
                '          </article>' % (tag, tag, e(time), e(title), e(desc)))
        panels.append('        <div class="day-panel" data-day="%d" aria-label="Events on %s">\n%s\n        </div>'
                      % (i, e(label), "\n".join(cards)))
    return "\n".join(inputs), "\n".join(tabs), "\n".join(panels)


def build_stamps():
    inputs, cards = [], []
    for i, (icon, country, craft) in enumerate(STAMPS):
        pid = "stamp-%d" % i
        inputs.append('      <input class="ui-input stamp-input" type="checkbox" id="%s">' % pid)
        cards.append(
            '        <label class="stamp-card" for="%s" data-stamp="%d">\n'
            '          <span class="stamp-icon" aria-hidden="true">%s</span>\n'
            '          <h4>%s</h4>\n'
            '          <p>%s</p>\n'
            '          <span class="stamp-btn"><span class="stamp-btn-collect">Collect Stamp</span>'
            '<span class="stamp-btn-done">Stamp Collected</span></span>\n'
            '        </label>' % (pid, i, icon, e(country), e(craft)))
    segs = "\n".join('          <span class="progress-seg" data-seg="%d"></span>' % i for i in range(len(STAMPS)))
    return "\n".join(inputs), "\n".join(cards), segs


def build_filter_inputs():
    return "\n".join(
        '      <input class="ui-input" type="radio" name="stallfilter" id="f-%s"%s>' % (fid, " checked" if fid == "all" else "")
        for fid, _, _, _ in FILTERS)


def build_filter_labels():
    return "\n".join(
        '          <label class="filter-btn" for="f-%s">%s</label>' % (fid, e(label))
        for fid, label, _, _ in FILTERS)


def build_result_counts():
    out = []
    for fid, _, kind, val in FILTERS:
        n = filter_count(kind, val)
        out.append('      <p class="results-count" data-filter="%s">Showing %d of %d stalls</p>' % (fid, n, len(STALLS)))
    return "\n".join(out)


# =====================================================================
# CSS — generated state rules for the repetitive, data-driven controls
# =====================================================================
def build_css():
    L = []
    A = L.append
    A("/* =================================================================")
    A("   CSS-ONLY INTERACTION LAYER")
    A("   Generated state rules for the controls that were previously driven")
    A("   by scripting. Every rule below is plain CSS.")
    A("   ================================================================= */")
    A("")
    A("/* Hidden but focusable inputs that carry all interactive state. */")
    A(".ui-input{ position:absolute; opacity:0; width:1px; height:1px; margin:0; pointer-events:none; }")
    A(".ui-scope{ position:relative; }")
    A("")

    A("/* ---------------- Country wheel ---------------- */")
    A(".country-node{ cursor:pointer; user-select:none; }")
    A(".country-panel{ display:none; }")
    A(".country-panel h3{ color: var(--deep-blue); margin-bottom:6px; }")
    A(".country-panel p{ color: var(--ink-soft); margin:0; }")
    for i in range(len(COUNTRIES)):
        A('#c-%d:checked ~ .wheel-wrap .country-node[for="c-%d"]{ transform: scale(1.12); background: var(--chili-red); color:#fff; box-shadow: var(--shadow-hover); z-index:3; }' % (i, i))
    A(".country-node.host{ background: var(--sun-yellow); border-color: var(--saffron); }")
    for i in range(len(COUNTRIES)):
        A('#c-%d:checked ~ .country-detail .country-panel[data-country="%d"]{ display:block; }' % (i, i))
    for i in range(len(COUNTRIES)):
        A('#c-%d:focus-visible ~ .wheel-wrap .country-node[for="c-%d"]{ outline:3px solid var(--saffron); outline-offset:3px; }' % (i, i))
    A("")

    A("/* ---------------- Directory filters ---------------- */")
    A(".filter-btn{ cursor:pointer; user-select:none; display:inline-block; }")
    A(".results-count{ display:none; }")
    A(".no-results{ display:none; }")
    for fid, _, kind, val in FILTERS:
        A('#f-%s:checked ~ .directory-controls .filter-btn[for="f-%s"]{ background: var(--deep-blue); border-color: var(--deep-blue); color:#fff; }' % (fid, fid))
        A('#f-%s:focus-visible ~ .directory-controls .filter-btn[for="f-%s"]{ outline:3px solid var(--saffron); outline-offset:3px; }' % (fid, fid))
        A('#f-%s:checked ~ .results-count[data-filter="%s"]{ display:block; }' % (fid, fid))
        if kind == "origin":
            A('#f-%s:checked ~ .stall-grid .stall-card:not([data-origin="%s"]){ display:none; }' % (fid, val))
        elif kind == "cat":
            A('#f-%s:checked ~ .stall-grid .stall-card:not([data-cat="%s"]){ display:none; }' % (fid, val))
        if filter_count(kind, val) == 0:
            A('#f-%s:checked ~ .no-results{ display:block; }' % fid)
    A("")

    A("/* ---------------- Map filters ---------------- */")
    A('#mf-indian:checked ~ .map-layout .map-stall[data-origin="international"],')
    A('#mf-international:checked ~ .map-layout .map-stall[data-origin="indian"]{ opacity:.15; }')
    for mid in ("all", "indian", "international"):
        A('#mf-%s:checked ~ .map-controls .filter-btn[for="mf-%s"]{ background: var(--deep-blue); border-color: var(--deep-blue); color:#fff; }' % (mid, mid))
        A('#mf-%s:focus-visible ~ .map-controls .filter-btn[for="mf-%s"]{ outline:3px solid var(--saffron); outline-offset:3px; }' % (mid, mid))
    A("")

    A("/* ---------------- Schedule day tabs ---------------- */")
    A(".day-tab{ cursor:pointer; user-select:none; display:inline-block; }")
    A(".day-panel{ display:none; }")
    for i in range(1, len(SCHEDULE) + 1):
        A('#day-%d:checked ~ .day-tabs .day-tab[for="day-%d"]{ background: var(--deep-blue); border-color: var(--deep-blue); color:#fff; }' % (i, i))
        A('#day-%d:focus-visible ~ .day-tabs .day-tab[for="day-%d"]{ outline:3px solid var(--saffron); outline-offset:3px; }' % (i, i))
        A('#day-%d:checked ~ .day-panels .day-panel[data-day="%d"]{ display:grid; }' % (i, i))
    A("")

    A("/* ---------------- Heritage Craft Passport ---------------- */")
    A("/* The count is produced by a CSS counter incremented by each checked")
    A("   stamp input — no scripting, no persistence across reloads. */")
    A(".passport-block{ counter-reset: stamps; }")
    A(".stamp-input:checked{ counter-increment: stamps; }")
    A('#passportCount::after{ content: counter(stamps) " / %d"; }' % len(STAMPS))
    A(".progress-track{ display:flex; gap:0; }")
    A(".progress-seg{ flex:1 1 0; height:100%; transform: scaleX(0); transform-origin:left center;")
    A("  transition: transform .5s ease; background: linear-gradient(90deg, var(--saffron), var(--chili-red));")
    A("  background-size: %d00%% 100%%; }" % len(STAMPS))
    for i in range(len(STAMPS)):
        pos = 0 if len(STAMPS) == 1 else (i / (len(STAMPS) - 1)) * 100
        A('.progress-seg[data-seg="%d"]{ background-position: %.1f%% 0; }' % (i, pos))
        A('#stamp-%d:checked ~ .passport-progress .progress-seg[data-seg="%d"]{ transform: scaleX(1); }' % (i, i))
        A('#stamp-%d:checked ~ .stamp-grid .stamp-card[data-stamp="%d"]{ border-style:solid; border-color: var(--leaf-green); background: rgba(46,139,79,.06); }' % (i, i))
        A('#stamp-%d:checked ~ .stamp-grid .stamp-card[data-stamp="%d"] .stamp-btn{ background: var(--leaf-green); border-color: var(--leaf-green); color:#fff; }' % (i, i))
        A('#stamp-%d:checked ~ .stamp-grid .stamp-card[data-stamp="%d"] .stamp-btn-collect{ display:none; }' % (i, i))
        A('#stamp-%d:checked ~ .stamp-grid .stamp-card[data-stamp="%d"] .stamp-btn-done{ display:inline; }' % (i, i))
        A('#stamp-%d:focus-visible ~ .stamp-grid .stamp-card[data-stamp="%d"]{ outline:3px solid var(--saffron); outline-offset:3px; }' % (i, i))
    A(".stamp-btn-done{ display:none; }")
    A("")
    return "\n".join(L) + "\n"


# =====================================================================
# PAGE ASSEMBLY
# =====================================================================
def build_html():
    wheel_inputs, wheel_nodes, wheel_panels = build_wheel()
    day_inputs, day_tabs, day_panels = build_schedule()
    stamp_inputs, stamp_cards, stamp_segs = build_stamps()

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BRICS Bazaar 2026 — Crafting Cultures, Connecting Peoples</title>
<meta name="description" content="BRICS Bazaar 2026 — 8-13 September, National Crafts Museum &amp; Hastkala Academy, New Delhi. 60 craft stalls from India and BRICS nations.">

<!-- Fonts: Fraunces (editorial serif for headings), Work Sans (body), IBM Plex Mono (labels/data) -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500&amp;family=Work+Sans:wght@300;400;500;600;700&amp;family=IBM+Plex+Mono:wght@400;500;600&amp;display=swap" rel="stylesheet">

<link rel="stylesheet" href="style.css">
</head>
<body>

<!-- ============================================= -->
<!-- SKIP LINK / ACCESSIBILITY                      -->
<!-- ============================================= -->
<a class="skip-link" href="#main">Skip to main content</a>

<!-- ============================================= -->
<!-- NAVIGATION                                     -->
<!-- Mobile menu is opened with :target (a plain    -->
<!-- anchor). Following any nav link moves :target  -->
<!-- to that section, which closes the menu.        -->
<!-- ============================================= -->
<header class="site-header" id="site-header">
  <nav class="navbar" aria-label="Primary">
    <a href="#home" class="nav-brand">
      <!-- UPDATE LOGO HERE: replace this mark with the official BRICS India 2026 logo image -->
      <span class="brand-mark" aria-hidden="true">
        <span class="mark-dot mark-1"></span><span class="mark-dot mark-2"></span><span class="mark-dot mark-3"></span><span class="mark-dot mark-4"></span><span class="mark-dot mark-5"></span>
      </span>
      <span class="brand-text">BRICS BAZAAR <em>2026</em></span>
    </a>

    <a class="nav-toggle" href="#navLinks" aria-label="Open navigation menu">
      <span></span><span></span><span></span>
    </a>
    <a class="nav-close" href="#site-header" aria-label="Close navigation menu">&times;</a>

    <ul class="nav-links" id="navLinks">
      <li><a href="#home">Home</a></li>
      <li><a href="#about">About</a></li>
      <li><a href="#stalls">Explore Stalls</a></li>
      <li><a href="#map">Map</a></li>
      <li><a href="#schedule">Events</a></li>
      <li><a href="#experiences">Experiences</a></li>
      <li><a href="#visitor-info">Visitor Info</a></li>
    </ul>
    <a href="#stalls" class="btn btn-primary nav-cta">Explore the Bazaar</a>
  </nav>
</header>

<main id="main">

<!-- ============================================= -->
<!-- 1. HERO                                        -->
<!-- ============================================= -->
<section class="hero" id="home">
  <div class="hero-threads" aria-hidden="true">
    <svg viewBox="0 0 1200 800" preserveAspectRatio="none" class="thread-svg">
      <path class="thread thread-blue" d="M-50,600 C250,500 350,700 600,550 C850,400 950,600 1250,450"/>
      <path class="thread thread-green" d="M-50,500 C250,650 400,350 650,480 C900,600 1000,350 1250,500"/>
      <path class="thread thread-yellow" d="M-50,680 C300,550 450,750 700,600 C950,450 1050,650 1250,550"/>
      <path class="thread thread-orange" d="M-50,420 C300,380 400,520 680,430 C920,360 1020,480 1250,400"/>
      <path class="thread thread-red" d="M-50,750 C280,700 500,780 720,700 C960,620 1080,720 1250,680"/>
    </svg>
  </div>

  <div class="hero-inner container">
    <p class="eyebrow reveal">National Crafts Museum &amp; Hastkala Academy · New Delhi</p>
    <h1 class="hero-title reveal">
      BRICS <span class="hero-title-accent">Bazaar</span><br>2026
    </h1>
    <p class="hero-theme reveal">Crafting Cultures, Connecting Peoples</p>

    <div class="hero-meta reveal">
      <div class="hero-meta-item">
        <span class="hero-meta-label">Dates</span>
        <span class="hero-meta-value">8 – 13 September 2026</span>
      </div>
      <div class="hero-meta-divider" aria-hidden="true"></div>
      <div class="hero-meta-item">
        <span class="hero-meta-label">Venue</span>
        <span class="hero-meta-value">National Crafts Museum &amp; Hastkala Academy, New Delhi</span>
      </div>
    </div>

    <div class="hero-actions reveal">
      <a href="#stalls" class="btn btn-primary">Explore the Bazaar</a>
      <a href="#map" class="btn btn-outline">View the Map</a>
    </div>

    <p class="hero-note reveal">Concept / prototype website. Event details below marked as sample are indicative and subject to confirmation.</p>
  </div>
</section>

<!-- ============================================= -->
<!-- 2. EVENT STATISTICS                            -->
<!-- Counters are static numbers (the animated      -->
<!-- count-up required JavaScript).                 -->
<!-- ============================================= -->
<section class="stats" aria-label="Event statistics">
  <div class="container stats-grid">
    <div class="stat-card reveal">
      <span class="stat-number">60</span>
      <span class="stat-label">Craft Stalls</span>
    </div>
    <div class="stat-card reveal">
      <span class="stat-number">40</span>
      <span class="stat-label">Indian Stalls</span>
    </div>
    <div class="stat-card reveal">
      <span class="stat-number">20</span>
      <span class="stat-label">International Stalls</span>
    </div>
    <div class="stat-card reveal">
      <span class="stat-number">6</span>
      <span class="stat-label">Days of Cultural Exchange</span>
    </div>
  </div>
</section>

<!-- ============================================= -->
<!-- 3. ABOUT THE BAZAAR                            -->
<!-- ============================================= -->
<section class="about" id="about">
  <div class="container about-grid">
    <div class="about-copy reveal">
      <p class="section-eyebrow">About the Bazaar</p>
      <h2 class="section-title">Where Cultures Meet Through Craft</h2>
      <p class="lede">BRICS Bazaar 2026 brings craftspeople from India and across the BRICS nations into one shared space — for six days, a single courtyard becomes a meeting point for hands that shape cloth, clay, metal and wood in very different ways, but toward the same human impulse: to make something meaningful.</p>
      <p>Every stall carries a story before it carries a product. A weave pattern passed through three generations. A glaze recipe kept in a family notebook. A form drawn from a local landscape rather than a catalogue. The Bazaar exists to let visitors encounter that knowledge directly — to ask a question, watch a technique in progress, and understand a craft as a living practice rather than a finished object on a shelf.</p>
      <p>For India, hosting the Bazaar is an opportunity to place its own artisan traditions in conversation with those of Brazil, Russia, China, South Africa and the wider BRICS membership — each bringing distinct materials, motifs and methods shaped by their own geography and history. What emerges is not a single narrative but many, side by side, open to discovery.</p>
      <p>Visitors are invited to participate rather than simply observe: through the stalls, the demonstrations, the Heritage Craft Passport and the Mystery Craft Box, the Bazaar is designed as an experience to move through, not a directory to scroll past.</p>
    </div>
    <div class="about-visual reveal" aria-hidden="true">
      <div class="about-frame">
        <div class="about-motif"></div>
        <div class="about-caption">
          <span class="mono-label">Est. 2026</span>
          <span>Six days · One courtyard<br>Eleven nations of craft</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ============================================= -->
<!-- 4. BRICS CULTURAL CONNECTION                   -->
<!-- Country nodes are <label>s for hidden radio    -->
<!-- inputs; :checked reveals the matching panel.   -->
<!-- ============================================= -->
<section class="brics-wheel" id="brics-connection">
  <div class="container">
    <p class="section-eyebrow center">The BRICS Cultural Connection</p>
    <h2 class="section-title center">Eleven Nations, One Craft Table</h2>
    <p class="section-intro center">Select a country to see the broad craft traditions it brings to the Bazaar. Descriptions are general cultural categories, not an official or exhaustive listing.</p>

    <div class="wheel-block ui-scope">
{wheel_inputs}

      <div class="wheel-wrap">
        <div class="wheel-center">
          <span class="wheel-center-label">BRICS<br>BAZAAR<br>2026</span>
        </div>
        <div class="wheel-ring">
{wheel_nodes}
        </div>
      </div>

      <div class="country-detail">
{wheel_panels}
      </div>
    </div>
  </div>
</section>

<!-- ============================================= -->
<!-- 5. STALL / ARTISAN DIRECTORY                   -->
<!-- All 60 stalls are written out as static cards. -->
<!-- Filtering is hidden radio inputs + :checked.   -->
<!-- ============================================= -->
<section class="directory" id="stalls">
  <div class="container">
    <p class="section-eyebrow center">Stall &amp; Artisan Directory</p>
    <h2 class="section-title center">Sixty Stalls, One Bazaar</h2>
    <p class="sample-flag center">Sample stall information — final artisan details to be updated.</p>

    <div class="directory-filterable ui-scope">
{filter_inputs}

      <div class="directory-controls">
        <form class="search-field" role="search" action="#stalls" method="get">
          <label for="stallSearch" class="visually-hidden">Search stall, artisan, craft or product</label>
          <input type="search" id="stallSearch" name="q" placeholder="Search stall / artisan / craft / product">
        </form>
        <p class="placeholder-note search-note">Text search needs a server-side search service and is not wired up in this static build. Use the category filters below to browse all 60 stalls.</p>
        <div class="filter-row" role="group" aria-label="Filter stalls">
{filter_labels}
        </div>
      </div>

{result_counts}

      <div class="stall-grid">
{stall_cards}
      </div>
      <p class="no-results">No stalls are listed in this category yet.</p>
    </div>
  </div>
</section>

<!-- ============================================= -->
<!-- Stall detail modals — one per stall, revealed  -->
<!-- by :target. Position:fixed, so they never      -->
<!-- affect page flow.                              -->
<!-- ============================================= -->
<div class="stall-modals">
{modals}
</div>

<!-- ============================================= -->
<!-- 6. VENUE SITE PLAN                             -->
<!-- Static SVG. Stall markers are real links that  -->
<!-- open the matching stall modal.                 -->
<!-- ============================================= -->
<section class="site-map" id="map">
  <div class="container">
    <p class="section-eyebrow center">Venue Site Plan</p>
    <h2 class="section-title center">Find Your Way Around</h2>
    <p class="sample-flag center">Stylised event site plan — not a geographically precise survey map. Zone positions are indicative.</p>

    <div class="map-block ui-scope">
      <input class="ui-input" type="radio" name="mapfilter" id="mf-all" checked>
      <input class="ui-input" type="radio" name="mapfilter" id="mf-indian">
      <input class="ui-input" type="radio" name="mapfilter" id="mf-international">

      <div class="map-controls">
        <div class="filter-row" role="group" aria-label="Filter map stalls">
          <label class="filter-btn" for="mf-all">All Stalls</label>
          <label class="filter-btn" for="mf-indian">India</label>
          <label class="filter-btn" for="mf-international">International</label>
        </div>
        <p class="placeholder-note map-note">Select any stall marker on the plan to open its details.</p>
      </div>

      <div class="map-layout">
        <div class="map-canvas-wrap">
          <svg viewBox="0 0 1000 640" class="map-canvas" role="img" aria-label="Site plan of the BRICS Bazaar venue showing zones and all 60 stall positions">
{map_svg}
          </svg>
        </div>
        <aside class="map-legend">
          <h3>Legend</h3>
          <ul>
{legend}
          </ul>
          <div class="map-selection">
            <p class="map-selection-hint">Stall markers are links — select one on the plan to open its full details, or browse the <a href="#stalls">stall directory</a>.</p>
          </div>
        </aside>
      </div>
    </div>
  </div>
</section>

<!-- ============================================= -->
<!-- 7. EVENT SCHEDULE                              -->
<!-- Day tabs are hidden radio inputs + <label>s.   -->
<!-- ============================================= -->
<section class="schedule" id="schedule">
  <div class="container">
    <p class="section-eyebrow center">Event Schedule</p>
    <h2 class="section-title center">Six Days of Craft &amp; Culture</h2>
    <p class="sample-flag center">Indicative schedule — timings and events subject to confirmation.</p>

    <div class="schedule-block ui-scope">
{day_inputs}

      <div class="day-tabs" role="group" aria-label="Select a day">
{day_tabs}
      </div>

      <div class="day-panels">
{day_panels}
      </div>
    </div>
  </div>
</section>

<!-- ============================================= -->
<!-- EXPERIENCES: MYSTERY CRAFT BOX + PASSPORT      -->
<!-- ============================================= -->
<div id="experiences">

<!-- 8. MYSTERY CRAFT BOX -->
<section class="mystery-box">
  <div class="container">
    <p class="section-eyebrow center">A Concept Experience</p>
    <h2 class="section-title center">Discover a Craft. Take Home a Story.</h2>
    <p class="section-intro center">The BRICS Mystery Craft Box is a curated take-home concept: choose a tier, and receive a hand-selected craft item inspired by the artisans of the Bazaar — with the maker's story included.</p>
    <p class="sample-flag center">Concept / sample pricing shown below — final pricing and contents to be confirmed.</p>

    <div class="box-tiers" id="box-tiers">
      <article class="box-card reveal">
        <span class="mono-label">Tier 01</span>
        <h3>Small</h3>
        <p class="box-price">₹999 <span>sample price</span></p>
        <p>A single small craft object with an artisan story card.</p>
      </article>
      <article class="box-card box-card-featured reveal">
        <span class="mono-label">Tier 02</span>
        <h3>Medium</h3>
        <p class="box-price">₹1,999 <span>sample price</span></p>
        <p>A curated pair of craft objects spanning two techniques or regions.</p>
      </article>
      <article class="box-card reveal">
        <span class="mono-label">Tier 03</span>
        <h3>Premium</h3>
        <p class="box-price">₹3,999 <span>sample price</span></p>
        <p>A larger curated selection, including a signature piece from a featured stall.</p>
      </article>
    </div>

    <ol class="box-steps reveal">
      <li><span class="step-num">1</span><span>Choose your box</span></li>
      <li><span class="step-num">2</span><span>Open the discovery</span></li>
      <li><span class="step-num">3</span><span>Meet the craft</span></li>
      <li><span class="step-num">4</span><span>Learn the artisan story</span></li>
    </ol>

    <div class="center">
      <a class="btn btn-primary" href="#box-tiers">Discover the Box</a>
    </div>
  </div>
</section>

<!-- 9. HERITAGE CRAFT PASSPORT -->
<!-- Stamps are checkboxes; the count is a CSS      -->
<!-- counter. State is visual only and resets on    -->
<!-- reload — it is not stored anywhere.            -->
<section class="passport" id="passport">
  <div class="container">
    <p class="section-eyebrow center">A Concept Experience</p>
    <h2 class="section-title center">Heritage Craft Passport</h2>
    <p class="section-intro center">Discover a stall, visit in person, collect a stamp, and learn the story behind the craft. A prototype interaction — the real passport will accompany your Bazaar visit.</p>

    <div class="passport-block ui-scope">
{stamp_inputs}

      <div class="passport-progress">
        <span id="passportCount"></span> CRAFTS DISCOVERED
        <div class="progress-track" aria-hidden="true">
{stamp_segs}
        </div>
      </div>

      <div class="stamp-grid">
{stamp_cards}
      </div>
    </div>

    <p class="placeholder-note center passport-note">Stamps are a visual prototype only — your selection is not saved and clears when the page reloads.</p>

    <div class="center">
      <a class="btn btn-outline" href="index.html?start=1#passport">Start Your Craft Journey</a>
    </div>
  </div>
</section>

</div><!-- /#experiences -->

<!-- ============================================= -->
<!-- 10. VISITOR INFORMATION                        -->
<!-- ============================================= -->
<section class="visitor-info" id="visitor-info">
  <div class="container">
    <p class="section-eyebrow center">Visitor Information</p>
    <h2 class="section-title center">Planning Your Visit</h2>

    <div class="quick-facts reveal">
      <div><span class="mono-label">Dates</span><span>8 – 13 September 2026</span></div>
      <div><span class="mono-label">Venue</span><span>National Crafts Museum &amp; Hastkala Academy, New Delhi, India</span></div>
      <div><span class="mono-label">Stalls</span><span>60 total</span></div>
      <div><span class="mono-label">Indian</span><span>40 stalls</span></div>
      <div><span class="mono-label">International</span><span>20 stalls</span></div>
    </div>

    <div class="info-grid">
      <article class="info-card reveal"><h3>Getting Here</h3><p>Details to be announced.</p></article>
      <article class="info-card reveal"><h3>Opening Hours</h3><p>Details to be announced.</p></article>
      <article class="info-card reveal"><h3>Accessibility</h3><p>Details to be announced.</p></article>
      <article class="info-card reveal"><h3>Information Desk</h3><p>Details to be announced.</p></article>
      <article class="info-card reveal"><h3>Food &amp; Refreshments</h3><p>Details to be announced.</p></article>
      <article class="info-card reveal"><h3>Facilities</h3><p>Details to be announced.</p></article>
      <article class="info-card reveal"><h3>Visitor Assistance</h3><p>Details to be announced.</p></article>
    </div>
  </div>
</section>

<!-- ============================================= -->
<!-- 11. VENUE                                      -->
<!-- ============================================= -->
<section class="venue">
  <div class="container venue-grid">
    <div class="reveal">
      <p class="section-eyebrow">The Venue</p>
      <h2 class="section-title">National Crafts Museum &amp; Hastkala Academy</h2>
      <p>New Delhi, India</p>
      <p>The National Crafts Museum &amp; Hastkala Academy is home to one of India's most significant collections of craft and folk art, set within courtyards and pavilions designed to house exactly this kind of living craft exchange. For six days, its grounds host the stalls, demonstrations and performances of BRICS Bazaar 2026.</p>
      <p class="placeholder-note">Directions and transport details to be announced.</p>
      <a href="#map" class="btn btn-outline">Explore Site Map</a>
    </div>
    <div class="venue-preview reveal" aria-hidden="true">
      <div class="venue-preview-frame">
        <svg viewBox="0 0 300 220" class="venue-mini-map">
          <rect x="10" y="10" width="280" height="200" rx="10" class="venue-mini-bg"/>
          <rect x="30" y="30" width="110" height="70" rx="6" class="venue-mini-zone zone-india"/>
          <rect x="160" y="30" width="110" height="70" rx="6" class="venue-mini-zone zone-intl"/>
          <rect x="30" y="120" width="240" height="40" rx="6" class="venue-mini-zone zone-stage"/>
          <rect x="30" y="170" width="110" height="30" rx="6" class="venue-mini-zone zone-food"/>
          <rect x="160" y="170" width="110" height="30" rx="6" class="venue-mini-zone zone-info"/>
        </svg>
      </div>
    </div>
  </div>
</section>

</main>

<!-- ============================================= -->
<!-- FOOTER                                         -->
<!-- ============================================= -->
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <span class="brand-mark" aria-hidden="true">
        <span class="mark-dot mark-1"></span><span class="mark-dot mark-2"></span><span class="mark-dot mark-3"></span><span class="mark-dot mark-4"></span><span class="mark-dot mark-5"></span>
      </span>
      <div>
        <p class="footer-title">BRICS BAZAAR 2026</p>
        <p class="footer-theme">Crafting Cultures, Connecting Peoples</p>
      </div>
    </div>

    <div class="footer-meta">
      <p>8 – 13 September 2026</p>
      <p>National Crafts Museum &amp; Hastkala Academy, New Delhi</p>
    </div>

    <nav class="footer-nav" aria-label="Footer">
      <a href="#home">Home</a>
      <a href="#about">About</a>
      <a href="#stalls">Explore Stalls</a>
      <a href="#map">Map</a>
      <a href="#schedule">Events</a>
      <a href="#experiences">Experiences</a>
      <a href="#visitor-info">Visitor Info</a>
    </nav>
  </div>
  <div class="container footer-bottom">
    <p>Concept Website / Prototype — informational content marked as sample or indicative is not officially confirmed.</p>
  </div>
</footer>

</body>
</html>
""".replace("{wheel_inputs}", wheel_inputs) \
   .replace("{wheel_nodes}", wheel_nodes) \
   .replace("{wheel_panels}", wheel_panels) \
   .replace("{filter_inputs}", build_filter_inputs()) \
   .replace("{filter_labels}", build_filter_labels()) \
   .replace("{result_counts}", build_result_counts()) \
   .replace("{stall_cards}", build_stall_cards()) \
   .replace("{modals}", build_modals()) \
   .replace("{map_svg}", build_map_svg()) \
   .replace("{legend}", build_legend()) \
   .replace("{day_inputs}", day_inputs) \
   .replace("{day_tabs}", day_tabs) \
   .replace("{day_panels}", day_panels) \
   .replace("{stamp_inputs}", stamp_inputs) \
   .replace("{stamp_cards}", stamp_cards) \
   .replace("{stamp_segs}", stamp_segs)


if __name__ == "__main__":
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_html())
    # The CSS interaction layer already lives inside style.css. It is only
    # re-emitted here (to build/_generated.css, for manual diffing) if the
    # number of countries, filters, schedule days or stamps changes, since
    # those counts determine how many state rules are needed.
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_generated.css"), "w", encoding="utf-8") as f:
        f.write(build_css())
    print("index.html written.")
    print("NOTE: style.css is maintained by hand. build/_generated.css is a")
    print("      reference dump — only merge it into style.css if the counts")
    print("      printed below have changed.")
    print("stalls:", len(STALLS), "| countries:", len(COUNTRIES), "| days:", len(SCHEDULE),
          "| stamps:", len(STAMPS), "| zones:", len(MAP_ZONES))
    for fid, label, kind, val in FILTERS:
        print("  filter %-20s %d" % (fid, filter_count(kind, val)))
