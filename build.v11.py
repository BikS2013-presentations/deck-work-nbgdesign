# Generator for "The nbg-design skill — how it is built, how it works, how its decks are edited".
# Reuses the helpers, CSS and JS of the AI Committee generator in ../deck-work (briefing look).
import re, sys
sys.path.insert(0, "/Users/giorgosmarinos/officework/deck-work-nbgdesign")
from diagrams import SVG
BASE = "/Users/giorgosmarinos/officework/deck-work"
HERE = "/Users/giorgosmarinos/officework/deck-work-nbgdesign"
OUT = f"{HERE}/deck.html"
src = open(f"{BASE}/build.py").read()
helpers = src.split("# =============================================================== SLIDES")[0]
ns = {}
exec(compile(helpers, "helpers", "exec"), ns)
ico, header, pill, numc, add, motif = ns["ico"], ns["header"], ns["pill"], ns["numc"], ns["add"], ns["motif"]
SLIDES = ns["SLIDES"]; ACC = ns["ACC"]

def dg(svg): return f'<div class="body dgb"><div class="dg">{svg}</div></div>'
EX, TM, DV = "01 · What it can do", "02 · How to use it", "03 · How to extend it"

def kbd(*keys): return " ".join(f'<span class="kbd">{k}</span>' for k in keys)
def code(s): return f'<span class="code">{s}</span>'
def mini(icon, title, body, tall=False):
    return f'<div class="mini{" tall" if tall else ""}"><div class="mini-h">{ico(icon,26)}<h4>{title}</h4></div>{body}</div>'
def lst(items, tight=False):
    li = "".join(f'<li>{ico(i,22)}<div>{t}</div></li>' for i,t in items)
    return f'<ul class="lst{" tight" if tight else ""}">{li}</ul>'
def divider(num, eyebrow, title, sub):
    add(0, f'''
  <div class="dv-bg"></div>
  <div class="dv-num">{num}</div>
  <div class="dv-motif">{"<i></i>"*9}</div>
  <div class="dv-l"><div class="dv-eyebrow">{eyebrow}</div><h1 class="dv-title">{title}</h1><div class="dv-rule"></div><p class="dv-sub">{sub}</p></div>
  <div class="logo-knockout dv-logo"></div>
  <div class="dv-pg">{len(SLIDES)+1}</div>''', cls="cover")

# ================================================================= 1 cover
add(0, f'''
  <div class="cover-l">
    <div class="eyebrow">A Presentations Skill inspired by the NBG Brand</div>
    <h1 class="cover-title sm">The<br>nbg-design<br>skill</h1>
    <div class="cover-rule"></div>
    <p class="cover-sub">How it is built, how it works, and how anyone who receives a deck can edit it.</p>
    <div class="cover-meta"><span>Skill v1.18.0</span><span class="dot"></span><span class="acc">Sep 2026</span></div>
    <div class="logo-primary cover-logo"></div>
  </div>
  <div class="cover-photo photo-athens"></div>
  {motif(1040, 160, 100)}
''', cls="cover")

# ================================================================= 2 agenda
add(0, f'''
    <div class="ag-left">
      <div class="eyebrow">nbg-design · Sep 2026</div>
      <div class="ag-title">Agenda</div>
      <div class="ag-rule"></div>
      <p class="ag-cap">Three sections. Each stands on its own.</p>
    </div>
    <div class="ag-vline"></div>
    <ul class="ag-list" style="top:200px">
      <li class="ag-item on"><span class="ag-num">01</span><span class="ag-lbl">WHAT IT CAN DO</span></li>
      <li class="ag-item on"><span class="ag-num">02</span><span class="ag-lbl">HOW TO USE IT</span></li>
      <li class="ag-item on"><span class="ag-num">03</span><span class="ag-lbl">HOW TO EXTEND IT</span></li>
    </ul>''')

# ================================================================= SECTION 01 — executives
divider("01", "Section 01", "What it<br>can do", "A design system inspired by the NBG brand, a build pipeline and an in-deck editor, packaged as one Claude skill.")

add(0, header(EX, "WHAT THE SKILL IS", "One Claude Code skill that turns a request into a finished presentation in a look inspired by the NBG brand.") + f'''
<div class="body fill">
  <div class="grid3" style="gap:28px">
    {mini("layers","A design system in a box",'<ul><li>A design system <b>inspired by the NBG brand</b>: 16:9 artboard, Aptos, a nine-colour teal-led palette.</li><li>Nine slide templates (covers, dividers, content), logos and photography bundled with the skill.</li><li>Guardrails written down once, applied to every deck.</li></ul>', True)}
    {mini("gear","A deterministic build pipeline",'<ul><li>Claude authors the HTML; six zero-dependency scripts embed the images, add the editor, verify, write the rebuild script, screenshot and export.</li><li>A strict, browser-free gate that a deck must pass before it is delivered.</li><li>The PDF is printed from the deck itself, so it looks exactly like the HTML.</li></ul>', True)}
    {mini("hand","Decks the recipients can edit",'<ul><li>Every delivered deck carries a right-click editor: fix a word, resize a card, align a row, ask an AI assistant.</li><li>Nothing to install: it works from a file on the desktop, in any modern browser.</li><li>Edits stay inside the look: the skill\'s fonts and palette only.</li></ul>', True)}
  </div>
  <div class="band big" style="margin-top:44px">
    <div class="band-stat"><div class="stat-n">1 file</div><div class="stat-l">the whole deck: HTML with every image embedded</div></div>
    <div class="band-stat"><div class="stat-n">0</div><div class="stat-l">installs for the viewer, npm packages for the builder</div></div>
    <div class="band-stat"><div class="stat-n">HTML + PDF</div><div class="stat-l">plus a rebuild script that refreshes the editor later; PowerPoint is out of scope</div></div>
    <div class="band-stat"><div class="stat-n">en · gr · bi</div><div class="stat-l">languages supported by the design system</div></div>
  </div>
</div>''')

add(0, header(EX, "WHY IT MATTERS", "Four problems every presentation team knows, and how the skill answers each.") + f'''
<div class="body fill">
  <div class="grid4" style="gap:26px">
    {mini("shield","Consistency",'<p><b>Every deck shares one look.</b> One palette, one type stack, one artboard, one logo lockup — enforced by the skill, not by the author\'s memory.</p><p>The verifier rejects a deck with a fake logo, a missing photo or an external image path.</p>', True)}
    {mini("rocket","Speed",'<p><b>From a Google Slides draft to a finished deck in minutes.</b> The Townhall deck was rebuilt 1:1 from its Google Slides source; every re-run since is one command.</p>', True)}
    {mini("globe","Portability",'<p><b>One self-contained file.</b> It can be emailed, put on a share or opened from a USB stick; it renders identically everywhere because nothing points back to the machine that built it.</p>', True)}
    {mini("users","Ownership",'<p><b>Recipients fix their own slides.</b> A typo, a longer title, a card that should be teal, a row that needs aligning — done in place, saved as a copy, exported to PDF — without a regeneration.</p>', True)}
  </div>
  <div class="insight"><span class="tag">Key point</span><p>The skill moves the effort from <b>making slides look right</b> to <b>deciding what they should say</b>.</p></div>
</div>''')

