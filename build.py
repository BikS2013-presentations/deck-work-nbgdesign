# Generator for "The nbg-design skill — how it is built, how it works, how its decks are edited".
# Self-contained: executes the shared helper section in base/helpers.py and uses base/deck.css + base/deck.js (briefing look).
import re, sys
sys.path.insert(0, "/Users/giorgosmarinos/officework/deck-work-nbgdesign")
from diagrams import SVG
HERE = "/Users/giorgosmarinos/officework/deck-work-nbgdesign"
BASE = f"{HERE}/base"
OUT = f"{HERE}/deck.html"
src = open(f"{BASE}/helpers.py").read()
helpers = src.split("# =============================================================== SLIDES")[0]
ns = {}
exec(compile(helpers, "helpers", "exec"), ns)
ico, header, pill, numc, add, motif = ns["ico"], ns["header"], ns["pill"], ns["numc"], ns["add"], ns["motif"]
SLIDES = ns["SLIDES"]; ACC = ns["ACC"]

def dg(svg): return f'<div class="body dgb"><div class="dg">{svg}</div></div>'
EX, TM, DV = "01 · What it makes possible", "02 · Ask, build, edit", "03 · Make it your own"

import base64
def img_uri(name):
    return "data:image/png;base64," + base64.b64encode(open(f"{HERE}/assets/{name}","rb").read()).decode()
def fig(name, title, cap):
    return f'<figure class="shotfig"><div class="shotbox"><img src="{img_uri(name)}" alt="{title}"></div><figcaption><b>{title}</b>{cap}</figcaption></figure>'
def tbp(active, rows):
    tabs = "".join(f'<span class="tt{" on" if k==active else ""}">{k}</span>' for k in ("Text","Shape","SVG"))
    return f'<div class="tbp"><div class="tbp-side"><span class="grip">⋮⋮</span><span class="ic">⚓</span><span class="ic">⧉</span></div><div class="tbp-main"><div class="tbp-tabs">{tabs}</div>{rows}</div></div>'
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
    <div class="cover-meta"><span>Skill v1.19.0</span><span class="dot"></span><span class="acc">Sep 2026</span></div>
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
      <li class="ag-item on"><span class="ag-num">01</span><span class="ag-lbl">WHAT IT MAKES POSSIBLE</span></li>
      <li class="ag-item on"><span class="ag-num">02</span><span class="ag-lbl">ASK, BUILD, EDIT</span></li>
      <li class="ag-item on"><span class="ag-num">03</span><span class="ag-lbl">MAKE IT YOUR OWN</span></li>
    </ul>''')

# ================================================================= SECTION 01 — executives
divider("01", "Section 01", "What it<br>makes possible", "A design system inspired by the NBG brand, a build pipeline and an in-deck editor, packaged as one Claude skill.")

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
    {mini("rocket","Speed",'<p><b>From any content to a finished deck in minutes</b> — a brief in chat, notes, a document, a spreadsheet, an existing deck or a Google Slides draft. Once the generator exists, every re-run is one command.</p>', True)}
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
add(0, header(EX, "THE NEWEST CAPABILITIES", "What arrived most recently in the skill. Each is explained in section 02; the recipient needs no new tooling for any of them.") + f'''
<div class="body fill"><div class="grid4" style="gap:24px">
  {mini("layers","Edit SVG",'<ul><li>A drawn icon, diagram or chart is no longer a picture: its <b>parts</b> — paths, shapes, text, groups — move, resize, recolour, reorder, duplicate and reword in place.</li><li>Path data is never rewritten; one reversible record per drawing.</li></ul>', True)}
  {mini("gear","One toolbar, three tabs",'<ul><li><b>Text</b>, <b>Shape</b> and <b>SVG</b> share one floating panel; the tab of the editor in use comes to the front by itself.</li><li>Pin, hide, anchor or detach it — remembered per deck.</li></ul>', True)}
  {mini("users","Smarter selection",f'<ul><li>{kbd("Shift")}+click takes the smallest shape under the pointer; {kbd("Ctrl/Cmd")}+click selects everything inside a shape.</li><li>A compact <b>picker</b> at the pointer when the menu is detached; the <b>Stack</b> list for nested levels.</li></ul>', True)}
  {mini("refresh","The rebuild script",'<ul><li>Every deck ships with <code class="code">&lt;deck&gt;.rebuild.mjs</code>: after a skill update it re-embeds the newer editing tools, keeps a backup, re-verifies and re-exports the PDF.</li><li><code class="code">--check</code> only reports.</li></ul>', True)}
