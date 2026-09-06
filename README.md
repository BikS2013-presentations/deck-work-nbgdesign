# The nbg-design skill — explained

A 38-slide HTML presentation that explains the **nbg-design** Claude Code skill — a presentations
skill inspired by the NBG brand: what it makes possible, how to ask for, build and edit a deck, and how to make it your own. The deck
itself was produced with the skill, so it is also a specimen of what the skill delivers.

> ### ▶ [Open the presentation online](https://biks2013-presentations.github.io/deck-work-nbgdesign/)
> **https://biks2013-presentations.github.io/deck-work-nbgdesign/** — the landing page on GitHub Pages, always the newest version.
> Straight to the deck: [NBG-Design-Skill-Explained-latest.html](https://biks2013-presentations.github.io/deck-work-nbgdesign/deck/NBG-Design-Skill-Explained-latest.html) ·
> [PDF](https://biks2013-presentations.github.io/deck-work-nbgdesign/deck/NBG-Design-Skill-Explained-latest.pdf) ·
> [diagrams](https://biks2013-presentations.github.io/deck-work-nbgdesign/#diagrams)

## The deck

| File | What it is |
|---|---|
| `deck/NBG-Design-Skill-Explained-latest.html` | **The stable link.** Always a copy of the newest version: one self-contained file, every image embedded, with the in-deck right-click editor. Open it in any modern browser. |
| `deck/NBG-Design-Skill-Explained-latest.pdf` | The same deck printed by the browser engine, one page per slide. |
| `deck/NBG-Design-Skill-Explained-latest.rebuild.mjs` | The deck's rebuild script: `node …rebuild.mjs` re-embeds the skill's current editing tools into the deck (backup, strict verify, PDF re-export) after the skill is updated; `--check` only reports. |
| `deck/VERSION` | The build number of the `-latest` files (`v<N>`). Only the newest build is kept in the tree; earlier ones are in the git history. |
| `deck/diagrams/nbg-design-*.html` | The five explanatory diagrams as standalone pages (layer stack, sequence, flowchart, tree, architecture). |

Viewing the HTML: double-click any text to edit it (Enter applies, Esc cancels); right-click for
*Resize / move shape*, *Edit SVG* (the parts of a drawn diagram), *Ask the assistant*, *Export to PDF*
and *Save edited copy*.

Reference the deck from elsewhere through the fixed name, so the link never goes stale:
`https://github.com/BikS2013-presentations/deck-work-nbgdesign/blob/main/deck/NBG-Design-Skill-Explained-latest.html`
(raw file: `https://raw.githubusercontent.com/BikS2013-presentations/deck-work-nbgdesign/main/deck/NBG-Design-Skill-Explained-latest.html`;
GitHub serves raw HTML as plain text, so to open it rendered use a viewer such as `https://raw.githack.com/BikS2013-presentations/deck-work-nbgdesign/main/deck/NBG-Design-Skill-Explained-latest.html`, or download it).

## Installing the skill

The skill is distributed through the public marketplace
[BikS2013-coding-agents/nbg-design](https://github.com/BikS2013-coding-agents/nbg-design):

```
/plugin marketplace add BikS2013-coding-agents/nbg-design
/plugin install nbg-design@nbg-design
```

Restart Claude Code; `/plugin list` shows it. Later: `/plugin marketplace update nbg-design` and
`claude plugin update nbg-design@nbg-design`.

## Rebuilding this deck

```
./rebuild.sh            # rebuild only if the skill, the generator or the assets changed since the last version
./rebuild.sh --force    # rebuild anyway
./rebuild.sh --check    # only report
```

`rebuild.sh` runs the pipeline below straight into the `-latest` names, writes their rebuild script and
bumps `deck/VERSION`.

## How it is built

- `build.py` — the data-driven generator: one `add()` call per slide, plus the cover, agenda and
  dark dividers. It writes `deck.html` with `{{TOKEN}}` image placeholders.
- `diagrams.py` — draws the five diagrams as inline SVG (drawn with the diagram-design skill's
  grammar on the NBG-inspired skin: white paper, dark-teal ink, one aqua accent, all-Aptos, 4 px
  grid, orthogonal connectors, masked labels, legend strip). It also writes the standalone pages.
- `base/` — the shared helper section, stylesheet and script the generator builds on (copied in, see below).
- `extra.css` — the deck's own additions to the shared deck stylesheet.
- `assets/assistant-*.png` — three real screenshots of the in-deck assistant (Settings, Ask, the Ask-about
  popup over the Outline), embedded on the "The assistant, as it looks" slide. Regenerate them with
  `node test_scripts/capture-assistant.mjs deck/<deck>.html 7` (headless Chrome through the skill's CDP helper).

The repository is self-contained: `base/helpers.py` (the shared helper section — icons, header, footer, `add()`),
`base/deck.css` and `base/deck.js` carry the briefing look the generator builds on. `HERE` in `build.py` is the
only absolute path to adjust on another machine; the nbg-design skill must be linked at `~/officework/.claude/skills/nbg-design`.

The pipeline, in order, with the nbg-design skill's scripts:

```
python3 build.py
node <skill>/scripts/embed-assets.mjs  deck.html -o deck/<name>.html   # tokens → data URIs
node <skill>/scripts/add-deck-menu.mjs deck/<name>.html                 # inline the editor
node <skill>/scripts/verify-deck.mjs   deck/<name>.html --strict        # the gate
node <skill>/scripts/write-rebuild-script.mjs deck/<name>.html          # <name>.rebuild.mjs, delivered too
node <skill>/scripts/screenshot-deck.mjs deck/<name>.html -o shots      # look
node <skill>/scripts/export-pdf.mjs    deck/<name>.html                 # one page per slide
```

## Notes

- The look is *inspired by* the NBG brand; this is not an official National Bank of Greece
  publication.
- Screenshots, rasterised PDF pages and the intermediate `deck.html` are not committed.
