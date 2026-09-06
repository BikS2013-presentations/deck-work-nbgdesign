# Five diagrams explaining the nbg-design skill, drawn with the diagram-design skill's grammar
# (NBG skin: white paper, dark-teal ink, aqua accent, all-Aptos; 4px grid; orthogonal connectors
# with r=8 corners; masked arrow labels with a 6-10px gap; legend strip at the bottom).
# Each diagram is a 1760x640 SVG that fits the deck's body area at 1:1 artboard pixels.
import os

PAPER, PAPER2 = "#FFFFFF", "#F5F8F6"
INK, MUTED, SOFT = "#003841", "#595959", "#939793"
RULE, RULE_SOLID = "rgba(0,56,65,0.12)", "#BEC1BE"
ACC, ACC_TINT, LINK = "#00ADBF", "rgba(0,173,191,0.22)", "#0D90FF"
FONT = "Aptos, Inter, 'Segoe UI', Helvetica, Arial, sans-serif"
W, H = 1760, 640

def ink(a): return f"rgba(0,56,65,{a})"

def svg_open(slug, title, desc):
    return (f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-labelledby="{slug}-title {slug}-desc" font-family="{FONT}">'
            f'<title id="{slug}-title">{title}</title><desc id="{slug}-desc">{desc}</desc>'
            f'<defs>'
            f'<marker id="{slug}-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{MUTED}"/></marker>'
            f'<marker id="{slug}-arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{ACC}"/></marker>'
            f'<marker id="{slug}-arrow-link" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="{LINK}"/></marker>'
            f'</defs><rect width="100%" height="100%" fill="{PAPER}"/>')

def text(x, y, s, size=20, weight=400, fill=INK, anchor="middle", track=None, italic=False):
    ls = f' letter-spacing="{track}"' if track else ""
    it = ' font-style="italic"' if italic else ""
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{ls}{it}>{s}</text>'

def eyebrow(x, y, s, fill=MUTED, anchor="start"):
    return text(x, y, s, 12, 400, fill, anchor, "0.14em")