</div>
<div class="insight"><span class="tag">Also</span><p>27 bundled photos with a written catalogue (Athens at dusk, data centre, network, microchip, security, developer, team analytics — three takes each); assistant settings kept <b>per provider</b> and an <i>Ask about…</i> popup on any row of the Outline or Tree; a full set of <b>keyboard shortcuts</b> for text, shapes, SVG parts and panels; PDFs whose shadows render correctly in <b>macOS Preview</b> (1.19).</p></div>
</div>''')

divider("02", "Section 02", "Ask,<br>build, edit", "Asking for a deck, what happens in between, the quality gates, and everything the right-click editor can do.")

add(0, header(TM, "INSTALLING THE SKILL", "One public marketplace, two commands. No npm install, no build step: the skill is Markdown, assets and zero-dependency Node scripts.") + f'''
<div class="body fill"><div class="cols" style="grid-template-columns:1fr 1fr;gap:56px;align-items:start">
  <div>
    <div class="seclbl">In Claude Code</div>
    <div class="cmdblock">
      <div class="cmdl"><span class="cm"># 1 · register the marketplace (once)</span></div>
      <div class="cmdl">/plugin marketplace add BikS2013-coding-agents/nbg-design</div>
      <div class="cmdl"><span class="cm"># 2 · install the plugin from it</span></div>
      <div class="cmdl">/plugin install nbg-design@nbg-design</div>
      <div class="cmdl"><span class="cm"># 3 · restart Claude Code, then check</span></div>
      <div class="cmdl">/plugin list</div>
      <div class="cmdl"><span class="cm"># later · pick up a new release</span></div>
      <div class="cmdl">/plugin marketplace update nbg-design</div>
      <div class="cmdl">claude plugin update nbg-design@nbg-design</div>
    </div>
    {lst([("link","The marketplace is the public repository <code class='code'>github.com/BikS2013-coding-agents/nbg-design</code> (branch <code class='code'>working</code>); its name and the plugin's name are both <code class='code'>nbg-design</code>, hence <code class='code'>nbg-design@nbg-design</code>."),
          ("check","From then on Claude uses the skill by itself whenever a presentation in this look is asked for; say <i>nbg-design</i> to make sure.")], True)}
  </div>
  <div>
    <div class="seclbl">What lands on the machine</div>
    {lst([("doc","The plugin is cached under <code class='code'>~/.claude/plugins/cache/nbg-design/nbg-design/&lt;version&gt;/</code>; the skill root is its <code class='code'>skills/nbg-design/</code> folder — the <code class='code'>&lt;skill-root&gt;</code> the pipeline commands use."),
          ("wrench","<b>Requirements</b>: Node 18 or newer for the scripts. Chrome, Chromium or Edge only for screenshots and the PDF; without a browser the strict verifier is still the gate and the PDF is exported elsewhere."),
          ("key","<b>Nothing to configure.</b> The skill holds no credentials and reads no configuration file; assistant keys are entered by each viewer in their own browser."),
          ("refresh","A delivered deck outlives the install: after an update, <code class='code'>node &lt;deck&gt;.rebuild.mjs</code> re-embeds the newer editing tools — pointed at the new cache folder with <code class='code'>--scripts</code> or <code class='code'>NBG_DESIGN_SCRIPTS</code> when the recorded one is gone.")], True)}
  </div>
</div></div>''')

add(0, header(TM, "ASKING FOR A DECK", "What the skill needs from you, what it decides by itself, and what it refuses to do.") + f'''
<div class="body fill"><div class="grid3" style="gap:28px">
  {mini("chat","It always asks for",'<ul><li><b>Topic</b> — what the deck is about.</li><li><b>Audience</b> — who reads it; this sets depth and tone.</li><li><b>Slide count or depth</b> — 8, 16, 20+.</li><li>Whether the bundled design-system files may be changed (they normally are not).</li></ul>', True)}
  {mini("check","Approved defaults",'<ul><li><b>Language</b>: English. <code class="code">gr</code> and <code class="code">bi</code> exist; anything else must come from you.</li><li><b>Output</b>: HTML. A PDF is always exported from the finished HTML, never authored separately.</li><li><b>Logo</b>: shown, unless you ask to hide it.</li><li>Cover first, dividers between sections, content slides in between.</li></ul>', True)}
  {mini("alert","It will not",'<ul><li>Produce or convert to <b>PowerPoint</b>.</li><li>Guess a missing input or substitute a fallback value.</li><li>Put an API key, token or endpoint into a deck or into the skill.</li><li>Reference an image by a path: every image is embedded, or the deck fails the gate.</li></ul>', True)}
</div>
<div class="insight"><span class="tag">Any content is a source</span><p>A brief typed in chat, meeting notes, a Word or Markdown document, a spreadsheet, a report, an existing HTML deck, or a Google Slides draft (read through the Slides API and rebuilt 1:1, page count kept). The skill turns whatever it is given into a cover, dividers and content slides; it only asks for what it cannot infer.</p></div>
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
add(0, header(TM, "WHAT A VIEWER CAN DO", "Five families of actions, all in the file itself, all recorded and reversible. The slides that follow walk through them, and end with every keyboard shortcut.") + dg(SVG["tree"]))

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
  {tbp("Text", TB)}
  <div class="two" style="margin-top:36px">
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
  {tbp("Shape", STB)}
  <div class="two" style="margin-top:30px">
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
            ("layers","<b>Edit SVG</b>: a drawn icon, diagram or chart has parts of its own — the next two slides. The SVG as a whole is still a shape: <i>Resize / move shape</i> sizes and places it.")], True)}
    </div>
  </div>