add(0, header(EX, "WHAT YOU RECEIVE", "Three files per deck, produced and verified the same way every time.") + f'''
<div class="body fill"><div class="two">
  <div>
    <div class="seclbl">The deliverables</div>
    {lst([("doc","<b>The HTML deck</b> — 1920×1080 slides that scale to any screen, keyboard and button navigation, every logo and photo embedded, the right-click editor inlined."),
          ("download","<b>The PDF</b> — printed from that HTML by the browser engine: one page per slide, vector text, same colours and photography, verified page count."),
          ("monitor","<b>Screenshots</b> (on request) — one PNG per slide at 1366×768 and 1440×900, the two viewports the skill requires to check."),
          ("refresh","<b>The rebuild script</b> — <code class='code'>deck.rebuild.mjs</code>: run it after the skill is updated and the deck receives the newer editing tools, verified, with its PDF re-exported — no regeneration."),
          ("wrench","<b>A generator</b> for data-driven decks — a small Python script that rebuilds the deck from its content, so updates are a diff, not a redo.")])}
  </div>
  <div>
    <div class="seclbl">What the skill asks before it starts</div>
    {lst([("chat","<b>Topic, audience, slide count.</b> The three inputs it never guesses; it asks instead."),
          ("globe","<b>Language</b> — English by default; Greek or bilingual on request."),
          ("doc","<b>Output</b> — HTML by default; \"send as PDF\" adds the export."),
          ("alert","<b>Not PowerPoint.</b> If asked, it says so and delivers HTML and PDF — no improvised conversion.")])}
    <div class="band" style="margin-top:28px"><p class="band-t">No fallbacks: a missing input is a question to you, never a silent default.</p></div>
  </div>
</div></div>''')

# ================================================================= SECTION 02 — team
divider("02", "Section 02", "How to<br>use it", "Asking for a deck, what happens in between, the quality gates, and everything the right-click editor can do.")

add(0, header(TM, "ASKING FOR A DECK", "What the skill needs from you, what it decides by itself, and what it refuses to do.") + f'''
<div class="body fill"><div class="grid3" style="gap:28px">
  {mini("chat","It always asks for",'<ul><li><b>Topic</b> — what the deck is about.</li><li><b>Audience</b> — who reads it; this sets depth and tone.</li><li><b>Slide count or depth</b> — 8, 16, 20+.</li><li>Whether the bundled design-system files may be changed (they normally are not).</li></ul>', True)}
  {mini("check","Approved defaults",'<ul><li><b>Language</b>: English. <code class="code">gr</code> and <code class="code">bi</code> exist; anything else must come from you.</li><li><b>Output</b>: HTML. A PDF is always exported from the finished HTML, never authored separately.</li><li><b>Logo</b>: shown, unless you ask to hide it.</li><li>Cover first, dividers between sections, content slides in between.</li></ul>', True)}
  {mini("alert","It will not",'<ul><li>Produce or convert to <b>PowerPoint</b>.</li><li>Guess a missing input or substitute a fallback value.</li><li>Put an API key, token or endpoint into a deck or into the skill.</li><li>Reference an image by a path: every image is embedded, or the deck fails the gate.</li></ul>', True)}
</div>
<div class="insight"><span class="tag">Tip</span><p>A Google Slides draft is a fine source: the skill reads it through the Slides API, rebuilds it 1:1 in the skill's look, and keeps the page count.</p></div>
</div>''')

add(0, header(TM, "A DECK, END TO END", "One request, three answers, one command chain, two files — and a recipient who can edit the result.") + dg(SVG["sequence"]))

add(0, header(TM, "THE PIPELINE: FIVE STEPS AND ONE GATE", "Claude authors; the scripts embed, add the editor and verify; a failing gate sends the deck back to the author, never forward.") + dg(SVG["flow"]))

add(0, header(TM, "THE PIPELINE, STEP BY STEP", "What each step does and the command behind it. Steps 2 to 4 and the rebuild script are mandatory for every deck.") + f'''
<div class="body fill">
  <div class="flow">
    <div class="step"><div class="step-h"><span class="stepn">1</span>{ico("doc",28)}</div><h4>Author with tokens</h4><p>Claude writes the deck on the 1920×1080 artboard, the design-system CSS and <b>placeholders</b> where images go: <code class="code">&#123;&#123;LOGO_PRIMARY&#125;&#125;</code>, <code class="code">&#123;&#123;PHOTO_STREET&#125;&#125;</code>.</p></div>
    <div class="step"><div class="step-h"><span class="stepn">2</span>{ico("download",28)}</div><h4>Embed the assets</h4><p>Every token becomes the verbatim base64 image. The script finds the assets next to itself, so it works from any folder and any machine.</p><span class="cmd">embed-assets.mjs deck.html</span></div>
    <div class="step"><div class="step-h"><span class="stepn">3</span>{ico("wrench",28)}</div><h4>Add the editor</h4><p>One script block is inlined before <code class="code">&lt;/body&gt;</code>: the right-click menu, editing, toolbars, assistant, print. Re-running upgrades an older block.</p><span class="cmd">add-deck-menu.mjs deck.html</span></div>
    <div class="step"><div class="step-h"><span class="stepn">4</span>{ico("shield",28)}</div><h4>Verify (strict)</h4><p>Browser-free gate: no unresolved tokens, no external image paths, real logo, enough images, current menu. A failing deck is never delivered.</p><span class="cmd">verify-deck.mjs deck.html --strict</span></div>
    <div class="step"><div class="step-h"><span class="stepn">5</span>{ico("monitor",28)}</div><h4>Script, look, print</h4><p>The deck's rebuild script is written next to it; screenshots per slide are read for overlaps and clipping; then the PDF is printed, one page per slide.</p><span class="cmd">write-rebuild-script.mjs · screenshot-deck.mjs · export-pdf.mjs</span></div>
  </div>
  <div class="insight"><span class="tag">Why tokens</span><p>Hand-pasting a 600 KB base64 photo is the step that silently fails on a headless run. Tokens make embedding a script's job, and the gate catches any slip.</p></div>
</div>''')

PAL = [("#003841","Deep teal","primary accent, dark panels, covers"),("#007B85","Teal","secondary accent, rules, icons"),("#00ADBF","Bright cyan","highlight accent"),
       ("#00CFE7","Electric cyan","highlight, sparingly"),("#0A1416","Black","body text on light"),("#BEC1BE","Grey 1","rules, muted surfaces"),
       ("#939793","Grey 2","secondary text"),("#F5F8F6","Cream","light page background"),("#FFFFFF","White","text on dark, cards on cream")]
