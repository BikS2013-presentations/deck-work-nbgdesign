#!/usr/bin/env node
// NBG-Design-Skill-Explained-latest.rebuild.mjs — rebuild "NBG-Design-Skill-Explained-latest.html" with the current NBG Design editing tools.
//
// Written by the nbg-design skill (scripts/write-rebuild-script.mjs) on 2026-09-06,
// when the deck was delivered with editor block v13 (plugin 1.19.0).
// The deck carries the in-deck editing tools (right-click menu, text and shape toolbars, structure
// panel, AI assistant, "Export to PDF", "Save edited copy") as one inlined script block. Those tools
// evolve with the skill; the deck does not. Run this script after the nbg-design skill / plugin was
// updated: it replaces the deck's editor block with the version the skill ships now — the slides
// themselves are left exactly as they are — then verifies the deck and exports its PDF again.
//
//   node NBG-Design-Skill-Explained-latest.rebuild.mjs                 # rebuild the deck next to this script and its PDF
//   node NBG-Design-Skill-Explained-latest.rebuild.mjs --check         # only report whether the deck's editor is current (writes nothing)
//   node NBG-Design-Skill-Explained-latest.rebuild.mjs --no-pdf        # rebuild the HTML only
//   node NBG-Design-Skill-Explained-latest.rebuild.mjs --pdf out.pdf   # rebuild and export the PDF to this path
//   node NBG-Design-Skill-Explained-latest.rebuild.mjs other.html      # rebuild another copy of the deck (e.g. the "-edited" copy)
//   node NBG-Design-Skill-Explained-latest.rebuild.mjs --no-backup     # do not keep a copy of the deck as it was before
//
// Where the nbg-design scripts are looked up (highest priority first):
//   --scripts <dir>             explicit;
//   NBG_DESIGN_SCRIPTS=<dir>    environment;
//   the recorded directory      /Users/giorgosmarinos/ai-coding/nbg-design-skill-dev/aihub-skills/plugins/nbg-design/skills/nbg-design/scripts
//                               (where the skill was when the deck was delivered).
// The directory must hold add-deck-menu.mjs, verify-deck.mjs, export-pdf.mjs and lib/ (the skill's
// scripts/ folder). Anything else is an error: the script never substitutes another location.
//
// Exit: 0 = rebuilt (or --check: current), 1 = error / gate failed (or --check: not current),
//       2 = usage, 3 = HTML rebuilt but no Chrome/Chromium/Edge on this host for the PDF.

import { readFileSync, writeFileSync, copyFileSync, existsSync } from 'node:fs';
import { resolve, dirname, basename } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawnSync } from 'node:child_process';

const RECORD = {
  "generated": "2026-09-06T10:27:38.035Z",
  "deck": "NBG-Design-Skill-Explained-latest.html",
  "pdf": "NBG-Design-Skill-Explained-latest.pdf",
  "scriptsDir": "/Users/giorgosmarinos/ai-coding/nbg-design-skill-dev/aihub-skills/plugins/nbg-design/skills/nbg-design/scripts",
  "blockVersion": 13,
  "shippedVersion": 13,
  "pluginVersion": "1.19.0",
  "config": null,
  "exportArgs": []
};

const HERE = dirname(fileURLToPath(import.meta.url));
const USAGE = `Rebuild "${RECORD.deck}" with the current NBG Design editing tools
Usage: node ${basename(fileURLToPath(import.meta.url))} [<deck.html>] [--scripts <dir>] [--pdf <file> | --no-pdf]
                              [--no-backup] [--check]

  <deck.html>       Another copy of the deck to rebuild (default: ${RECORD.deck} next to this script).
  --scripts <dir>   The nbg-design skill's scripts/ directory (default: NBG_DESIGN_SCRIPTS, else the
                    recorded ${RECORD.scriptsDir}).
  --pdf <file>      Export the PDF to this path (default: ${RECORD.pdf || 'none — the deck was delivered without a PDF'}).
  --no-pdf          Skip the PDF export.
  --no-backup       Do not copy the deck to <name>.backup-<stamp>.html before rebuilding.
  --check           Report the deck's editor version against the skill's and exit 0 when current,
                    1 otherwise. Writes nothing.

Exit: 0 = rebuilt / current, 1 = error / gate failed / not current, 2 = usage, 3 = no browser for the PDF.`;

function parseArgs(argv) {
  const a = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const x = argv[i];
    const val = () => { if (i + 1 >= argv.length) throw new Error(`${x} needs a value`); return argv[++i]; };
    if (x === '--scripts') a.scripts = val();
    else if (x === '--pdf') a.pdf = val();
    else if (x === '--no-pdf') a.noPdf = true;
    else if (x === '--no-backup') a.noBackup = true;
    else if (x === '--check') a.check = true;
    else if (x === '-h' || x === '--help') a.help = true;
    else if (x.startsWith('-')) throw new Error(`unknown option ${x}`);
    else a._.push(x);
  }
  if (a._.length > 1) throw new Error('at most one deck file');
  return a;
}