</div>''')

GTB = '''<div class="tbar"><span class="grip">⋮⋮</span><span class="sel">Parts ▾</span><span class="sep"></span><span class="lab">X</span><span class="sel">240</span><span class="lab">Y</span><span class="sel">256</span><span class="lab">W</span><span class="sel">280</span><span class="lab">H</span><span class="sel">88</span><span class="sep"></span><span class="lab">Fill</span><span class="dot" style="background:#00ADBF"></span><span class="dot" style="background:#003841"></span><span class="dot" style="background:#fff"></span><span class="sel">None ▾</span><span class="lab">Stroke</span><span class="dot" style="background:#003841"></span><span class="sel">1.5 ▾</span><span class="lab">Opacity</span><span class="sel">100</span><span class="sep"></span><span class="lab">Text</span><span class="sel" style="min-width:150px">deck-menu.js</span><span class="sep"></span><span class="lab">Order</span><span class="bt">Front</span><span class="bt">Forward</span><span class="bt">Backward</span><span class="bt">Back</span><span class="sep"></span><span class="bt">Duplicate</span><span class="bt">Delete</span><span class="bt">All</span><span class="sep"></span><span class="bt">Reset SVG</span><span class="bt on">Done</span></div>'''
add(0, header(TM, "EDITING 4 · EDIT SVG: THE PARTS OF A DRAWING", "Right-click a drawn icon, diagram or chart → Edit SVG. The drawing gets a dashed outline and every part inside it becomes a thing you can pick.") + f'''
<div class="body fill">
  {tbp("SVG", GTB)}
  <div class="two" style="margin-top:30px">
    <div>
      <div class="seclbl">Entering and selecting</div>
      {lst([("hand","<b>Three ways in</b>: right-click the drawing → <i>Edit SVG</i>; double-click a drawing that is already selected as a shape; click one of its parts in the <b>Tree</b> tab."),
            ("layers","<b>What a part is</b>: a path, rect, circle, ellipse, line, polygon, text, image, <code class='code'>use</code> reference or group. Nothing inside <code class='code'>defs</code>, clip paths, masks or symbols."),
            ("search",f"<b>A click picks the innermost part</b> under the pointer — through the frame of a selected group too, so its members are one click away. {kbd('Shift')}+click adds a part (or removes a selected one); {kbd('Ctrl/Cmd')}+click selects what is inside the part there; {kbd('Ctrl/Cmd+A')} or <b>All</b> every top-level part."),
            ("refresh",f"{kbd('Tab')} selects the enclosing group, {kbd('Shift+Tab')} the first part inside; the <b>Parts</b> list offers every part in drawing order.")], True)}
    </div>
    <div>
      <div class="seclbl">Moving, resizing, styling</div>
      {lst([("hand",f"The selection gets a frame with eight handles — several parts: one frame spanning them, a dashed mark per part. <b>Drag inside</b> to move, <b>a handle</b> to resize ({kbd('Shift')} keeps proportions); arrows nudge by one SVG unit, {kbd('Shift')} ten, {kbd('Alt')}+arrows resize — all selected parts together, keeping their places."),
            ("wrench","<b>The SVG row</b>: X / Y / W / H in the drawing's own units; <b>fill</b> and <b>stroke</b> from the palette, <i>None</i> or <i>Default</i>; <b>stroke width</b>; <b>opacity</b>; the <b>text</b> of a label (one run; Enter applies)."),
            ("layers",f"<b>Order</b> in the drawing ({kbd('Ctrl/Cmd+]')} / {kbd('[')}), <b>Duplicate</b> ({kbd('Ctrl/Cmd+D')}; copies sit on the originals), <b>Delete</b> ({kbd('Delete')}), <b>Reset SVG</b> (every part as designed), <b>Done</b>."),
            ("check",f"{kbd('Esc')} deselects the part, then ends the session; {kbd('Enter')}, <i>Done</i>, <i>Finish SVG editing</i> in the menu or a click outside the drawing end it too.")], True)}
    </div>
  </div>
</div>''')

add(0, header(TM, "EDITING 5 · WHAT AN SVG EDIT WRITES", "Geometry goes into attributes, colour into presentation attributes, and the whole drawing becomes one reversible record. The path data itself is never touched.") + f'''
<div class="body fill"><div class="grid3" style="gap:28px">
  {mini("layers","Geometry, never path data",'<ul><li>A move or resize is written in the part\'s <b>parent coordinate system</b>: the screen box is mapped back through the parent\'s transform.</li><li>A rect or image without a transform gets plain <code class="code">x / y / width / height</code>; a pure move of text, a <code class="code">use</code>, a circle, an ellipse or a line changes <code class="code">x / y</code>, <code class="code">cx / cy</code> or <code class="code">x1…y2</code>.</li><li>Everything else — a path, a scaled text, a group — gets a <code class="code">matrix()</code> <b>prepended</b> to its own transform. The <code class="code">d</code> attribute stays as drawn.</li></ul>', True)}
  {mini("doc","Colours, order, text",'<ul><li>Fill, stroke, stroke width and opacity become <b>presentation attributes</b>, or the inline style property when the part already sets one — so the change wins over the stylesheet without touching it.</li><li>Order is a real move in the drawing order inside the parent; Duplicate clones without ids and places the copy after the original.</li><li>The text field replaces the one run of a <code class="code">&lt;text&gt;</code>; labels with several runs are edited as source in the Tree tab.</li></ul>', True)}
  {mini("db","One record for the whole drawing",'<ul><li>Every operation records the <code class="code">&lt;svg&gt;</code> element\'s inner HTML as a single <b>html</b> edit — the same kind as a text edit — so it persists in the browser, lands in the saved copy, is discarded per slide and prints.</li><li><b>Reset SVG</b> drops that record. Sessions are exclusive: editing text, selecting a shape or preparing a print ends the SVG session first.</li><li>SVG text is never <code class="code">contenteditable</code>; the SVG as a whole is still a shape for <i>Resize / move shape</i>.</li></ul>', True)}