sw = "".join(f'<div class="sw2"><i style="background:{h};{"border-bottom:1px solid #D9E4E5" if h in ("#FFFFFF","#F5F8F6") else ""}"></i><div><b>{n}</b><span>{h}</span><small>{r}</small></div></div>' for h,n,r in PAL)
add(0, header(TM, "THE DESIGN SYSTEM THE SKILL CARRIES", "Inspired by the NBG brand and distilled into one HTML reference: nine colours, one typeface and nine templates.") + f'''
<div class="body fill">
  <div class="pal">{sw}</div>
  <div class="grid3" style="margin-top:34px;gap:28px">
    {mini("layers","Format & type",'<p><b>16:9, 1920×1080 artboard</b>, scaled to fit any viewport. <b>Aptos</b> for everything, with a system fallback where it is absent — the stack is never swapped.</p>')}
    {mini("doc","Nine templates",'<p><b>Covers</b> (hero photo, image card, alternate), <b>dividers</b> (photo, deep teal, bright), <b>content</b> (image right, two columns, stat-led). Content pages stay calm and mostly monochrome; accent blocks belong to covers and openers.</p>')}
    {mini("star","Eight assets",'<p>Three logo lockups — <b>primary</b> for light backgrounds, <b>knockout</b> for dark, <b>small</b> for footers — and five photographs, each shipped with a ready-made data URI. The logo is always the image, never text or a box.</p>')}
  </div>
</div>''')

add(0, header(TM, "QUALITY GATES", "What must be true before a deck leaves. The first gate runs anywhere; the others need a browser.") + f'''
<div class="body fill"><div class="two">
  <div>
    <div class="seclbl">verify-deck --strict (browser-free, mandatory)</div>
    {lst([("check","<b>No unresolved tokens</b> and no image referenced by <code class='code'>file://</code>, absolute, relative or <code class='code'>http</code> path — every image is a <code class='code'>data:</code> URI."),
          ("check","<b>Enough embedded images</b> (default 2) and a minimum size (200 KB): a photo-less deck is the classic tell of a skipped step."),
          ("check","<b>A real logo</b>: bare <code class='code'>“NBG”</code> text nodes that could stand in for the lockup fail the gate."),
          ("check","<b>The current editor block</b>: missing, PDF-only or older than the skill's — fail or warn; incomplete — always fail.")], True)}
  </div>
  <div>
    <div class="seclbl">Visual and print checks</div>
    {lst([("monitor","<b>Fit</b>: the full slide visible at 1366×768 and 1440×900 with no scrolling caused by the artboard."),
          ("layers","<b>No collisions</b>: title, body, card rows, callouts, footer and page number keep separate zones — at least 32 px between groups and 72 px above the footer. Crowded content is cut or split, never squeezed or hidden."),
          ("doc","<b>PDF = deck</b>: page count equals slide count and every slide box equals the page box, or the exporter exits with an error."),
          ("search","<b>Read the pictures</b>: screenshots and rasterised PDF pages are inspected, not just produced.")], True)}
  </div>
</div></div>''')

# ---- editing slides
MENU = f'''<div class="mock">
  <div class="mock-h"><span class="tab on">Menu</span><span class="tab">Assistant</span><span class="tab">Outline</span><span class="tab">Tree</span><span class="sp"></span><span class="ic">📌</span><span class="ic">⧉</span><span class="ic">✕</span></div>
  <div class="mock-sec">At this point</div>
  <div class="mock-i"><b>Edit text</b><span>double-click does the same</span></div>
  <div class="mock-i"><b>Resize / move shape</b><span>card · 420 × 300</span></div>
  <div class="mock-sec">Select at this point</div>
  <div class="mock-i dim"><b>Text block</b><span>front-most</span></div>
  <div class="mock-i dim"><b>Card</b><span>encloses the one above</span></div>
  <div class="mock-i dim"><b>Photo panel</b><span>behind</span></div>
  <div class="mock-sec">Slide</div>
  <div class="mock-i"><b>Select all shapes on this slide</b><span>Ctrl/Cmd+A</span></div>
  <div class="mock-i"><b>Ask the assistant</b><span>Ctrl/Cmd+Shift+L</span></div>
  <div class="mock-sec">Deck</div>
  <div class="mock-i"><b>Export to PDF</b><span>one page per slide</span></div>
  <div class="mock-i"><b>Save edited copy</b><span>deck-edited.html</span></div>
  <div class="mock-i"><b>Discard changes on this slide</b><span>3 changes</span></div>
  <div class="mock-i"><b>Discard edits</b><span>every slide</span></div>
</div>'''
add(0, header(TM, "WHAT A VIEWER CAN DO", "Five families of actions, all in the file itself, all recorded and reversible. The next seven slides walk through them.") + dg(SVG["tree"]))

add(0, header(TM, "EDITING 1 · THE RIGHT-CLICK MENU", "Every delivered deck carries its own editor. Right-click anywhere on a slide; Escape or a click outside closes it.") + f'''
<div class="body fill"><div class="cols" style="grid-template-columns:640px 1fr;gap:70px;align-items:start">
  {MENU}
  <div>
    {lst([("hand","<b>It shows what applies to the spot you clicked.</b> Text under the pointer offers <i>Edit text</i>; a card, image or panel offers <i>Resize / move shape</i>; a stack of nested shapes lists every level so you can pick the one you mean."),
          ("layers","<b>Four tabs.</b> <i>Menu</i> holds the actions. <i>Assistant</i> is the AI panel. <i>Outline</i> lists the slide's shapes with checkboxes. <i>Tree</i> shows the slide's HTML, with the selected element's source underneath."),
          ("pin","<b>📌 pins it</b> — it stays open after a choice, keeps its place and can be dragged by its header. <b>⧉ detaches it</b> into a window of its own (always-on-top in Chrome and Edge)."),
          ("gear","<b>Toolbars section.</b> Ticks show which toolbar tabs are shown and which is in front; tick one to pin it and bring it forward, untick to hide, <i>Automatic toolbars</i> restores the default where they appear with the selection."),
          ("shield","<b>Lives outside the slides.</b> The menu, frames and toolbars never appear in screenshots, in the PDF or in the print layout.")])}
  </div>
</div></div>''')

