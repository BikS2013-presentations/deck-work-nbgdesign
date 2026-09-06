# Shared helper section of the briefing-look generator (icons, header, footer, pills, numbered circles,
# motif, SLIDES list and add()). Copied into this repository so the deck builds on its own;
# build.py executes it and then adds its slides on top. Companion files: base/deck.css, base/deck.js.
# Generator for the 8th AI Committee deck (nbg-design, briefing look).
# Emits deck.html with {{TOKEN}} image placeholders; embed with embed-assets.mjs.
import html as _h

ACC = "#007B85"
OUT = None   # set by the deck generator that executes this helper section

# ----------------------------------------------------------------- icons
def ico(name, size=28, stroke=ACC, sw=1.8):
    P = {
        "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8zM19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8z"/>',
        "mic": '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M8 21h8"/>',
        "doc": '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
        "code": '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13 6l-2 12"/>',
        "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
        "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V4h6v3M3 13h18"/>',
        "wallet": '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M16 14h2"/>',
        "building": '<path d="M4 21V5l8-3v19M12 9l8 3v9M8 8h1M8 12h1M8 16h1M16 15h1M16 18h1"/>',
        "chart": '<path d="M4 20h16M7 16v-5M12 16V6M17 16v-8"/>',
        "link": '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
        "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>',
        "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
        "refresh": '<path d="M20 12a8 8 0 0 1-14 5.3L4 15M4 12a8 8 0 0 1 14-5.3L20 9M4 20v-5h5M20 4v5h-5"/>',
        "db": '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
        "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="10" y="10" width="4" height="4"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
        "calc": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h2M12 12h2M16 12h0M8 16h2M12 16h2M16 16h0"/>',
        "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
        "search": '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',
        "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
        "key": '<circle cx="8" cy="14" r="4"/><path d="M11 11l9-9M16 6l2 2M13 9l2 2"/>',
        "scale": '<path d="M12 3v18M4 7h16M6 7l-3 7a3 3 0 0 0 6 0zM18 7l-3 7a3 3 0 0 0 6 0zM8 21h8"/>',
        "server": '<rect x="4" y="4" width="16" height="6" rx="1.5"/><rect x="4" y="14" width="16" height="6" rx="1.5"/><path d="M8 7h.01M8 17h.01"/>',
        "rocket": '<path d="M5 19l3-3M14 4c3 0 5 2 5 5-1 4-4 7-8 9l-4-4c2-4 5-7 7-10z"/><circle cx="14" cy="10" r="1.5"/><path d="M7 14l-3 1 2-4M10 17l-1 3 4-2"/>',
        "wrench": '<path d="M14 4a5 5 0 0 0-5.5 6.5L3 16l3 3 5.5-5.5A5 5 0 0 0 20 8l-3 3-3-3z"/>',
        "star": '<path d="M12 3l2.7 5.7 6.3.8-4.6 4.3 1.2 6.2L12 17l-5.6 3 1.2-6.2L3 9.5l6.3-.8z"/>',
        "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "users": '<circle cx="9" cy="8" r="3"/><circle cx="17" cy="9" r="2.5"/><path d="M3 20a6 6 0 0 1 12 0M15 20a5 5 0 0 1 6-4.5"/>',
        "layers": '<path d="M12 3l9 5-9 5-9-5zM3 13l9 5 9-5M3 17l9 5 9-5"/>',
        "chat": '<path d="M4 5h16v10H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
        "home": '<path d="M3 11l9-7 9 7v9H3z"/><path d="M10 20v-6h4v6"/>',
        "card": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 15h4"/>',
        "brain": '<path d="M9 4a3 3 0 0 0-3 3 3 3 0 0 0-2 5 3 3 0 0 0 2 5 3 3 0 0 0 6 0V6a2 2 0 0 0-3-2zM15 4a3 3 0 0 1 3 3 3 3 0 0 1 2 5 3 3 0 0 1-2 5 3 3 0 0 1-6 0V6a2 2 0 0 1 3-2z"/>',
        "hand": '<path d="M8 12V6a1.5 1.5 0 0 1 3 0v5M11 5a1.5 1.5 0 0 1 3 0v6M14 6a1.5 1.5 0 0 1 3 0v6M17 9a1.5 1.5 0 0 1 3 0v5a6 6 0 0 1-6 6h-2a6 6 0 0 1-5-3l-3-5a1.5 1.5 0 0 1 2.5-1.5L8 12"/>',
        "flask": '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3"/><path d="M7 16h10"/>',
        "trend": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
        "pin": '<path d="M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11z"/><circle cx="12" cy="10" r="2"/>',
        "alert": '<path d="M12 3l10 18H2z"/><path d="M12 10v4M12 17h.01"/>',
        "download": '<path d="M12 3v12M7 10l5 5 5-5M4 21h16"/>',
        "bot": '<rect x="4" y="8" width="16" height="11" rx="3"/><path d="M12 4v4M9 13h.01M15 13h.01M9 16h6"/>',
        "play": '<circle cx="12" cy="12" r="9"/><path d="M10 8l6 4-6 4z"/>',
        "steps": '<path d="M3 20h5v-5h5v-5h5V5h3"/>',
        "monitor": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
        "signal": '<path d="M12 20V10M5 8a10 10 0 0 1 14 0M8 11a6 6 0 0 1 8 0"/>',
        "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
        "cloud": '<path d="M7 18a4 4 0 0 1-.5-8A6 6 0 0 1 18 9a4 4 0 0 1 0 9z"/>',
        "handshake": '<path d="M3 10l4-4 5 3 5-3 4 4-4 5-3 3-3-1-3 1-3-3z"/><path d="M9 12l3 2 3-2"/>',
        "chev": '<path d="M9 6l6 6-6 6"/>',
        "arrow": '<path d="M4 12h16M14 6l6 6-6 6"/>',
        "satellite": '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M5 19l2-2M17 7l2-2"/>',
        "coins": '<circle cx="9" cy="9" r="6"/><path d="M15 9a6 6 0 1 1-6 6"/>',
        "vault": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="12" cy="12" r="4"/><path d="M12 10v2h2M6 20v2M18 20v2"/>',
    }
    return (f'<svg class="ico" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{P[name]}</svg>')