</div>
<div class="insight"><span class="tag">Known limits</span><p>The frame is the axis-aligned screen box: a part inside a <b>rotated</b> group is moved correctly in that group\'s space, but its frame does not rotate. Parts sized in percentages or with a CSS transform take the matrix path. The five diagrams in this deck are editable this way.</p></div>
</div>''')

add(0, header(TM, "EDITING 6 · SEVERAL SHAPES AT ONCE", "Text blocks, cards, panels and images alike. The frame spans the selection and each member gets a dashed mark.") + f'''
<div class="body fill"><div class="grid3" style="gap:28px">
  {mini("users","Selecting",f'<ul><li>{kbd("Shift")}+click adds the smallest shape under the pointer, or removes it when it is already selected.</li><li>{kbd("Shift")}+drag on the slide draws a box: every top-level shape fully inside is added.</li><li>{kbd("Ctrl/Cmd+A")} selects every top-level shape of the slide; {kbd("Ctrl/Cmd")}+click selects everything inside the shape under the pointer; a shape with nothing inside is picked alone, even a group member, and on the same spot again cycles outward.</li><li>The menu offers <i>Add to</i> / <i>Remove from selection</i> / <i>Select all shapes</i>; the <b>Outline</b> tab does it with checkboxes.</li></ul>', True)}
  {mini("layers","Arranging",f'<ul><li><b>Order</b>: bring to front / forward, send backward / to back ({kbd("Ctrl/Cmd+]")} and {kbd("[")}, {kbd("Shift")} for front / back).</li><li><b>Align</b> left, centre, right, top, middle, bottom — relative to the selection\'s own box or to the slide.</li><li><b>Distribute</b> horizontally or vertically with equal gaps; the first and last stay put.</li><li>Dragging moves all, handles scale all proportionally, every style control applies to all.</li></ul>', True)}
  {mini("link","Grouping",f'<ul><li><b>Group</b> ({kbd("Ctrl/Cmd+G")}) / <b>Ungroup</b> ({kbd("Ctrl/Cmd+Shift+G")}).</li><li>A group is logical: members carry a <code class="code">data-nbg-group</code> mark and always select, move, resize, align and order together.</li><li>Groups persist in the browser, land in the saved copy and are removed by <i>Discard edits</i>.</li><li>The page structure is never rebuilt: ordering is an inline z-index, grouping an attribute, so every earlier edit stays valid.</li></ul>', True)}
</div>
<div class="insight"><span class="tag">Nested shapes</span><p>A click lands on one level only. Use <b>Select at this point</b> in the menu (front-most first, containers, shapes behind), the toolbar's <b>Stack</b> list, or {kbd('Tab')} / {kbd('Shift+Tab')} to reach the others.</p></div>
</div>''')

add(0, header(TM, "EDITING 7 · STRUCTURE, WINDOWS AND THE PICKER", "The Outline and Tree tabs, panels that leave the browser window, and the compact menu that takes over while the big one is away.") + f'''
<div class="body fill"><div class="grid3" style="gap:28px">
  {mini("search","Outline & Tree",'<ul><li><b>Outline</b>: the slide\'s shapes nested by containment — cards, text blocks, images — with kind icons, sizes, group badges, a text filter, checkboxes, All / None. Click a name to select it, Shift+click adds.</li><li><b>Tree</b>: the slide\'s HTML elements, synced both ways with the selection; double-click edits a text; hovering outlines the element on the slide.</li><li>Under the tree, the selected element\'s <b>editable source</b> behind a draggable splitter. <i>Apply</i> records it like any other edit; scripts are stripped. For people who know what they are doing.</li></ul>', True)}
  {mini("monitor","Detachable panels",'<ul><li><b>⧉</b> on the menu (structure and assistant included) or on the toolbar moves it into a <b>window of its own</b>: a Document Picture-in-Picture window in Chrome and Edge — always on top, no browser chrome, anywhere on the desktop, even off the browser — or a pop-up elsewhere.</li><li>The panel keeps working on the deck from there; closing the window, ✕ or Esc brings it back.</li><li>A detached panel is pinned: it idles rather than disappears when nothing is selected. Screenshots asked from a detached assistant use that window\'s permission.</li></ul>', True)}
  {mini("hand","The picker",f'<ul><li>While the menu is detached, or open on a panel tab, a <b>right-click on the slide opens a compact picker</b> at the pointer instead of the full menu.</li><li>It holds the same <i>Select at this point</i> hierarchy — front-most first, containers and shapes behind — plus <i>Edit text</i>.</li><li>A click selects, {kbd("Shift")}+click adds, {kbd("Esc")} closes it. The big menu keeps its place and its tab.</li><li>{kbd("Ctrl/Cmd+Shift+O")} / {kbd("H")} open Outline / Tree directly; {kbd("Ctrl/Cmd+Shift+L")} the assistant.</li></ul>', True)}
</div></div>''')

add(0, header(TM, "EDITING 8 · THE TOOLBAR: ONE PANEL, THREE TABS", "Text, Shape and SVG share one floating panel with one grip, one anchor and one detach button. One tab's row shows at a time.") + f'''
<div class="body fill">
  <div class="tbstack">{tbp("Text", TB)}{tbp("Shape", STB)}{tbp("SVG", GTB)}</div>
  <div class="two" style="margin-top:22px">
    <div>
      {lst([("refresh","<b>The editor in use takes the front.</b> Text being edited, or a selection made only of text blocks → <b>Text</b>; any other selection → <b>Shape</b>; a drawing in SVG editing → <b>SVG</b>. The panel appears with the selection and follows it."),
            ("hand","<b>A tab you click stays in front</b> until another editor takes over. A tab whose editor has nothing to work on is <b>dimmed but opens</b>: its row idles with the controls greyed."),
            ("gear","<b>Three modes per tab</b> — auto (with the selection), on (pinned), off (hidden until shown again) — set from a row's ✕ or the menu's <i>Toolbars</i> section, and remembered per deck in that browser.")], True)}
    </div>
    <div>
      {lst([("pin","<b>Anchored</b>: drag the panel by its grip and it opens at that spot from then on, showing ⚓; click ⚓ or double-click the grip and it follows the selection again."),
            ("monitor","<b>Detached</b>: ⧉ moves the whole panel, tabs included, into a window of its own (always on top in Chrome and Edge). It keeps working on the deck; closing the window brings it back."),
            ("shield","<b>Every tab adapts to the selection</b>: the Shape row shows the selection's geometry and style, the SVG row the part's units, and the Text row formats selected text blocks without entering edit mode.")], True)}
    </div>
  </div>