TB = '''<div class="tbar"><span class="grip">⋮⋮</span><span class="bt on">B</span><span class="bt"><i>I</i></span><span class="bt"><u>U</u></span><span class="bt"><s>S</s></span><span class="sep"></span><span class="bt">A−</span><span class="sel">24 px</span><span class="bt">A+</span><span class="sep"></span><span class="sel">Aptos ▾</span><span class="sep"></span><span class="lab">Colour</span><span class="dot" style="background:#003841"></span><span class="dot" style="background:#007B85"></span><span class="dot" style="background:#00ADBF"></span><span class="dot" style="background:#00CFE7"></span><span class="dot" style="background:#0A1416"></span><span class="dot" style="background:#5B6B6D"></span><span class="dot" style="background:#F5F8F6"></span><span class="dot" style="background:#fff"></span><span class="sep"></span><span class="bt">≡</span><span class="bt">☰</span><span class="bt">≡</span><span class="sep"></span><span class="bt">Clear</span><span class="bt on">Done</span></div>'''
add(0, header(TM, "EDITING 2 · TEXT", "Double-click any text. The whole block becomes editable in place, with a teal outline; the slide's CSS is never touched.") + f'''
<div class="body fill">
  {TB}
  <div class="two" style="margin-top:40px">
    <div>
      <div class="seclbl">Editing</div>
      {lst([("hand",f"<b>Double-click</b> a text (or right-click → <i>Edit text</i>). Type, {kbd('Backspace')}, {kbd('Shift+Enter')} for a line break, {kbd('Ctrl/Cmd+Z')} to undo."),
            ("check",f"{kbd('Enter')} or a click outside <b>applies</b>; {kbd('Esc')} <b>cancels</b>. Deck shortcuts (arrows, space) are paused while you edit."),
            ("doc","<b>Paste and drop insert plain text.</b> Anything a browser wraps around typed text is unwrapped when the edit is applied, so no stray formatting leaks in."),
            ("star","Accent spans inside a title (the teal word in a heading) stay intact.")], True)}
    </div>
    <div>
      <div class="seclbl">The formatting row</div>
      {lst([("wrench","<b>Selection first.</b> Every control applies to the selected run when there is one, and to the whole block when there is none."),
            ("doc",f"<b>B / I / U / S</b> ({kbd('Ctrl/Cmd+B')} {kbd('I')} {kbd('U')}), <b>A− / A+</b> or an exact px size ({kbd('Ctrl/Cmd+Shift+>')} / {kbd('<')}), <b>font</b> from the design-system stacks, <b>colour</b> from the skill's palette only, <b>alignment</b> for the block."),
            ("refresh","<b>Clear</b> removes the selection's formatting, or returns the block to its authored style. <b>Done</b> applies."),
            ("shield","Fonts and colours are limited on purpose: a viewer can fix a slide but cannot leave the look.")], True)}
    </div>
  </div>
</div>''')

STB = '''<div class="tbar"><span class="grip">⋮⋮</span><span class="lab">X</span><span class="sel">120</span><span class="lab">Y</span><span class="sel">300</span><span class="lab">W</span><span class="sel">420</span><span class="lab">H</span><span class="sel">300</span><span class="sep"></span><span class="lab">Fill</span><span class="dot" style="background:#007B85"></span><span class="dot" style="background:#F5F8F6"></span><span class="dot" style="background:#fff"></span><span class="sel">Transparent ▾</span><span class="sep"></span><span class="lab">Border</span><span class="sel">1 px ▾</span><span class="dot" style="background:#003841"></span><span class="sep"></span><span class="lab">Radius</span><span class="sel">8</span><span class="lab">Opacity</span><span class="sel">100</span><span class="lab">Shadow</span><span class="sel">Soft ▾</span><span class="sep"></span><span class="sel">Stack ▾</span><span class="bt">Reset</span><span class="bt on">Done</span></div>
<div class="tbar" style="margin-top:12px"><span class="grip">⋮⋮</span><span class="lab">Order</span><span class="bt">Front</span><span class="bt">Forward</span><span class="bt">Backward</span><span class="bt">Back</span><span class="sep"></span><span class="lab">Align</span><span class="bt">⇤</span><span class="bt">⇹</span><span class="bt">⇥</span><span class="bt">⤒</span><span class="bt">⇳</span><span class="bt">⤓</span><span class="sep"></span><span class="lab">Distribute</span><span class="bt">↔</span><span class="bt">↕</span><span class="sel">to selection ▾</span><span class="sep"></span><span class="bt">Group</span><span class="bt">Ungroup</span><span class="sep"></span><span class="bt">&lt;/&gt;</span></div>'''
add(0, header(TM, "EDITING 3 · SHAPES", "Right-click a card, photo panel, image or text block → Resize / move shape. A teal frame with eight handles appears.") + f'''
<div class="body fill">
  {STB}
  <div class="two" style="margin-top:36px">
    <div>
      <div class="seclbl">Moving and resizing</div>
      {lst([("hand",f"<b>Drag a handle</b> to resize ({kbd('Shift')} keeps the proportions), <b>drag inside</b> to move. Arrow keys nudge by 1 px, {kbd('Shift')} by 10; {kbd('Alt')}+arrows resize."),
            ("layers",f"{kbd('Tab')} selects the enclosing shape, {kbd('Shift+Tab')} steps back in; {kbd('Esc')}, {kbd('Enter')} or a click outside finishes."),
            ("gear","<b>Only inline geometry changes</b> — left, top, width, height — and pointer movement is divided by the slide's current scale, so coordinates stay exact artboard pixels at any window size."),
            ("refresh","Elements in normal flow get only the right and bottom handles: they grow right and down. <b>Reset</b> restores size, position and style.")], True)}
    </div>
    <div>
      <div class="seclbl">The shape row</div>
      {lst([("wrench","<b>X / Y / W / H</b> typed exactly; <b>fill</b> (the palette, transparent or default); <b>border</b> none to 6 px in a palette colour; <b>corner radius</b>, <b>opacity</b>, <b>shadow</b> none / soft / strong."),
            ("doc","Everything is inline style on the element, recorded as one reversible edit per element."),
            ("alert","<b>Neighbours do not re-flow.</b> Widen one card in a row, then use <i>Distribute</i> or move the next card to restore the spacing. The overlap rules still apply to the result."),
            ("search","<b>Stack</b> lists the enclosing shapes, the selected one and its children, for the level a click cannot reach."),
            ("layers","<b>Edit SVG</b>: right-click a drawn icon, diagram or chart and its parts — paths, shapes, text, groups — get handles of their own: move, resize, recolour, reorder, reword. The five diagrams in this deck are editable this way.")], True)}
    </div>
  </div>
</div>''')