# ----------------------------------------------------------------- helpers
def e(s):  # escape but keep intentional <b>/<br>
    return s

def header(eyebrow, title, sub=None):
    s = f'<div class="hdr"><div class="eyebrow">{eyebrow}</div><h1 class="title">{title}</h1>'
    if sub:
        s += f'<p class="sub">{sub}</p>'
    return s + '</div>'

def footer(n, note=""):
    return (f'<div class="ftr"><div class="ftr-l"><div class="logo-small"></div>'
            f'<span class="ftr-note">{note}</span></div><span class="pg">{n}</span></div>')

def pill(text, kind="done"):
    return f'<span class="pill {kind}">{text}</span>'

def numc(n, size=44):
    return f'<span class="numc" style="width:{size}px;height:{size}px;font-size:{int(size*0.45)}px">{n}</span>'

SLIDES = []
def add(n, body, cls="", note=""):
    n = len(SLIDES) + 1  # numbering follows file order
    SLIDES.append(f'<section class="slide {cls}" data-n="{n}">{body}{footer(n, note) if cls != "cover" else ""}</section>')

AGENDA9 = ["EXECUTIVE SUMMARY", "STRATEGIC ROADMAP", "LESSONS LEARNT &amp; MITIGATION ACTIONS",
           "2026 FOCUS AREAS PROGRESS", "DEMOS", "CHANGE MANAGEMENT", "LATEST AI NEWS", "NEXT STEPS", "APPENDIX"]
AGENDA8 = ["EXECUTIVE SUMMARY", "STRATEGIC ROADMAP", "2026 FOCUS AREAS PROGRESS", "DEMOS",
           "CHANGE MANAGEMENT", "LATEST AI NEWS", "NEXT STEPS", "APPENDIX"]

def agenda(n, active=None, items=AGENDA9):
    rows = ""
    for i, it in enumerate(items, 1):
        a = " on" if i == active else ""
        rows += f'<li class="ag-item{a}"><span class="ag-num">{i:02d}</span><span class="ag-lbl">{it}</span></li>'
    body = f'''
    <div class="ag-left">
      <div class="eyebrow">8th AI Committee · Sep 2026</div>
      <div class="ag-title">Agenda</div>
      <div class="ag-rule"></div>
      <p class="ag-cap">{len(items)} sections. Orientation first, detail in the appendix.</p>
    </div>
    <div class="ag-vline"></div>
    <ul class="ag-list">{rows}</ul>'''
    add(n, body)

# ------------------------------------------------------------ motif (cover)
def motif(x, y, s=110, op=1):
    # single column of quarter-circle tiles in teal, echoing the source cover pattern
    tiles = [(0,0,0),(0,1,1),(0,2,2),(0,3,3),(0,4,0)]
    out = f'<svg class="motif" style="left:{x}px;top:{y}px;opacity:{op}" width="{s}" height="{s*5}" viewBox="0 0 {s} {s*5}">'
    for cx, cy, r in tiles:
        X, Y = cx*s, cy*s
        d = [f"M{X},{Y} h{s} a{s},{s} 0 0 1 -{s},{s} z",
             f"M{X+s},{Y} v{s} a{s},{s} 0 0 1 -{s},-{s} z",
             f"M{X+s},{Y+s} h-{s} a{s},{s} 0 0 1 {s},-{s} z",
             f"M{X},{Y+s} v-{s} a{s},{s} 0 0 1 {s},{s} z"][r]
        fill = ACC if cy % 2 == 0 else "none"
        out += f'<path d="{d}" fill="{fill}" fill-opacity="0.9" stroke="{ACC}" stroke-width="1.5"/>'
    return out + '</svg>'