</div>''')

add(0, header(TM, "EDITING 9 · THE ASSISTANT, AS IT LOOKS", "Three real screenshots from this deck: the Settings view, the Ask view with a card selected, and the Ask-about popup opened from a row of the Outline.") + f'''
<div class="body fill"><div class="grid3 shots" style="gap:32px">
  {fig("assistant-settings.png", "Settings", "Provider, endpoint, model or deployment, API key and where it is remembered. Settings are kept per provider; <i>Standard values</i> fills a fixed endpoint, <i>Test</i> sends a one-line request. The key never enters the deck file.")}
  {fig("assistant-ask.png", "Ask", "A prompt from the drop-down with its text shown beneath, a request box, the four attachments as checkboxes, the reply mode, and what is selected. <i>Send</i> shows the answer here, or replaces the selected element with Undo.")}
  {fig("assistant-popup.png", "Ask about… on a row", "Right-click a row of the Outline or Tree: a compact popup for that element, with its text, a request box, <i>Answer me</i> / <i>Replace this element</i>, the prompt and the attachments. It stays put until you close it and never opens the panel by itself.")}
</div></div>''')

add(0, header(TM, "EDITING 10 · ASK THE ASSISTANT", "An AI request from inside the deck, with the slide as context. The viewer brings their own endpoint and key; nothing is baked in.") + f'''
<div class="body fill"><div class="grid4" style="gap:24px">
  {mini("chat","Ask",'<ul><li>A <b>prompt</b> from the drop-down: <i>Free request</i>, <i>Review the slide</i>, <i>Proofread the text</i>, <i>Tighten the copy</i>, <i>Speaker notes</i>, <i>Restyle the selection</i>, <i>Rewrite the selection\'s text</i>, plus your own.</li><li>A request box for extra instructions.</li></ul>', True)}
  {mini("link","Attach",'<ul><li><b>Screenshot of the slide</b> (tab capture; toolbars hidden, cropped to the slide).</li><li><b>Slide source</b> — its HTML plus the CSS rules it uses; embedded images travel as small placeholders, so photos cost no tokens.</li><li><b>Selected element source.</b></li><li><b>Clipboard image</b> — paste, drop or <i>Read clipboard</i>.</li></ul>', True)}
  {mini("refresh","Reply",'<ul><li><b>Show the answer</b> in the panel, with <i>Copy</i> and <i>Apply to selection</i>.</li><li><b>Replace the selected element</b>: the reply is the element\'s replacement HTML — same tag, scripts stripped, recorded as a normal edit — with <b>Undo</b>.</li><li>Right-click a row in Outline or Tree for an <i>Ask about…</i> popup on that element.</li></ul>', True)}
  {mini("key","Settings",'<ul><li><b>Providers</b>: Anthropic, Azure-hosted Anthropic (Microsoft Foundry), OpenAI-compatible, Azure OpenAI, DeepSeek.</li><li>Endpoint, model or deployment, API key (kept in this browser, or for the tab only), <i>Test</i>.</li><li>Settings are kept per provider; nothing is defaulted — a missing value blocks the request with a message.</li><li>The page calls the endpoint directly; a provider that blocks browser calls needs a gateway.</li></ul>', True)}
</div>
<div class="insight"><span class="tag">Privacy</span><p>Each attachment is a checkbox, so the viewer decides per request what leaves the machine. The key never enters the deck file or a saved copy.</p></div>
</div>''')

add(0, header(TM, "EDITING 11 · KEEPING, SHARING AND PRINTING YOUR CHANGES", "The deck on disk never changes by itself. Edits live in the browser until you save a copy.") + f'''
<div class="body fill"><div class="two">
  <div>
    {lst([("db","<b>Edits persist in the browser</b>, keyed by the file: reload the deck and they are still there. They exist only in that browser — the original file is untouched."),
          ("download","<b>Save edited copy</b> downloads <code class='code'>&lt;name&gt;-edited.html</code>: your edits applied to a pristine snapshot of the deck taken at load. The copy is still one self-contained file and carries the editor itself."),
          ("refresh","<b>Discard changes on this slide</b> restores the slide under the pointer (the hint counts its changes); <b>Discard edits</b> restores every slide."),
          ("refresh","<b>Refresh the tools later</b>: <code class='code'>node deck.rebuild.mjs</code> replaces only the editor block with the one the skill ships now, keeps a backup, re-runs the strict gate and re-exports the PDF. <code class='code'>--check</code> only reports CURRENT or REBUILD NEEDED."),
          ("doc","<b>Export to PDF</b> applies the same print layout as the command-line exporter and opens the print dialog: choose <i>Save as PDF</i> in Chrome or Edge. Page size, zero margins and backgrounds are preset — one page per slide, the same layout as the CLI export. Blurred shadows are printed as images on this path (block v13), so the PDF also renders correctly in macOS Preview.")])}
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