add(0, header(TM, "EDITING 4 · SEVERAL SHAPES AT ONCE", "Text blocks, cards, panels and images alike. The frame spans the selection and each member gets a dashed mark.") + f'''
<div class="body fill"><div class="grid3" style="gap:28px">
  {mini("users","Selecting",f'<ul><li>{kbd("Shift")}+click adds the smallest shape under the pointer, or removes it when it is already selected.</li><li>{kbd("Shift")}+drag on the slide draws a box: every top-level shape fully inside is added.</li><li>{kbd("Ctrl/Cmd+A")} selects every top-level shape of the slide; {kbd("Ctrl/Cmd")}+click selects everything inside the shape under the pointer; a shape with nothing inside is picked alone, even a group member, and on the same spot again cycles outward.</li><li>The menu offers <i>Add to</i> / <i>Remove from selection</i> / <i>Select all shapes</i>; the <b>Outline</b> tab does it with checkboxes.</li></ul>', True)}
  {mini("layers","Arranging",f'<ul><li><b>Order</b>: bring to front / forward, send backward / to back ({kbd("Ctrl/Cmd+]")} and {kbd("[")}, {kbd("Shift")} for front / back).</li><li><b>Align</b> left, centre, right, top, middle, bottom — relative to the selection\'s own box or to the slide.</li><li><b>Distribute</b> horizontally or vertically with equal gaps; the first and last stay put.</li><li>Dragging moves all, handles scale all proportionally, every style control applies to all.</li></ul>', True)}
  {mini("link","Grouping",f'<ul><li><b>Group</b> ({kbd("Ctrl/Cmd+G")}) / <b>Ungroup</b> ({kbd("Ctrl/Cmd+Shift+G")}).</li><li>A group is logical: members carry a <code class="code">data-nbg-group</code> mark and always select, move, resize, align and order together.</li><li>Groups persist in the browser, land in the saved copy and are removed by <i>Discard edits</i>.</li><li>The page structure is never rebuilt: ordering is an inline z-index, grouping an attribute, so every earlier edit stays valid.</li></ul>', True)}
</div>
<div class="insight"><span class="tag">Nested shapes</span><p>A click lands on one level only. Use <b>Select at this point</b> in the menu (front-most first, containers, shapes behind), the toolbar's <b>Stack</b> list, or {kbd('Tab')} / {kbd('Shift+Tab')} to reach the others.</p></div>
</div>''')

add(0, header(TM, "EDITING 5 · STRUCTURE, TOOLBARS AND WINDOWS", "The Outline and Tree tabs, the toolbar modes, and panels that leave the browser window.") + f'''
<div class="body fill"><div class="grid3" style="gap:28px">
  {mini("search","Outline & Tree",'<ul><li><b>Outline</b>: the slide\'s shapes nested by containment — cards, text blocks, images — with kind icons, sizes, group badges, a text filter, checkboxes, All / None. Click a name to select it, Shift+click adds.</li><li><b>Tree</b>: the slide\'s HTML elements, synced both ways with the selection; double-click edits a text; hovering outlines the element on the slide.</li><li>Under the tree, the selected element\'s <b>editable source</b> behind a draggable splitter. <i>Apply</i> records it like any other edit; scripts are stripped. For people who know what they are doing.</li></ul>', True)}
  {mini("gear","Toolbars",f'<ul><li>One floating panel with three tabs — <b>Text</b>, <b>Shape</b>, <b>SVG</b> — one row at a time: the tab of the editor in use comes to the front by itself; a tab you click stays in front; each can be hidden on its own.</li><li>Three modes per toolbar: <b>auto</b> (with the selection), <b>on</b> (pinned; idles dimmed when nothing applies), <b>off</b> (hidden until shown again) — remembered per deck.</li><li>Drag a toolbar and it becomes <b>anchored</b> (⚓): it opens at that spot from then on; ⚓ or a double-click on the grip releases it.</li><li>{kbd("Ctrl/Cmd+Shift+O")} / {kbd("H")} open Outline / Tree directly.</li></ul>', True)}
  {mini("monitor","Detachable panels",'<ul><li><b>⧉</b> on the menu (structure and assistant included) or on the shape toolbar moves it into a <b>window of its own</b>: a Document Picture-in-Picture window in Chrome and Edge — always on top, no browser chrome, anywhere on the desktop, even off the browser — or a pop-up elsewhere.</li><li>The panel keeps working on the deck from there; closing the window, ✕ or Esc brings it back.</li><li>While the menu is away, a right-click on the slide opens a compact <b>picker</b> at the pointer with the same <i>Select at this point</i> list and <i>Edit text</i>.</li></ul>', True)}
</div></div>''')

add(0, header(TM, "EDITING 6 · ASK THE ASSISTANT", "An AI request from inside the deck, with the slide as context. The viewer brings their own endpoint and key; nothing is baked in.") + f'''
<div class="body fill"><div class="grid4" style="gap:24px">
  {mini("chat","Ask",'<ul><li>A <b>prompt</b> from the drop-down: <i>Free request</i>, <i>Review the slide</i>, <i>Proofread the text</i>, <i>Tighten the copy</i>, <i>Speaker notes</i>, <i>Restyle the selection</i>, <i>Rewrite the selection\'s text</i>, plus your own.</li><li>A request box for extra instructions.</li></ul>', True)}
  {mini("link","Attach",'<ul><li><b>Screenshot of the slide</b> (tab capture; toolbars hidden, cropped to the slide).</li><li><b>Slide source</b> — its HTML plus the CSS rules it uses; embedded images travel as small placeholders, so photos cost no tokens.</li><li><b>Selected element source.</b></li><li><b>Clipboard image</b> — paste, drop or <i>Read clipboard</i>.</li></ul>', True)}
  {mini("refresh","Reply",'<ul><li><b>Show the answer</b> in the panel, with <i>Copy</i> and <i>Apply to selection</i>.</li><li><b>Replace the selected element</b>: the reply is the element\'s replacement HTML — same tag, scripts stripped, recorded as a normal edit — with <b>Undo</b>.</li><li>Right-click a row in Outline or Tree for an <i>Ask about…</i> popup on that element.</li></ul>', True)}
  {mini("key","Settings",'<ul><li><b>Providers</b>: Anthropic, Azure-hosted Anthropic (Microsoft Foundry), OpenAI-compatible, Azure OpenAI, DeepSeek.</li><li>Endpoint, model or deployment, API key (kept in this browser, or for the tab only), <i>Test</i>.</li><li>Settings are kept per provider; nothing is defaulted — a missing value blocks the request with a message.</li><li>The page calls the endpoint directly; a provider that blocks browser calls needs a gateway.</li></ul>', True)}
</div>
<div class="insight"><span class="tag">Privacy</span><p>Each attachment is a checkbox, so the viewer decides per request what leaves the machine. The key never enters the deck file or a saved copy.</p></div>
</div>''')