/** Resolve and validate the nbg-design scripts directory — explicit flag, environment, recorded path; nothing else. */
function resolveScriptsDir(explicit) {
  const source = explicit ? '--scripts' : process.env.NBG_DESIGN_SCRIPTS ? 'NBG_DESIGN_SCRIPTS' : 'the recorded directory';
  const dir = resolve(process.cwd(), explicit || process.env.NBG_DESIGN_SCRIPTS || RECORD.scriptsDir);
  const need = ['add-deck-menu.mjs', 'verify-deck.mjs', 'export-pdf.mjs', 'lib/deck-menu.js', 'lib/print-layout.js'];
  for (const f of need) {
    if (!existsSync(resolve(dir, f))) {
      throw new Error(`nbg-design scripts directory (${source}) is missing ${f}: ${dir}\n` +
        '  Point --scripts (or NBG_DESIGN_SCRIPTS) at the nbg-design skill\'s scripts/ directory — the one that holds add-deck-menu.mjs, verify-deck.mjs and export-pdf.mjs.');
    }
  }
  const version = Number((readFileSync(resolve(dir, 'lib/deck-menu.js'), 'utf8').match(/var VERSION = (\d+);/) || [])[1]);
  if (!version) throw new Error(`lib/deck-menu.js in ${dir} has no VERSION marker`);
  return { dir, source, version };
}

/** The editor block version a deck carries (null when it has none). */
function deckBlockVersion(html) {
  const m = html.match(/<script id="nbg-(?:pdf|deck)-menu(?:-script)?" data-nbg-(?:pdf|deck)-menu="(\d+)">/);
  return m ? Number(m[1]) : null;
}

function run(label, dir, script, args) {
  console.log(`\n▶ ${label}: node ${script} ${args.map((s) => (/\s/.test(s) ? JSON.stringify(s) : s)).join(' ')}`);
  const r = spawnSync(process.execPath, [resolve(dir, script), ...args], { stdio: 'inherit' });
  if (r.error) throw new Error(`${script} could not start: ${r.error.message}`);
  return r.status === null ? 1 : r.status;
}

function stamp() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`;
}

async function main() {
  let args;
  try { args = parseArgs(process.argv.slice(2)); }
  catch (e) { console.error('rebuild ERROR: ' + e.message + '\n'); console.log(USAGE); process.exit(2); }
  if (args.help) { console.log(USAGE); process.exit(0); }
  if (args.pdf && args.noPdf) { console.error('rebuild ERROR: --pdf and --no-pdf exclude each other'); process.exit(2); }

  try {
    const deck = args._[0] ? resolve(process.cwd(), args._[0]) : resolve(HERE, RECORD.deck);
    if (!existsSync(deck)) throw new Error('deck not found: ' + deck);
    const { dir, source, version: shipped } = resolveScriptsDir(args.scripts);
    const html = readFileSync(deck, 'utf8');
    const embedded = deckBlockVersion(html);

    console.log(`NBG deck rebuild — ${deck}`);
    console.log(`  editor block in the deck: ${embedded === null ? 'none' : 'v' + embedded} | the skill ships: v${shipped} (${source}: ${dir})`);
    console.log(`  delivered with: block v${RECORD.blockVersion}${RECORD.pluginVersion ? ', plugin ' + RECORD.pluginVersion : ''} on ${RECORD.generated.slice(0, 10)}`);

    if (args.check) {
      const current = embedded !== null && embedded >= shipped && html.includes('id="nbg-deck-menu-script"');
      console.log(current ? `\nRESULT: CURRENT — the deck carries editor block v${embedded}; nothing to rebuild.` : `\nRESULT: REBUILD NEEDED — ${embedded === null ? 'the deck has no editor block' : 'the deck carries v' + embedded + ', the skill ships v' + shipped}. Run this script without --check.`);
      process.exit(current ? 0 : 1);
    }

    // 1 — keep the deck as it was
    if (!args.noBackup) {
      const backup = resolve(dirname(deck), basename(deck).replace(/\.html?$/i, '') + '.backup-' + stamp() + '.html');
      copyFileSync(deck, backup);
      console.log(`\n▶ backup: ${backup}`);
    }

    // 2 — the editor block: the skill's current one, with the configuration the deck was delivered with
    const { addMenu } = await import(pathToFileURL(resolve(dir, 'add-deck-menu.mjs')).href);
    const r = addMenu(html, RECORD.config || undefined);
    writeFileSync(deck, r.html, 'utf8');
    console.log(`\n▶ editor block: v${r.version} ${r.status}`);

    // 3 — the strict gate
    if (run('verify', dir, 'verify-deck.mjs', [deck, '--strict']) !== 0) {
      console.log('\nRESULT: FAIL — the deck does not pass verify-deck.mjs --strict after the rebuild; the PDF was not exported.');
      process.exit(1);
    }

    // 4 — the PDF
    const pdf = args.noPdf ? null : args.pdf ? resolve(process.cwd(), args.pdf) : args._[0] ? resolve(dirname(deck), basename(deck).replace(/\.html?$/i, '') + '.pdf') : RECORD.pdf ? resolve(HERE, RECORD.pdf) : null;
    if (pdf) {
      const code = run('export PDF', dir, 'export-pdf.mjs', [deck, '-o', pdf, ...RECORD.exportArgs]);
      if (code === 3) {
        console.log(`\nRESULT: HTML REBUILT (editor block v${r.version} ${r.status}) — no browser on this host, the PDF was not exported. Run this script where Chrome/Chromium/Edge exists to refresh ${pdf}.`);
        process.exit(3);
      }
      if (code !== 0) { console.log('\nRESULT: FAIL — the PDF export did not pass; the HTML was rebuilt.'); process.exit(1); }
      console.log(`\nRESULT: PASS — ${basename(deck)} carries editor block v${r.version} (${r.status}), verified, PDF exported to ${pdf}.`);
    } else {
      console.log(`\nRESULT: PASS — ${basename(deck)} carries editor block v${r.version} (${r.status}), verified. No PDF export was requested.`);
    }
    process.exit(0);
  } catch (e) {
    console.error('rebuild ERROR: ' + e.message);
    process.exit(1);
  }
}

main();