def krow(keys, what): return f'<tr><td class="kc">{kbd(*keys)}</td><td>{what}</td></tr>'
def ktable(title, rows): return f'<div class="kt"><div class="seclbl">{title}</div><table class="tbl keys"><tbody>{"".join(krow(k, w) for k, w in rows)}</tbody></table></div>'
add(0, header(TM, "KEYBOARD SHORTCUTS", "Every shortcut the editor understands, by mode. Ctrl on Windows and Linux, Cmd on a Mac; deck navigation keys are paused while you edit.") + f'''
<div class="body fill"><div class="grid4 keys4" style="gap:26px">
  {ktable("Editing text", [(("Enter",),"applies the edit; a click outside does the same"),(("Esc",),"cancels the edit and its formatting"),(("Shift+Enter",),"line break"),(("Ctrl/Cmd+Z",),"undo while editing"),(("Ctrl/Cmd+B","I","U"),"bold, italic, underline"),(("Ctrl/Cmd+Shift+>","<"),"larger / smaller text"),(("Double-click",),"a text: start editing it")])}
  {ktable("Shapes (one selected)", [(("↑↓←→",),"nudge by 1 px; <b>Shift</b> 10 px"),(("Alt+arrows",),"resize"),(("Tab","Shift+Tab"),"enclosing shape / child shape"),(("Shift+click",),"add the smallest shape there, or remove a selected one"),(("Shift+drag",),"selection box on the slide"),(("Ctrl/Cmd+click",),"everything inside the shape; a leaf alone, again cycles outward"),(("Ctrl/Cmd+A",),"every top-level shape of the slide"),(("Ctrl/Cmd+]","["),"forward / backward; <b>Shift</b> front / back"),(("Ctrl/Cmd+G","Shift+G"),"group / ungroup"),(("Esc","Enter"),"finish")])}
  {ktable("SVG parts", [(("Click",),"innermost part; drag moves it"),(("Shift+click",),"add a part, or remove a selected one"),(("Ctrl/Cmd+click",),"what is inside the part there"),(("Ctrl/Cmd+A",),"every top-level part"),(("Tab","Shift+Tab"),"enclosing group / first part inside"),(("↑↓←→",),"nudge one unit; <b>Shift</b> ten; <b>Alt</b> resizes"),(("Ctrl/Cmd+]","["),"drawing order; <b>Shift</b> front / back"),(("Ctrl/Cmd+D",),"duplicate"),(("Delete","Backspace"),"delete the part"),(("Esc",),"deselect, then end; <b>Enter</b> ends")])}
  {ktable("Menu and panels", [(("Right-click",),"the menu, or the picker while the menu is away"),(("Esc",),"closes the menu, the picker, a popup"),(("Ctrl/Cmd+Shift+O",),"Outline tab"),(("Ctrl/Cmd+Shift+H",),"Tree tab with the element's source"),(("Ctrl/Cmd+Shift+L",),"the assistant"),(("Ctrl/Cmd+V",),"paste an image into the assistant's request"),(("Double-click",),"a shape selects it; a selected drawing opens its parts; a grip releases an anchored panel")])}
</div></div>''')

# ================================================================= SECTION 03 — developers
divider("03", "Section 03", "Make it<br>your own", "How it is built: the folder, the scripts and libraries, the editor's internals, the PDF path, the configuration hook and the rules to keep.")

add(0, header(DV, "HOW IT IS BUILT, IN FIVE LAYERS", "Each layer rests on the one below; extend the one you need. The editor is the layer that turns a deck into something recipients can change themselves.") + dg(SVG["layers"]))

add(0, header(DV, "ANATOMY OF THE SKILL FOLDER", "15 MB, 14 of them photography; one Markdown file that is the whole behaviour, seven scripts, five libraries, and the design system with its assets.") + f'''
<div class="body fill"><div class="cols" style="grid-template-columns:1fr 1fr;gap:60px">
  <div class="tree">
<span class="d">nbg-design/</span><span class="cm">plugin nbg-design v1.19.0 · marketplace BikS2013-coding-agents/nbg-design · MIT</span><br>
├─ <b>SKILL.md</b><span class="sz">60 KB · 388 lines</span><span class="cm">the single source of behaviour, defaults, assets, guardrails</span><br>
├─ <span class="d">NBG-Design/</span><br>
│&nbsp;&nbsp;├─ NBG Design System.html<span class="sz">39 KB</span><span class="cm">visual reference</span><br>
│&nbsp;&nbsp;├─ slide-templates.jsx<span class="sz">32 KB</span><span class="cm">nine 1920×1080 templates</span><br>
│&nbsp;&nbsp;├─ tweaks-panel.jsx<span class="sz">24 KB</span><span class="cm">tweak / edit helper reference</span><br>
│&nbsp;&nbsp;├─ <span class="d">assets/</span><span class="sz">14 MB</span><span class="cm">3 logos + 27 photos, each with a .datauri.txt</span><br>
│&nbsp;&nbsp;└─ <span class="d">screenshots/</span><span class="cm">8 reference renders</span><br>
├─ <span class="d">scripts/</span><span class="sz">500 KB</span><span class="cm">seven scripts, five libraries</span><br>
│&nbsp;&nbsp;├─ embed-assets.mjs · add-deck-menu.mjs · verify-deck.mjs<br>
│&nbsp;&nbsp;├─ write-rebuild-script.mjs · screenshot-deck.mjs · export-pdf.mjs<br>
│&nbsp;&nbsp;├─ fix-pdf-soft-masks.mjs · README.md<span class="sz">51 KB</span><br>
│&nbsp;&nbsp;└─ <span class="d">lib/</span> find-browser.mjs · cdp.mjs · print-layout.js<br>
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;pdf-soft-masks.mjs<span class="sz">23 KB</span> · <b>deck-menu.js</b><span class="sz">326 KB</span><br>
└─ <span class="d">references/</span><span class="cm">design decisions, functions, config guide, issue register</span>
  </div>
  <div>
    {lst([("doc","<b>SKILL.md is the contract.</b> Inputs, defaults, palette, templates, embedding rules, the editor's behaviour, the PDF rules and the quality checklist — all in one file, no separate configuration."),
          ("globe","<b>Everything resolves relative to the skill root</b>, never to the working directory: the scripts find the assets next to themselves, so the skill works from any folder, on any machine, through a symlink."),
          ("link","<b>Installed as a project skill</b> via a symlink in <code class='code'>.claude/skills/</code> pointing at the plugin checkout, so the working tree is the live skill."),
          ("db","<b>References are history, not behaviour</b>: every design decision from v1.3 to v1.19 is recorded with its rationale, mechanism and verification in project-design.md.")], True)}
  </div>
</div></div>''')