add(0, header(TM, "EDITING 7 · KEEPING, SHARING AND PRINTING YOUR CHANGES", "The deck on disk never changes by itself. Edits live in the browser until you save a copy.") + f'''
<div class="body fill"><div class="two">
  <div>
    {lst([("db","<b>Edits persist in the browser</b>, keyed by the file: reload the deck and they are still there. They exist only in that browser — the original file is untouched."),
          ("download","<b>Save edited copy</b> downloads <code class='code'>&lt;name&gt;-edited.html</code>: your edits applied to a pristine snapshot of the deck taken at load. The copy is still one self-contained file and carries the editor itself."),
          ("refresh","<b>Discard changes on this slide</b> restores the slide under the pointer (the hint counts its changes); <b>Discard edits</b> restores every slide."),
          ("refresh","<b>Refresh the tools later</b>: <code class='code'>node deck.rebuild.mjs</code> replaces only the editor block with the one the skill ships now, keeps a backup, re-runs the strict gate and re-exports the PDF. <code class='code'>--check</code> only reports CURRENT or REBUILD NEEDED."),
          ("doc","<b>Export to PDF</b> applies the same print layout as the command-line exporter and opens the print dialog: choose <i>Save as PDF</i> in Chrome or Edge. Page size, zero margins and backgrounds are preset — one page per slide, identical to the CLI export.")])}
  </div>
  <div>
    <div class="seclbl">What the editor can and cannot do</div>
    <table class="tbl" style="width:100%;margin-top:18px;border-collapse:collapse"><thead><tr><th>In the deck, by anyone</th><th>By regenerating, with the skill</th></tr></thead><tbody>
      <tr><td>Text, formatting, size, font, palette colour, alignment</td><td>New images or photos</td></tr>
      <tr><td>Geometry and style of shapes: fill, border, radius, opacity, shadow</td><td>New elements, new slides, new layouts</td></tr>
      <tr><td>Order, alignment, distribution, groups of several shapes</td><td>Structural changes to the page</td></tr>
      <tr><td>AI-assisted rewrites and restyles of an element</td><td>Anything outside the skill's fonts and palette</td></tr>
    </tbody></table>
    <div class="band" style="margin-top:26px"><p class="band-t">A PDF of an edited deck is printed from the saved copy — the CLI prints what is on disk.</p></div>
  </div>
</div></div>''')

# ================================================================= SECTION 03 — developers
divider("03", "Section 03", "How to<br>extend it", "How it is built: the folder, the scripts and libraries, the editor's internals, the PDF path, the configuration hook and the rules to keep.")

add(0, header(DV, "HOW IT IS BUILT, IN FIVE LAYERS", "Each layer rests on the one below; extend the one you need. The editor is the layer that turns a deck into something recipients can change themselves.") + dg(SVG["layers"]))

add(0, header(DV, "ANATOMY OF THE SKILL FOLDER", "15 MB, 14 of them photography; one Markdown file that is the whole behaviour, six scripts, four libraries, and the design system with its assets.") + f'''
<div class="body fill"><div class="cols" style="grid-template-columns:1fr 1fr;gap:60px">
  <div class="tree">
<span class="d">nbg-design/</span><span class="cm">plugin nbg-design v1.15.0 · aihub-skills marketplace · MIT</span><br>
├─ <b>SKILL.md</b><span class="sz">56 KB · 385 lines</span><span class="cm">the single source of behaviour, defaults, assets, guardrails</span><br>
├─ <span class="d">NBG-Design/</span><br>
│&nbsp;&nbsp;├─ NBG Design System.html<span class="sz">39 KB</span><span class="cm">visual reference</span><br>
│&nbsp;&nbsp;├─ slide-templates.jsx<span class="sz">32 KB</span><span class="cm">nine 1920×1080 templates</span><br>
│&nbsp;&nbsp;├─ tweaks-panel.jsx<span class="sz">24 KB</span><span class="cm">tweak / edit helper reference</span><br>
│&nbsp;&nbsp;├─ <span class="d">assets/</span><span class="sz">14 MB</span><span class="cm">3 logos + 27 photos, each with a .datauri.txt</span><br>
│&nbsp;&nbsp;└─ <span class="d">screenshots/</span><span class="cm">8 reference renders</span><br>
├─ <span class="d">scripts/</span><span class="sz">452 KB</span><br>
│&nbsp;&nbsp;├─ embed-assets.mjs · add-deck-menu.mjs · verify-deck.mjs<br>
│&nbsp;&nbsp;├─ write-rebuild-script.mjs · screenshot-deck.mjs · export-pdf.mjs · README.md<span class="sz">46 KB</span><br>
│&nbsp;&nbsp;└─ <span class="d">lib/</span> find-browser.mjs · cdp.mjs · print-layout.js · <b>deck-menu.js</b><span class="sz">317 KB</span><br>
└─ <span class="d">references/</span><span class="cm">design decisions, functions, config guide, issue register</span>
  </div>
  <div>
    {lst([("doc","<b>SKILL.md is the contract.</b> Inputs, defaults, palette, templates, embedding rules, the editor's behaviour, the PDF rules and the quality checklist — all in one file, no separate configuration."),
          ("globe","<b>Everything resolves relative to the skill root</b>, never to the working directory: the scripts find the assets next to themselves, so the skill works from any folder, on any machine, through a symlink."),
          ("link","<b>Installed as a project skill</b> via a symlink in <code class='code'>.claude/skills/</code> pointing at the plugin checkout, so the working tree is the live skill."),
          ("db","<b>References are history, not behaviour</b>: every design decision from v1.3 to v1.15 is recorded with its rationale, mechanism and verification in project-design.md.")], True)}
  </div>
</div></div>''')

rows = [("embed-assets.mjs","Replaces every <code class='code'>&#123;&#123;TOKEN&#125;&#125;</code> with the verbatim data URI; tokens map to files by name; fails loudly on a missing asset.","no","0 / 1"),
        ("add-deck-menu.mjs","Inlines one <code class='code'>&lt;script id=\"nbg-deck-menu-script\" data-nbg-deck-menu=\"12\"&gt;</code> before the last <code class='code'>&lt;/body&gt;</code>: print-layout.js then deck-menu.js. Idempotent; upgrades older blocks; <code class='code'>--remove</code> strips.","no","0 / 1"),
        ("verify-deck.mjs","The gate: tokens, image paths, image count, size, bare-logo text, editor block version. <code class='code'>--strict</code> promotes the warnings to failures.","no","0 pass / 1 fail"),
        ("write-rebuild-script.mjs","Writes <code class='code'>&lt;deck&gt;.rebuild.mjs</code> next to the deck: a self-contained script that later re-embeds the skill's current editor block (backup, verify, re-export the PDF); <code class='code'>--check</code> only reports.","no","0 / 1 / 2"),
        ("screenshot-deck.mjs","Drives a headless browser over the DevTools protocol; isolates the Nth <code class='code'>.slide</code> in place, so <code class='code'>.active</code>, <code class='code'>.hidden</code>, inline-display and stacked decks all work; PNG per slide per viewport.","yes","0 / 1 / 3 no browser"),
        ("export-pdf.mjs","Lifts the host layer, prints with <code class='code'>Page.printToPDF</code> at the slide box, verifies pages = slides and slide box = page box.","yes","0 / 1 / 3 no browser")]
