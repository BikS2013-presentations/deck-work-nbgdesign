#!/usr/bin/env bash
# Rebuild "The nbg-design skill — explained" with the nbg-design pipeline.
#
#   ./rebuild.sh            rebuild only if the skill, the generator or the assets changed since the last build
#   ./rebuild.sh --force    rebuild even if nothing changed
#   ./rebuild.sh --check    only report what changed, build nothing
#
# Output (next to this script, in deck/): only the newest version is kept —
#   NBG-Design-Skill-Explained-latest.html / .pdf / .rebuild.mjs   the stable names to link to
#   VERSION                                                         the build number (v<N>); older builds live in git history
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
OUTDIR="$HERE/deck"
NAME="NBG-Design-Skill-Explained"
SKILL="$(readlink "$HOME/officework/.claude/skills/nbg-design")"
BASE="$HERE/base"                                    # the shared helper section, deck.css and deck.js (in this repo)
MODE="${1:-}"
OUT="$OUTDIR/$NAME-latest.html"
VERSION_FILE="$OUTDIR/VERSION"

last="$(cat "$VERSION_FILE" 2>/dev/null || echo 0)"
next=$((last + 1))
changed=0
if [ "$last" -gt 0 ] && [ -f "$OUT" ]; then
  newer="$(find "$SKILL" -type f -newer "$OUT" \( -name '*.js' -o -name '*.mjs' -o -name '*.css' -o -name '*.txt' -o -name 'SKILL.md' \) | sed "s|$SKILL/||")"
  if [ -n "$newer" ]; then changed=1; echo "Skill files changed since v$last:"; echo "$newer" | sed 's/^/  /'; else echo "Skill unchanged since v$last."; fi
  gen="$(find "$HERE/build.py" "$HERE/diagrams.py" "$HERE/extra.css" "$HERE/assets" "$BASE" -type f -newer "$OUT" 2>/dev/null | sed "s|$HERE/||")"
  if [ -n "$gen" ]; then changed=1; echo "Generator / asset files changed since v$last:"; echo "$gen" | sed 's/^/  /'; else echo "Generator and assets unchanged since v$last."; fi
else
  changed=1
fi
if [ "$MODE" = "--check" ]; then
  [ "$changed" = 1 ] && echo "RESULT: REBUILD NEEDED (next: v$next)" || echo "RESULT: CURRENT (v$last)"; exit 0
fi
if [ "$changed" = 0 ] && [ "$MODE" != "--force" ]; then echo "RESULT: CURRENT (v$last) — nothing to rebuild; --force overrides."; exit 0
fi

echo; echo "Building v$next …"
( cd "$HERE" && python3 build.py )
node "$SKILL/scripts/embed-assets.mjs" "$HERE/deck.html" -o "$OUT" | tail -1
node "$SKILL/scripts/add-deck-menu.mjs" "$OUT"
node "$SKILL/scripts/verify-deck.mjs" "$OUT" --strict | grep RESULT
node "$SKILL/scripts/write-rebuild-script.mjs" "$OUT" >/dev/null
rm -rf "$HERE"/shots-v*
node "$SKILL/scripts/screenshot-deck.mjs" "$OUT" -o "$HERE/shots-v$next" | grep Wrote || true
node "$SKILL/scripts/export-pdf.mjs" "$OUT" >/dev/null
pages="$(python3 -c "import re,sys;print(len(re.findall(rb'/Type\s*/Page[^s]',open(sys.argv[1],'rb').read())))" "$OUTDIR/$NAME-latest.pdf")"
echo "PDF: $pages pages"
echo "$next" > "$VERSION_FILE"
echo "RESULT: BUILT v$next → $OUT / .pdf / .rebuild.mjs"