rows = [("embed-assets.mjs","Replaces every <code class='code'>&#123;&#123;TOKEN&#125;&#125;</code> with the verbatim data URI; tokens map to files by name; fails loudly on a missing asset.","no","0 / 1"),
        ("add-deck-menu.mjs","Inlines one <code class='code'>&lt;script id=\"nbg-deck-menu-script\" data-nbg-deck-menu=\"13\"&gt;</code> before the last <code class='code'>&lt;/body&gt;</code>: print-layout.js then deck-menu.js. Idempotent; upgrades older blocks; <code class='code'>--remove</code> strips.","no","0 / 1"),
        ("verify-deck.mjs","The gate: tokens, image paths, image count, size, bare-logo text, editor block version. <code class='code'>--strict</code> promotes the warnings to failures.","no","0 pass / 1 fail"),
        ("write-rebuild-script.mjs","Writes <code class='code'>&lt;deck&gt;.rebuild.mjs</code> next to the deck: a self-contained script that later re-embeds the skill's current editor block (backup, verify, re-export the PDF); <code class='code'>--check</code> only reports.","no","0 / 1 / 2"),
        ("screenshot-deck.mjs","Drives a headless browser over the DevTools protocol; isolates the Nth <code class='code'>.slide</code> in place, so <code class='code'>.active</code>, <code class='code'>.hidden</code>, inline-display and stacked decks all work; PNG per slide per viewport.","yes","0 / 1 / 3 no browser"),
        ("export-pdf.mjs","Lifts the host layer, prints with <code class='code'>Page.printToPDF</code> at the slide box, verifies pages = slides and slide box = page box; then re-anchors the soft masks so shadows render in macOS Preview.","yes","0 / 1 / 3 no browser"),
        ("fix-pdf-soft-masks.mjs","Re-anchors the soft masks of a PDF exported earlier (or saved from the print dialog): an incremental update, the original bytes intact; <code class='code'>--check</code> only reports.","no","0 / 1 / 2")]
tr = "".join(f'<tr><td class="b"><span class="code">{a}</span></td><td>{b}</td><td class="c">{pill("browser","prog") if c=="yes" else pill("none","grey")}</td><td class="c">{d}</td></tr>' for a,b,c,d in rows)
add(0, header(DV, "THE SCRIPTS AND LIBRARIES", "Zero-dependency Node (18+). No npm install, no build step; seven single-file scripts that import from lib/.") + f'''
<div class="body fill">
  <table class="tbl compact" style="width:100%;border-collapse:collapse"><thead><tr><th style="width:250px">Script</th><th>What it does</th><th style="width:130px;text-align:center">Needs</th><th style="width:190px;text-align:center">Exit codes</th></tr></thead><tbody>{tr}</tbody></table>
  <div class="libs">
    {mini("search","lib/find-browser.mjs",'<p>Locates Chrome, Chromium or Edge; <code class="code">--browser</code>, <code class="code">NBG_BROWSER</code>, <code class="code">CHROME_BIN</code> override.</p>')}
    {mini("link","lib/cdp.mjs",'<p>A minimal DevTools-protocol client over the debugging pipe: launch, navigate, evaluate, print, count pages.</p>')}
    {mini("doc","lib/print-layout.js",'<p>The print shim shared by the exporter and the in-deck menu; a registry undoes every change after printing. On the menu path it prints blurred shadows as images (v13).</p>')}
    {mini("layers","lib/pdf-soft-masks.mjs",'<p>Zero-dependency PDF rewriter: re-anchors Chrome\'s luminosity soft masks so macOS Preview renders shadows; incremental update.</p>')}
    {mini("wrench","lib/deck-menu.js",'<p>The editor: ~4,000 lines of plain browser JavaScript — editing, selection, SVG parts, toolbars, structure, assistant, persistence, print.</p>')}
  </div>
</div>''')

add(0, header(DV, "INSIDE A DELIVERED DECK", "One HTML file carries the slides and the editor; the browser keeps the edits; three ways lead out.") + dg(SVG["arch"]))