tr = "".join(f'<tr><td class="b"><span class="code">{a}</span></td><td>{b}</td><td class="c">{pill("browser","prog") if c=="yes" else pill("none","grey")}</td><td class="c">{d}</td></tr>' for a,b,c,d in rows)
add(0, header(DV, "THE SCRIPTS AND LIBRARIES", "Zero-dependency Node (18+). No npm install, no build step; six single-file scripts that import from lib/.") + f'''
<div class="body fill">
  <table class="tbl" style="width:100%;border-collapse:collapse"><thead><tr><th style="width:250px">Script</th><th>What it does</th><th style="width:130px;text-align:center">Needs</th><th style="width:190px;text-align:center">Exit codes</th></tr></thead><tbody>{tr}</tbody></table>
  <div class="grid4" style="margin-top:30px;gap:22px">
    {mini("search","lib/find-browser.mjs",'<p>Locates Chrome, Chromium or Edge; <code class="code">--browser</code>, <code class="code">NBG_BROWSER</code> or <code class="code">CHROME_BIN</code> override.</p>')}
    {mini("link","lib/cdp.mjs",'<p>A minimal DevTools-protocol client over <code class="code">--remote-debugging-pipe</code>: launch, navigate, evaluate, print, count pages.</p>')}
    {mini("doc","lib/print-layout.js",'<p>The print shim shared by the exporter and the in-deck menu, with a registry so every change can be undone after printing.</p>')}
    {mini("wrench","lib/deck-menu.js",'<p>The editor: ~4,000 lines of plain browser JavaScript. UI, editing, selection, SVG parts, toolbars, structure, assistant, persistence, saved copy, print orchestration.</p>')}
  </div>
</div>''')

add(0, header(DV, "INSIDE A DELIVERED DECK", "One HTML file carries the slides and the editor; the browser keeps the edits; three ways lead out.") + dg(SVG["arch"]))

add(0, header(DV, "INSIDE THE EDITOR", "How a standalone file:// deck can be edited, remembered and handed back without ever writing to itself.") + f'''
<div class="body fill"><div class="grid3" style="gap:28px">
  {mini("db","Edit records",'<ul><li>Every change is a record <code class="code">{{ path, original, … }}</code> where <b>path</b> is the child-index path from the root — cheap, exact, and the reason the DOM is never restructured.</li><li>Three kinds: <b>html</b> (text and selection-level formatting), <b>style</b> (block formatting, geometry, fill, border, z-index), <b>group</b> (the <code class="code">data-nbg-group</code> attribute).</li><li>Stored in <code class="code">localStorage</code> under <code class="code">nbg-deck-edits:&lt;path&gt;#&lt;title&gt;</code>; re-applied on load; a record whose original no longer matches is dropped.</li></ul>', True)}
  {mini("doc","Pristine snapshot",'<ul><li>When the inlined script runs — after the deck\'s own scripts, before any runtime element and before stored edits — it takes an <code class="code">outerHTML</code> snapshot.</li><li><b>Save edited copy</b> parses that snapshot with <code class="code">DOMParser</code>, applies the records, and downloads the result: it loads exactly like the original and carries the menu.</li><li>The print path uses the same print-layout shim as the CLI, then restores every class, style and attribute it touched.</li></ul>', True)}
  {mini("layers","Geometry, order, groups",'<ul><li>A "shape" is a positioned element, one with a background, border or shadow, or an image; otherwise the text block.</li><li>Pointer deltas are divided by the slide\'s scale (<code class="code">rect.width / offsetWidth</code>), so coordinates are artboard pixels.</li><li>Ordering ranks siblings by effective layer and writes an inline <code class="code">z-index</code>; a negative index makes the parent a stacking context with <code class="code">isolation: isolate</code>.</li><li>Rich <code class="code">contenteditable</code>, not <code class="code">plaintext-only</code>, because the latter forces <code class="code">pre-wrap</code> and re-flows titles.</li></ul>', True)}
</div>
<div class="insight"><span class="tag">Design rule</span><p>Inline style and attributes only, never DOM re-ordering — so every earlier record's path stays valid and every change stays reversible.</p></div>
</div>''')

add(0, header(DV, "THE PDF PATH", "The PDF is the deck, printed by the same engine that renders it. Nothing is re-laid out for paper.") + f'''
<div class="body fill"><div class="two">
  <div>
    <div class="seclbl">What the exporter does</div>
    {lst([("play","Opens the deck in headless Chrome, Chromium or Edge over the DevTools pipe — nothing to install."),
          ("layers","<b>Lifts the host layer only</b>: navigation toggles (<code class='code'>.active</code>, <code class='code'>.hidden</code>, inline display), the viewport-fit wrappers and scaling, buttons and counters; jumps animations to their end state; forces <code class='code'>print-color-adjust: exact</code>."),
          ("doc","Makes every top-level <code class='code'>.slide</code> visible in flow and prints with <code class='code'>Page.printToPDF</code>: page size = the measured slide box (1920×1080 px = 20 × 11.25 in), zero margins, backgrounds on, scale 1."),
          ("shield","<b>Verifies</b>: page count equals slide count and every slide box equals the page box; otherwise exit 1 (the PDF is still written for diagnosis). Exit 3 means no browser on the host.")], True)}
  </div>
  <div>
    <div class="seclbl">Rules that are not negotiable</div>
    {lst([("alert","<b>Aesthetics are frozen.</b> No print stylesheets, no resized slides, no font swaps \"to make it print\". A mismatch is a bug in the deck, fixed in the HTML."),
          ("alert","<b>No fakes.</b> No <code class='code'>window.print()</code> at A4, no browser Save-as-PDF with headers and margins, no office round-trips, no stitched screenshots."),
          ("doc","Every top-level slide carries the <code class='code'>slide</code> class — the exporter and the screenshot helper key on it."),
          ("globe","<b>Fonts come from the exporting host</b>: with Aptos absent, PDF and screenshots share the same fallback. Export where Aptos is installed if it must appear."),
          ("check","Never print a deck that fails <code class='code'>verify-deck --strict</code>. The in-deck <i>Export to PDF</i> inlines the very same shim, so viewers get an identical result.")], True)}
  </div>
</div></div>''')

