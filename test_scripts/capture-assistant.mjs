// Captures three screenshots of the in-deck assistant from a delivered deck, in headless Chrome:
//   assets/assistant-settings.png  — the assistant's Settings view
//   assets/assistant-ask.png       — the assistant's Ask view with a selection and a request
//   assets/assistant-popup.png     — the "Ask about…" popup over the structure panel (Outline tab)
// Usage: node test_scripts/capture-assistant.mjs deck/<deck>.html [slide-number]
import { writeFileSync, mkdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
const SK = resolve(process.env.HOME, 'officework/.claude/skills/nbg-design/scripts/lib');
const { launchBrowser, openPage, navigate, evaluate } = await import(pathToFileURL(resolve(SK, 'cdp.mjs')).href);
const { findBrowser } = await import(pathToFileURL(resolve(SK, 'find-browser.mjs')).href);
const HERE = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const deck = resolve(process.argv[2] || 'deck/NBG-Design-Skill-Explained-v12.html');
const slideNo = parseInt(process.argv[3] || '7', 10);
const OUT = resolve(HERE, 'assets'); mkdirSync(OUT, { recursive: true });
const browser = findBrowser(); if (!browser) { console.error('no browser'); process.exit(3); }
const { cdp, close } = launchBrowser(browser, { width: 1920, height: 1080 });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
try {
  const { sessionId } = await openPage(cdp, { width: 1920, height: 1080 });
  await navigate(cdp, sessionId, pathToFileURL(deck).href + '#' + slideNo, 30000);
  await sleep(600);
  const ev = (expr) => evaluate(cdp, sessionId, expr);
  await ev(`window.showSlide && window.showSlide(${slideNo}); true`);
  await sleep(300);
  const shot = async (name, rectExpr, pad = 12) => {
    const r = await ev(rectExpr);
    const clip = { x: Math.max(0, r.x - pad), y: Math.max(0, r.y - pad), width: r.width + 2 * pad, height: r.height + 2 * pad, scale: 2 };
    const { data } = await cdp.send('Page.captureScreenshot', { format: 'png', clip, captureBeyondViewport: false }, sessionId);
    writeFileSync(resolve(OUT, name), Buffer.from(data, 'base64'));
    console.log(name, Math.round(clip.width), 'x', Math.round(clip.height));
  };
  const rectOf = (sel) => `(function(){var e=document.querySelector('${sel}');var b=e.getBoundingClientRect();return {x:b.left,y:b.top,width:b.width,height:b.height};})()`;
  // common set-up: a selection on the slide, realistic settings (a throwaway profile — nothing persists)
  await ev(`(function(){
    var s = document.querySelectorAll('.slide')[${slideNo - 1}];
    var el = s.querySelector('.mini') || s.querySelector('.card, h4, p');
    window.__el = el;
    nbgDeck.ai.settings({ provider: 'anthropic', url: 'https://api.anthropic.com', model: 'claude-opus-5', keyScope: 'browser', key: 'sk-ant-api03-demo-demo-demo-demo-demo-demo-demo-demo-demo-demo', include: { shot: true, slide: true, sel: true, clip: false }, output: 'answer' });
    return !!el; })()`);
  // 1. Settings view
  await ev(`nbgDeck.menu.open(1180, 200); nbgDeck.ai.open('settings'); document.getElementById('nbg-deck-menu').style.height = '520px'; true`);
  await sleep(400);
  await shot('assistant-settings.png', rectOf('#nbg-deck-menu'));
  // 2. Ask view with a selected element, a prompt and a request
  await ev(`nbgDeck.shape.select(window.__el); nbgDeck.toolbars.set('shape','off'); nbgDeck.toolbars.set('text','off'); nbgDeck.ai.open('ask'); nbgDeck.ai.prompts.select('b:copy'); nbgDeck.ai.request('Keep every number as it is; make each bullet one line and use the same verb form throughout.'); document.getElementById('nbg-deck-menu').style.height = '440px'; true`);
  await sleep(400);
  await shot('assistant-ask.png', rectOf('#nbg-deck-menu'));
  // 3. The Ask-about popup over the structure panel (Outline tab)
  await ev(`nbgDeck.ai.close && nbgDeck.ai.close(); nbgDeck.code.open(window.__el, 'outline'); document.getElementById('nbg-deck-menu').style.height = '600px'; true`);
  await sleep(400);
  await ev(`(function(){ var row = nbgDeck.code.outlineRowOf(window.__el); var b = row ? row.getBoundingClientRect() : document.querySelector('#nbg-deck-menu').getBoundingClientRect(); nbgDeck.ai.popup.open(b.left + 120, b.bottom + 8, window.__el); return true; })()`);
  await sleep(400);
  await shot('assistant-popup.png', `(function(){var a=document.querySelector('#nbg-deck-menu').getBoundingClientRect(),p=document.querySelector('#nbg-ai-pop').getBoundingClientRect();var x=Math.min(a.left,p.left),y=Math.min(a.top,p.top);return {x:x,y:y,width:Math.max(a.right,p.right)-x,height:Math.max(a.bottom,p.bottom)-y};})()`);
} finally { close(); }