add(0, header(DV, "INSIDE THE EDITOR", "How a standalone file:// deck can be edited, remembered and handed back without ever writing to itself.") + f'''
<div class="body fill"><div class="grid3" style="gap:28px">
  {mini("db","Edit records",'<ul><li>Every change is a record <code class="code">{{ path, original, … }}</code> where <b>path</b> is the child-index path from the root — cheap, exact, and the reason the DOM is never restructured.</li><li>Three kinds: <b>html</b> (text and selection-level formatting), <b>style</b> (block formatting, geometry, fill, border, z-index), <b>group</b> (the <code class="code">data-nbg-group</code> attribute). An SVG session records the whole <code class="code">&lt;svg&gt;</code> as one html record.</li><li>Stored in <code class="code">localStorage</code> under <code class="code">nbg-deck-edits:&lt;path&gt;#&lt;title&gt;</code>; re-applied on load; a record whose original no longer matches is dropped.</li></ul>', True)}
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
          ("shield","<b>Verifies</b>: page count equals slide count and every slide box equals the page box; otherwise exit 1 (the PDF is still written for diagnosis). Exit 3 means no browser on the host."),
          ("refresh","<b>Re-anchors the soft masks</b> (since 1.19): Chrome writes every blurred shadow as a luminosity mask that macOS Preview mis-positions into gray blocks. The exporter rewrites them to page space as an incremental update; every other viewer draws the same picture. <code class='code'>fix-pdf-soft-masks.mjs</code> does it for older PDFs.")], True)}
  </div>
  <div>
    <div class="seclbl">Rules that are not negotiable</div>
    {lst([("alert","<b>Aesthetics are frozen.</b> No print stylesheets, no resized slides, no font swaps \"to make it print\". A mismatch is a bug in the deck, fixed in the HTML."),
          ("alert","<b>No fakes.</b> No <code class='code'>window.print()</code> at A4, no browser Save-as-PDF with headers and margins, no office round-trips, no stitched screenshots."),
          ("doc","Every top-level slide carries the <code class='code'>slide</code> class — the exporter and the screenshot helper key on it."),
          ("globe","<b>Fonts come from the exporting host</b>: with Aptos absent, PDF and screenshots share the same fallback. Export where Aptos is installed if it must appear."),
          ("check","Never print a deck that fails <code class='code'>verify-deck --strict</code>. The in-deck <i>Export to PDF</i> inlines the very same shim; since the print dialog's PDF cannot be post-processed, that path prints blurred shadows as images instead (block v13).")], True)}
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
    {lst([("code","A deck can be a <b>data-driven Python generator</b>: a helper section (icons, header, footer, pills, numbered circles) and one <code class='code'>add()</code> per slide, sharing one <code class='code'>deck.css</code> and <code class='code'>deck.js</code> with sibling decks."),
          ("link","Slides can be <b>sliced out of another generator</b> by comment markers and re-executed, so a slide reused across decks is one line."),
          ("refresh","A <code class='code'>rebuild.sh</code> per deck detects skill, generator or asset changes, builds the next version through the five steps and refreshes a fixed-name <code class='code'>-latest</code> copy — the stable link."),
          ("star","This deck was built that way: a 550-line generator, the shared CSS plus 150 lines of additions, and the pipeline.")], True)}
  </div>
</div></div>''')

add(0, header(DV, "RULES THAT KEEP IT SAFE", "The constraints written into SKILL.md that every generated deck, and every future change to the skill, must respect.") + f'''
<div class="body fill"><div class="grid3" style="gap:28px">
  {mini("shield","Delivery",'<ul><li>Run order: author → embed → add menu → verify strict → rebuild script → screenshots → PDF. Never deliver a deck that fails the gate.</li><li>Every image a <code class="code">data:</code> URI; the logo always the bundled lockup.</li><li>Fit at 1366×768 and 1440×900; no element collisions; 32 px between groups, 72 px above the footer.</li><li>PDF only from the verified HTML, only through the exporter.</li></ul>', True)}
  {mini("key","Secrets & fallbacks",'<ul><li>The skill holds <b>no credentials</b>. Assistant keys are the viewer\'s and live only in their browser — never in the skill, a deck or a saved copy.</li><li><b>No fallback values</b>: a missing input is a question, a missing setting a message. Exceptions are written into the project memory first.</li><li>The agent never enters endpoints or keys for a recipient and never relies on the assistant for its own work.</li></ul>', True)}
  {mini("layers","Scope",'<ul><li><b>The look cannot be left</b> from the editor: fonts limited to the design-system stacks, colours to the NBG-inspired palette. The Tree tab\'s source editor is the one deliberate exception, for experts.</li><li>The editor changes text, formatting, geometry, order, groups and shape style. Images, new elements and structure are the skill\'s job — regenerate.</li><li><b>PowerPoint is out of scope</b>; newsletters, GPT and NotebookLM artifacts of the original project are excluded unless asked for.</li></ul>', True)}
</div></div>''')

# ================================================================= closing
add(0, header("Summary", "USING IT TOMORROW", "One line for recipients, six commands for builders, one marketplace to install from.") + f'''
<div class="body fill"><div class="two">
  <div>
    <div class="seclbl">Tell the recipient</div>
    <div class="band" style="margin-top:18px;text-align:left"><p class="band-t" style="text-align:left;font-size:22px;line-height:1.5">Double-click any text to edit it (Enter applies, Esc cancels). Right-click for <b>Resize / move shape</b> (Shift+click or Shift+drag selects several; the toolbar orders, aligns, distributes and groups them), <b>Edit SVG</b> (the parts of a drawn icon, diagram or chart; one toolbar with Text, Shape and SVG tabs serves all three), <b>Ask the assistant</b>, <b>Export to PDF</b> and <b>Save edited copy</b>. After a skill update, <code class="code">node deck.rebuild.mjs</code> refreshes the editing tools and the PDF.</p></div>
    <div class="seclbl" style="margin-top:36px">Where it lives</div>
    {lst([("link","Public marketplace <code class='code'>github.com/BikS2013-coding-agents/nbg-design</code>: <code class='code'>/plugin marketplace add BikS2013-coding-agents/nbg-design</code>, then <code class='code'>/plugin install nbg-design@nbg-design</code>."),
          ("doc","This deck: <code class='code'>github.com/BikS2013-presentations/deck-work-nbgdesign</code>, browsable on GitHub Pages and always current as <code class='code'>deck/NBG-Design-Skill-Explained-latest.html</code>; its generator and <code class='code'>rebuild.sh</code> live in the same repository.")], True)}
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
    {lst([("steps","Ask for your next deck in this look and hand the three files to its readers."),
          ("users","Hand a deck to two colleagues, watch them edit it, and feed the friction back into the next release."),
          ("star","Commit and push the v1.19 working tree of the plugin.")], True)}
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