add(0, header(DV, "THE CONFIGURATION HOOK: ONE EDITOR FOR ANY HTML PAGE", "Since v1.15 the editor is configured, not forked. A deck keeps its defaults; any other document declares what its editable regions are.") + f'''
<div class="body fill"><div class="two">
  <div>
    <div class="seclbl">window.nbgDeckMenuConfig</div>
    <div class="tree" style="margin-top:18px;background:#F5F8F6;border-radius:10px;padding:22px 26px">
<b>window.nbgDeckMenuConfig</b> = {{<br>
&nbsp;&nbsp;mode: <span class="d">'deck'</span> | 'page',<span class="cm">print: one page per slide, or the browser's pagination</span><br>
&nbsp;&nbsp;root: <span class="d">'.slide'</span>,<span class="cm">CSS selector of the editable regions (top-level matches)</span><br>
&nbsp;&nbsp;unit: 'Slide',<span class="cm">the word the UI uses: Slide, Page, Section …</span><br>
&nbsp;&nbsp;title: '…',<span class="cm">the label in the menu header</span><br>
&nbsp;&nbsp;aiSystem: '…'<span class="cm">replaces the assistant's system prompt</span><br>
}};
    </div>
    {lst([("gear","Written as the block's first statement by <code class='code'>addMenu(html, config)</code> / <code class='code'>buildMenuBlock(config)</code>; <code class='code'>readMenuConfig(html)</code> reads it back. The CLI has no flags: a deck always gets the defaults."),
          ("doc","<b>Page mode</b>: the print path adds only background and animation rules; wording says <i>page</i> / <i>Section N</i>; the assistant gets page-oriented prompts (Review the page, Summarise the page …).")], True)}
  </div>
  <div>
    <div class="seclbl">Reusing the skill in generators</div>
    {lst([("code","The AI Committee and Townhall decks are built by a <b>data-driven Python generator</b>: a helper section (icons, header, footer, pills, numbered circles) and one <code class='code'>add()</code> per slide, sharing one <code class='code'>deck.css</code> and <code class='code'>deck.js</code>."),
          ("link","The Townhall generator <b>slices slides out of the AI Committee generator</b> by comment markers and re-executes them, so a slide reused across decks is one line."),
          ("refresh","A <code class='code'>rebuild.sh</code> re-fetches the Google Slides source, compares its revision and text, detects skill or generator changes, and builds the next version through the five steps."),
          ("star","This deck was built the same way: a 500-line generator, the shared CSS plus 120 lines of additions, and the pipeline.")], True)}
  </div>
</div></div>''')

add(0, header(DV, "RULES THAT KEEP IT SAFE", "The constraints written into SKILL.md that every generated deck, and every future change to the skill, must respect.") + f'''
<div class="body fill"><div class="grid3" style="gap:28px">
  {mini("shield","Delivery",'<ul><li>Run order: author → embed → add menu → verify strict → rebuild script → screenshots → PDF. Never deliver a deck that fails the gate.</li><li>Every image a <code class="code">data:</code> URI; the logo always the bundled lockup.</li><li>Fit at 1366×768 and 1440×900; no element collisions; 32 px between groups, 72 px above the footer.</li><li>PDF only from the verified HTML, only through the exporter.</li></ul>', True)}
  {mini("key","Secrets & fallbacks",'<ul><li>The skill holds <b>no credentials</b>. Assistant keys are the viewer\'s and live only in their browser — never in the skill, a deck or a saved copy.</li><li><b>No fallback values</b>: a missing input is a question, a missing setting a message. Exceptions are written into the project memory first.</li><li>The agent never enters endpoints or keys for a recipient and never relies on the assistant for its own work.</li></ul>', True)}
  {mini("layers","Scope",'<ul><li><b>The look cannot be left</b> from the editor: fonts limited to the design-system stacks, colours to the NBG-inspired palette. The Tree tab\'s source editor is the one deliberate exception, for experts.</li><li>The editor changes text, formatting, geometry, order, groups and shape style. Images, new elements and structure are the skill\'s job — regenerate.</li><li><b>PowerPoint is out of scope</b>; newsletters, GPT and NotebookLM artifacts of the original project are excluded unless asked for.</li></ul>', True)}
</div></div>''')

# ================================================================= closing
add(0, header("Summary", "USING IT TOMORROW", "One line for recipients, six commands for builders, one place where it lives.") + f'''
<div class="body fill"><div class="two">
  <div>
    <div class="seclbl">Tell the recipient</div>
    <div class="band" style="margin-top:18px;text-align:left"><p class="band-t" style="text-align:left;font-size:22px;line-height:1.5">Double-click any text to edit it (Enter applies, Esc cancels). Right-click for <b>Resize / move shape</b> (Shift+click or Shift+drag selects several; the toolbar orders, aligns, distributes and groups them), <b>Edit SVG</b> (the parts of a drawn icon, diagram or chart), <b>Ask the assistant</b>, <b>Export to PDF</b> and <b>Save edited copy</b>. After a skill update, <code class="code">node deck.rebuild.mjs</code> refreshes the editing tools and the PDF.</p></div>
    <div class="seclbl" style="margin-top:36px">Where it lives</div>
    {lst([("link","<code class='code'>~/officework/.claude/skills/nbg-design</code> → the plugin checkout in the aihub-skills marketplace (dev repo <code class='code'>aihub-skills-dev</code>)."),
          ("doc","Deliverables per deck in their own folder; generators in <code class='code'>deck-work-*</code>; the Townhall deck rebuilds with <code class='code'>rebuild.sh</code>.")], True)}
  </div>
  <div>
    <div class="seclbl">The six commands</div>
    <div class="tree" style="margin-top:18px;background:#F5F8F6;border-radius:10px;padding:22px 26px;font-size:16px">
<span class="cm" style="margin:0">S=&lt;skill-root&gt;/scripts</span><br>
node $S/embed-assets.mjs deck.html<span class="cm">tokens → data URIs</span><br>
node $S/add-deck-menu.mjs deck.html<span class="cm">inline the editor</span><br>
node $S/verify-deck.mjs deck.html --strict<span class="cm">the gate</span><br>
node $S/write-rebuild-script.mjs deck.html<span class="cm">deck.rebuild.mjs, delivered too</span><br>
node $S/screenshot-deck.mjs deck.html -o shots<span class="cm">look</span><br>
node $S/export-pdf.mjs deck.html<span class="cm">one page per slide</span>
    </div>
    <div class="seclbl" style="margin-top:36px">Next steps</div>
    {lst([("steps","Fill the Townhall placeholders (slides 4, 10, 13, 14) and re-run."),
          ("users","Hand a deck to two colleagues, watch them edit it, and feed the friction back into the next release."),
          ("star","Commit and push the v1.18 working tree of the plugin.")], True)}
  </div>
</div></div>''')

# =============================================================== CSS / HTML
CSS = "\n".join(l for l in open(f"{BASE}/deck.css").read().splitlines() if "{{PHOTO_STREET}}" not in l and "{{PHOTO_PARTHENON}}" not in l) + open(f"{HERE}/extra.css").read()
JS = open(f"{BASE}/deck.js").read()
html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The nbg-design skill — a presentations skill inspired by the NBG brand</title>
<style>{CSS}</style></head>
<body>
<div id="frame"><div id="stage">
{"".join(SLIDES)}
</div></div>
<div id="nav"><button id="prev" aria-label="Previous">‹</button><span id="ctr"></span><button id="next" aria-label="Next">›</button></div>
<script>{JS}</script>
</body></html>'''
open(OUT, "w").write(html)
print("slides:", len(SLIDES), "bytes:", len(html))