def node(x, y, w, h, name, sub=None, kind="backend", tag=None, sub2=None):
    fill, stroke, dash = {
        "focal": (ACC_TINT, ACC, ""), "backend": (PAPER, INK, ""), "store": (ink(0.05), MUTED, ""),
        "external": (ink(0.03), ink(0.30), ""), "input": ("rgba(89,89,89,0.10)", SOFT, ""),
        "optional": (ink(0.02), ink(0.20), ' stroke-dasharray="4,3"'),
    }[kind]
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER}"/>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1"{dash}/>'
    cx = x + w // 2
    if tag:
        tw = 12 + 8 * len(tag)
        s += f'<rect x="{x+8}" y="{y+8}" width="{tw}" height="16" rx="2" fill="transparent" stroke="{stroke}" stroke-opacity="0.4" stroke-width="0.8"/>'
        s += text(x + 8 + tw // 2, y + 20, tag, 12, 400, stroke, "middle", "0.08em")
    lines = [l for l in (sub, sub2) if l]
    ny = y + h // 2 + (8 if not lines else (2 if len(lines) == 1 else -6))
    s += text(cx, ny, name, 20, 600, INK)
    for i, l in enumerate(lines):
        s += text(cx, ny + 24 + 20 * i, l, 16, 400, MUTED)
    return s

def label(cx, cy, s, fill=MUTED, size=12):
    """Masked arrow label centred at (cx, cy) — cy is the text baseline; the mask spans cy-12..cy+4."""
    w = int(round(size * 0.62 * len(s) / 4)) * 4 + 16
    return (f'<rect x="{cx - w // 2}" y="{cy - 12}" width="{w}" height="16" rx="2" fill="{PAPER}"/>'
            + text(cx, cy, s, size, 400, fill, "middle", "0.06em"))

def label_left(x, cy, s, fill=MUTED, size=12):
    w = int(round(size * 0.62 * len(s) / 4)) * 4 + 16
    return (f'<rect x="{x}" y="{cy - 12}" width="{w}" height="16" rx="2" fill="{PAPER}"/>'
            + text(x + 8, cy, s, size, 400, fill, "start", "0.06em"))

def legend(slug, items, y=556):
    s = f'<line x1="40" y1="{y}" x2="{W-40}" y2="{y}" stroke="{ink(0.10)}" stroke-width="0.8"/>'
    s += eyebrow(40, y + 24, "LEGEND")
    x = 160
    for kind, t in items:
        if kind == "swatch-focal":
            s += f'<rect x="{x}" y="{y+36}" width="20" height="14" rx="2" fill="{ACC_TINT}" stroke="{ACC}" stroke-width="1"/>'
        elif kind == "swatch-store":
            s += f'<rect x="{x}" y="{y+36}" width="20" height="14" rx="2" fill="{ink(0.05)}" stroke="{MUTED}" stroke-width="1"/>'
        elif kind == "swatch-external":
            s += f'<rect x="{x}" y="{y+36}" width="20" height="14" rx="2" fill="{ink(0.03)}" stroke="{ink(0.30)}" stroke-width="1"/>'
        elif kind == "swatch-input":
            s += f'<rect x="{x}" y="{y+36}" width="20" height="14" rx="2" fill="rgba(89,89,89,0.10)" stroke="{SOFT}" stroke-width="1"/>'
        elif kind == "swatch-backend":
            s += f'<rect x="{x}" y="{y+36}" width="20" height="14" rx="2" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>'
        elif kind == "oval":
            s += f'<rect x="{x}" y="{y+36}" width="24" height="14" rx="7" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>'
        elif kind == "diamond":
            s += f'<polygon points="{x+12},{y+34} {x+24},{y+43} {x+12},{y+52} {x},{y+43}" fill="{ACC_TINT}" stroke="{ACC}" stroke-width="1"/>'
        elif kind == "arrow":
            s += f'<line x1="{x}" y1="{y+44}" x2="{x+28}" y2="{y+44}" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#{slug}-arrow)"/>'
        elif kind == "arrow-dashed":
            s += f'<line x1="{x}" y1="{y+44}" x2="{x+28}" y2="{y+44}" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="5,4" marker-end="url(#{slug}-arrow)"/>'
        elif kind == "arrow-accent":
            s += f'<line x1="{x}" y1="{y+44}" x2="{x+28}" y2="{y+44}" stroke="{ACC}" stroke-width="1.4" marker-end="url(#{slug}-arrow-accent)"/>'
        elif kind == "arrow-link":
            s += f'<line x1="{x}" y1="{y+44}" x2="{x+28}" y2="{y+44}" stroke="{LINK}" stroke-width="1.2" marker-end="url(#{slug}-arrow-link)"/>'
        elif kind == "activation":
            s += f'<rect x="{x+8}" y="{y+32}" width="8" height="22" fill="{ink(0.06)}" stroke="{MUTED}" stroke-width="0.8"/>'
        s += text(x + 40, y + 49, t, 14, 400, MUTED, "start")
        x += 40 + 14 * 0.55 * len(t) + 72
        x = int(x // 4 * 4)
    return s

def zone(x, y, w, h, lab):
    lw = int(round(12 * 0.62 * len(lab) / 4)) * 4 + 16
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{ink(0.02)}" stroke="{ink(0.10)}" stroke-width="0.8"/>'
            f'<rect x="{x+8}" y="{y+4}" width="{lw}" height="16" rx="2" fill="{PAPER}"/>'
            + text(x + 8 + lw // 2, y + 16, lab, 12, 400, ink(0.5), "middle", "0.14em"))

# =============================================================== A. layer stack — how it is built
def layers():
    slug = "nbg-layers"
    s = svg_open(slug, "How the nbg-design skill is built, in five layers",
                 "Layer stack showing the skill from its SKILL.md contract at the bottom, through the design system, the build pipeline and the in-deck editor, to the delivered HTML deck and PDF at the top.")
    X, WD, HT = 320, 1280, 80
    rows = [("L5", "Deliverables", "One self-contained HTML deck, its PDF, its rebuild script", "images embedded · one PDF page per slide · tools refreshable later", False),
            ("L4", "In-deck editor", "Right-click menu, toolbars, structure, assistant", "print-layout.js + deck-menu.js, inlined into the deck", True),
            ("L3", "Build pipeline", "Embed · add editor · verify · screenshot · export", "7 zero-dependency Node scripts + 5 shared libraries", False),
            ("L2", "Design system", "Palette, Aptos, 1920×1080 artboard, 9 templates", "3 logo lockups · 5 photos · ready-made data URIs", False),
            ("L1", "Contract", "SKILL.md: inputs, defaults, guardrails, quality gate", "one Markdown file is the whole behaviour", False)]
    # outer silhouette
    s += f'<rect x="{X}" y="40" width="{WD}" height="{HT*5}" rx="8" fill="{PAPER}" stroke="{ink(0.35)}" stroke-width="1"/>'
    for i, (tag, name, desc, note, focal) in enumerate(rows):
        y = 40 + i * HT
        if focal:
            s += f'<rect x="{X}" y="{y}" width="{WD}" height="{HT}" fill="{ACC_TINT}" stroke="{ACC}" stroke-width="1.2"/>'
        elif i % 2 == 1:
            s += f'<rect x="{X}" y="{y}" width="{WD}" height="{HT}" fill="{PAPER2}"/>'
        if i > 0 and not focal and not rows[i-1][4]:
            s += f'<line x1="{X}" y1="{y}" x2="{X+WD}" y2="{y}" stroke="{RULE}" stroke-width="1"/>'
        col = ACC if focal else MUTED
        s += eyebrow(X + 24, y + 48, tag, col)
        s += text(X + 96, y + 36, name, 20, 600, INK, "start")
        s += text(X + 96, y + 60, desc, 16, 400, MUTED, "start")
        s += text(X + WD - 24, y + 48, note, 16, 400, SOFT, "end")
    # direction indicator on the left margin
    s += f'<line x1="272" y1="440" x2="272" y2="56" stroke="{MUTED}" stroke-width="1.2" marker-end="url(#{slug}-arrow)"/>'
    s += eyebrow(272, 472, "BUILDS ON", MUTED, "middle")
    s += legend(slug, [("swatch-focal", "Focal layer — what makes a delivered deck editable by anyone"),
                       ("swatch-backend", "Layer — rests on the one below it")])
    return s + "</svg>"

# =============================================================== B. flowchart — the pipeline
def flow():
    slug = "nbg-flow"
    s = svg_open(slug, "How a deck is produced: five steps and one gate",
                 "Flowchart of the build pipeline: a request, the three inputs, authoring with tokens, embedding assets, adding the editor, the strict verification gate that loops back on failure, then screenshots, PDF export and delivery.")
    Y, HT = 160, 96
    A = f"url(#{slug}-arrow)"
    # ---- arrows first
    s += f'<line x1="216" y1="208" x2="256" y2="208" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'
    s += f'<line x1="464" y1="208" x2="504" y2="208" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'
    s += f'<line x1="712" y1="208" x2="752" y2="208" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'
    s += f'<line x1="960" y1="208" x2="1000" y2="208" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'
    s += f'<line x1="1208" y1="208" x2="1248" y2="208" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'
    # yes → right (accent, headline path)
    s += f'<line x1="1472" y1="208" x2="1512" y2="208" stroke="{ACC}" stroke-width="1.4" marker-end="url(#{slug}-arrow-accent)"/>'
    # screenshot+pdf → deliver (down)
    s += f'<line x1="1616" y1="256" x2="1616" y2="352" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'
    # no → down to fix
    s += f'<line x1="1360" y1="272" x2="1360" y2="352" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'
    # fix → back to author (left along y=392, up into author's bottom)
    s += f'<path d="M1248,392 H616 Q608,392 608,384 V256" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'
    # ---- labels
    s += label(1492, 190, "YES", ACC)
    s += label_left(1372, 320, "NO")
    s += label(928, 374, "FIX THE HTML, RUN AGAIN")
    # ---- nodes
    def oval(x, y, w, h, name, sub):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h//2}" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>'
                + text(x + w // 2, y + h // 2 + 2, name, 20, 600) + text(x + w // 2, y + h // 2 + 26, sub, 16, 400, MUTED))
    s += oval(40, Y, 176, HT, "Request", "topic in mind")
    s += node(256, Y, 208, HT, "Ask the inputs", "topic · audience · slides")
    s += node(504, Y, 208, HT, "Author the deck", "HTML with image tokens")
    s += node(752, Y, 208, HT, "Embed the assets", "embed-assets.mjs")
    s += node(1000, Y, 208, HT, "Add the editor", "add-deck-menu.mjs")
    # diamond (focal gate)
    s += f'<polygon points="1360,144 1472,208 1360,272 1248,208" fill="{PAPER}"/>'
    s += f'<polygon points="1360,144 1472,208 1360,272 1248,208" fill="{ACC_TINT}" stroke="{ACC}" stroke-width="1.2"/>'
    s += text(1360, 204, "Gate passes?", 20, 600) + text(1360, 228, "verify --strict", 16, 400, MUTED)
    s += node(1512, Y, 208, HT, "Script, look, print", "rebuild.mjs · shots · PDF")
    s += node(1248, 352, 224, 80, "Fix the deck", "layout, image, logo")
    s += oval(1512, 352, 208, 80, "Deliver", "HTML · PDF · rebuild.mjs")
    s += legend(slug, [("oval", "Start / end"), ("swatch-backend", "Step"), ("diamond", "The gate — the only decision"),
                       ("arrow-accent", "Happy path"), ("arrow", "Flow")])
    return s + "</svg>"

# =============================================================== C. sequence — a deck, end to end
def sequence():
    slug = "nbg-seq"
    s = svg_open(slug, "A deck, end to end",
                 "Sequence diagram of one deck: you brief Claude, Claude asks for topic, audience and slide count, authors the HTML, runs the scripts, the scripts drive a headless browser for screenshots and the PDF, Claude delivers HTML and PDF, and the recipient edits the deck in place and saves a copy.")
    X = [200, 560, 920, 1280, 1560]
    A, D = f"url(#{slug}-arrow)", f"url(#{slug}-arrow-accent)"
    TOP, BOT = 104, 548
    for x in X:
        s += f'<line x1="{x}" y1="{TOP}" x2="{x}" y2="{BOT}" stroke="{ink(0.22)}" stroke-width="1" stroke-dasharray="3,3"/>'
    # activations
    s += f'<rect x="556" y="140" width="8" height="304" fill="{ink(0.06)}" stroke="{MUTED}" stroke-width="0.8"/>'
    s += f'<rect x="916" y="300" width="8" height="112" fill="{ink(0.06)}" stroke="{MUTED}" stroke-width="0.8"/>'
    s += f'<rect x="1276" y="336" width="8" height="40" fill="{ink(0.06)}" stroke="{MUTED}" stroke-width="0.8"/>'
    def call(x1, x2, y, col=MUTED, m=None, dashed=False, w="1.2"):
        d = ' stroke-dasharray="5,4"' if dashed else ""
        return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="{w}"{d} marker-end="{m or A}"/>'
    s += call(200, 556, 140)                                  # m1 brief
    s += call(556, 200, 176, dashed=True)                      # m2 questions (return)
    s += call(200, 556, 212)                                  # m3 answers
    s += f'<path d="M564,244 H600 V268 H564" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'  # m4 self: author
    s += call(564, 916, 300)                                  # m5 run the scripts
    s += call(924, 1276, 336)                                 # m6 drive browser
    s += call(1276, 924, 372, dashed=True)                     # m7 PNG + PDF back
    s += call(916, 564, 408, dashed=True)                      # m8 PASS back
    s += call(556, 200, 444, ACC, D, w="1.4")                  # m9 headline: HTML + PDF
    s += call(200, 1560, 480)                                 # m10 hand over
    s += f'<path d="M1564,512 H1600 V536 H1564" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'  # m11 self: edit
    # labels (baseline = line - 14 → mask bottom at line - 10)
    s += label(380, 126, "A DECK ON TOPIC X")
    s += label(380, 162, "TOPIC · AUDIENCE · SLIDES?")
    s += label(380, 198, "ANSWERS")
    s += label_left(608, 260, "AUTHOR HTML WITH TOKENS")
    s += label(740, 286, "EMBED · EDITOR · VERIFY · SHOTS · PDF")
    s += label(1100, 322, "DEVTOOLS: CAPTURE + PRINT")
    s += label(1100, 358, "PNG PER SLIDE · PDF")
    s += label(740, 394, "PASS · PAGES = SLIDES")
    s += label(380, 430, "HTML · PDF · REBUILD.MJS", ACC)
    s += label(1100, 466, "DECK.HTML — ONE FILE, BY MAIL")
    s += label_left(1608, 528, "EDIT · SAVE COPY")
    # actors
    s += node(80, 32, 240, 72, "You", "the author", "input", "YOU")
    s += node(440, 32, 240, 72, "Claude + skill", "authors and runs", "focal", "AGENT")
    s += node(800, 32, 240, 72, "Scripts", "embed · menu · verify", "backend", "NODE")
    s += node(1160, 32, 240, 72, "Headless browser", "Chrome · Edge", "external", "EXT")
    s += node(1440, 32, 240, 72, "Recipient", "opens the file", "input", "USER")
    s += legend(slug, [("swatch-focal", "Focal actor"), ("activation", "Holds control"), ("arrow", "Call"),
                       ("arrow-dashed", "Return"), ("arrow-accent", "The deliverable")])
    return s + "</svg>"

# =============================================================== D. architecture — inside a delivered deck
def arch():
    slug = "nbg-arch"
    s = svg_open(slug, "Inside a delivered deck",
                 "Architecture of one delivered HTML file: the slides and the inlined editor block, the menu and toolbars the editor builds in the browser, the edit records kept in browser storage and re-applied on load, and the three ways out — a saved edited copy, a PDF through the print layout, and an optional call to the viewer's own LLM endpoint.")
    A, L = f"url(#{slug}-arrow)", f"url(#{slug}-arrow-link)"
    s += zone(200, 48, 360, 472, "DECK.HTML · ONE FILE")
    s += zone(720, 48, 360, 472, "IN THE VIEWER'S BROWSER")
    s += zone(1200, 48, 360, 472, "WAYS OUT")
    # ---- arrows
    s += f'<path d="M520,272 H632 Q640,272 640,264 V164 Q640,156 648,156 H760" fill="none" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'   # deck-menu → menu
    s += f'<line x1="900" y1="200" x2="900" y2="256" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'                                  # menu → records
    s += f'<line x1="760" y1="320" x2="520" y2="320" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="4,3" marker-end="{A}"/>'            # records → deck-menu (re-applied)
    s += f'<line x1="380" y1="256" x2="380" y2="200" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'                                  # deck-menu → slides
    s += f'<line x1="380" y1="344" x2="380" y2="400" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'                                  # deck-menu → print-layout
    s += f'<path d="M380,112 V96 Q380,88 388,88 H1592 Q1600,88 1600,96 V292 Q1600,300 1592,300 H1520" fill="none" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4,3" marker-end="{A}"/>'  # slides → saved copy (snapshot)
    s += f'<line x1="1040" y1="300" x2="1240" y2="300" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'                                # records → saved copy
    s += f'<line x1="520" y1="444" x2="1240" y2="444" stroke="{MUTED}" stroke-width="1.2" marker-end="{A}"/>'                                 # print-layout → pdf
    s += f'<line x1="1040" y1="156" x2="1240" y2="156" stroke="{LINK}" stroke-width="1.2" marker-end="{L}"/>'                                 # menu → llm
    # ---- labels
    s += label(704, 142, "BUILDS THE UI")
    s += label_left(908, 236, "RECORDS EDITS")
    s += label(640, 306, "RE-APPLIED ON LOAD")
    s += label_left(388, 236, "EDITS IN PLACE")
    s += label_left(388, 380, "EXPORT TO PDF")
    s += label(640, 74, "SNAPSHOT AT LOAD")
    s += label(1140, 286, "APPLY RECORDS")
    s += label(880, 430, "PRINT LAYOUT · SAVE AS PDF")
    s += label(1140, 142, "HTTPS · VIEWER'S KEY", LINK)
    # ---- nodes
    s += node(240, 112, 280, 88, "Slides", "N × .slide, images embedded", "backend", "HTML")
    s += node(240, 256, 280, 88, "deck-menu.js", "the editor, ~4,000 lines", "focal", "JS")
    s += node(240, 400, 280, 88, "print-layout.js", "same shim as the CLI exporter", "backend", "JS")
    s += node(760, 112, 280, 88, "Menu & toolbars", "tabs · text and shape rows", "backend", "UI")
    s += node(760, 256, 280, 88, "Edit records", "localStorage · path, original, html", "store", "STORE")
    s += node(1240, 112, 280, 88, "LLM endpoint", "your provider, your key", "external", "EXT")
    s += node(1240, 256, 280, 88, "Saved edited copy", "deck-edited.html, still one file", "backend", "OUT")
    s += node(1240, 400, 280, 88, "PDF", "print dialog → Save as PDF", "backend", "OUT")
    s += legend(slug, [("swatch-focal", "Focal component"), ("swatch-store", "Browser storage"), ("swatch-external", "Outside the deck"),
                       ("arrow", "Calls / writes"), ("arrow-dashed", "Passive: taken or re-applied on load"), ("arrow-link", "HTTPS")])
    return s + "</svg>"

# =============================================================== E. tree — what a viewer can do
def tree():
    slug = "nbg-tree"
    s = svg_open(slug, "What a viewer can do with a delivered deck",
                 "Tree of the in-deck editor's capabilities: text editing and formatting, shapes and arrangement, structure and toolbars, the AI assistant, and the outputs — saved copy, PDF and discard.")
    A = f"url(#{slug}-arrow)"
    xs = [56, 392, 728, 1064, 1400]; cw, ch, cy = 304, 188, 224
    cxs = [x + cw // 2 for x in xs]
    # connectors: root drop, bus, child drops
    s += f'<line x1="880" y1="128" x2="880" y2="176" stroke="{MUTED}" stroke-width="1.2"/>'
    s += f'<path d="M{cxs[0]},{cy} V184 Q{cxs[0]},176 {cxs[0]+8},176 H{cxs[-1]-8} Q{cxs[-1]},176 {cxs[-1]},184 V{cy}" fill="none" stroke="{MUTED}" stroke-width="1.2"/>'
    for cx in cxs[1:-1]:
        s += f'<line x1="{cx}" y1="176" x2="{cx}" y2="{cy}" stroke="{MUTED}" stroke-width="1.2"/>'
    # root
    s += node(720, 48, 320, 80, "Right-click editor", "in every delivered deck", "focal")
    kids = [("Text", ["Double-click, type, Enter applies", "B I U S · size · font · alignment", "colour from the NBG palette only"]),
            ("Shapes & arrange", ["Resize, move, fill, border, radius", "several at once: Shift+click / drag", "order · align · distribute · group", "Edit SVG: the parts of a drawing"]),
            ("Structure & toolbars", ["Outline and Tree tabs, checkboxes", "element source under a splitter", "toolbars pin, anchor, detach"]),
            ("Assistant", ["prompt · screenshot · source · clip", "answer, or replace the element", "your own endpoint and key"]),
            ("Output", ["Save edited copy: still one file", "Export to PDF, one page per slide", "discard this slide, or every edit", "rebuild.mjs: newer tools, later"])]
    for x, (name, lines) in zip(xs, kids):
        s += f'<rect x="{x}" y="{cy}" width="{cw}" height="{ch}" rx="6" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>'
        s += text(x + cw // 2, cy + 40, name, 20, 600)
        s += f'<line x1="{x+24}" y1="{cy+56}" x2="{x+cw-24}" y2="{cy+56}" stroke="{RULE}" stroke-width="1"/>'
        for i, l in enumerate(lines):
            s += text(x + cw // 2, cy + 84 + 26 * i, l, 16, 400, MUTED)
    # one editorial aside
    s += text(880, 460, "Fonts and colours stay inside the NBG-inspired look: a viewer can fix a slide, not leave the system.", 20, 400, MUTED, "middle", None, True)
    s += text(880, 492, "Images, new elements and new layouts remain the skill's job — regenerate.", 20, 400, SOFT, "middle", None, True)
    s += legend(slug, [("swatch-focal", "The editor itself"), ("swatch-backend", "A family of actions, all recorded and reversible")])
    return s + "</svg>"

SVG = {"layers": layers(), "flow": flow(), "sequence": sequence(), "arch": arch(), "tree": tree()}
META = {"layers": ("Layer stack", "How the nbg-design skill is built, in five layers"),
        "flow": ("Flowchart", "How a deck is produced: five steps and one gate"),
        "sequence": ("Sequence", "A deck, end to end"),
        "arch": ("Architecture", "Inside a delivered deck"),
        "tree": ("Tree", "What a viewer can do with a delivered deck")}

def write_standalone(outdir):
    os.makedirs(outdir, exist_ok=True)
    for k, svg in SVG.items():
        kind, title = META[k]
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{ --color-paper: {PAPER}; --color-ink: {INK}; --color-muted: {MUTED}; --color-accent: {ACC}; --font-sans: {FONT}; }}
body {{ font-family: var(--font-sans); background: var(--color-paper); color: var(--color-ink); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 3rem 2rem; }}
.frame {{ max-width: 1760px; width: 100%; }}
.eyebrow {{ font-size: 0.7rem; letter-spacing: 0.14em; text-transform: uppercase; color: #007B85; margin-bottom: 0.5rem; }}
h1 {{ font-size: 1.75rem; font-weight: 400; letter-spacing: -0.01em; line-height: 1.15; color: var(--color-ink); margin-bottom: 1.5rem; }}
svg {{ width: 100%; height: auto; display: block; }}
</style>
</head>
<body>
<div class="frame">
<p class="eyebrow">{kind} · nbg-design · Diagram Design</p>
<h1>{title}</h1>
{svg}
</div>
</body>
</html>
'''
        open(os.path.join(outdir, f"nbg-design-{k}.html"), "w").write(html)

if __name__ == "__main__":
    import sys
    write_standalone(sys.argv[1] if len(sys.argv) > 1 else "diagrams")
    for k, v in SVG.items(): print(k, len(v), "bytes")
