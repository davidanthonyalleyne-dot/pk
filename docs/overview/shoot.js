// Takes the overview screenshots from a local copy of PK.
// Usage: PK_CODE=XXXX-XXXX-XXXX-XXXX node docs/overview/shoot.js
// The access code is read from the environment and never written anywhere.
// Optional: THREE_PATH=/path/to/three.min.js (r128) if cdnjs can't be reached.
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..', '..'), OUT = path.join(__dirname, 'shots'), FONTS = path.join(__dirname, 'fonts');
const CODE = process.env.PK_CODE;
if (!CODE) { console.error('Set PK_CODE to the access code.'); process.exit(1); }
const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.webmanifest': 'application/manifest+json', '.bin': 'application/octet-stream', '.woff2': 'font/woff2' };

const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
  const f = path.join(ROOT, p);
  if (!f.startsWith(ROOT) || !fs.existsSync(f)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream' }); fs.createReadStream(f).pipe(res);
});

const fontCSS = [['Bungee', 400, 'bungee-latin-400-normal'], ['Barlow', 400, 'barlow-latin-400-normal'], ['Barlow', 600, 'barlow-latin-600-normal'],
  ['Barlow Condensed', 600, 'barlow-condensed-latin-600-normal'], ['Barlow Condensed', 700, 'barlow-condensed-latin-700-normal']]
  .map(([f, w, n]) => `@font-face{font-family:'${f}';font-weight:${w};font-style:normal;src:url(http://localhost:8799/docs/overview/fonts/${n}.woff2) format('woff2')}`).join('\n');

const wait = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  await new Promise(r => server.listen(8799, r));
  const browser = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  await ctx.route(/fonts\.googleapis\.com/, r => r.fulfill({ body: fontCSS, contentType: 'text/css' }));
  if (process.env.THREE_PATH) await ctx.route(/cdnjs\.cloudflare\.com.*three\.min\.js/, r => r.fulfill({ body: fs.readFileSync(process.env.THREE_PATH), contentType: 'text/javascript' }));
  // the diagnostics reporter stays quiet while shooting
  await ctx.route(/firestore\.googleapis\.com|identitytoolkit/, r => r.abort());
  const page = await ctx.newPage();
  const shot = async name => { await page.screenshot({ path: path.join(OUT, name + '.png') }); console.log('shot', name); };
  const tapSel = async sel => { await page.locator(sel).first().click({ force: true }); await wait(700); };
  const hideTalk = async () => { await page.evaluate(() => { const t = document.getElementById('talk'); if (t && !t.hidden) t.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true })); }); await wait(400); };
  const pick = async (group, val) => { await tapSel('#pause'); await tapSel(`#${group} button[data-${group === 'wxset' ? 'w' : 't'}="${val}"]`); await tapSel('#resume'); };

  await page.goto('http://localhost:8799/#join=' + CODE, { waitUntil: 'load' });
  await page.waitForFunction(() => { const s = document.getElementById('start'); return s && !s.disabled; }, null, { timeout: 180000 });
  await wait(1500); await shot('01-title');

  await tapSel('#start'); await wait(9000); await hideTalk(); await wait(1500); await shot('02-play');

  await pick('wxset', 'snow'); await wait(25000); await hideTalk(); await shot('03-snow');

  await tapSel('#tod'); await pick('wxset', 'rain'); await wait(40000); await hideTalk(); await shot('04-rain-night');

  await tapSel('#pause'); await page.evaluate(() => { const r = document.getElementById('wxset'); r && r.scrollIntoView({ block: 'center' }); }); await wait(800); await shot('05-settings');
  await tapSel('#wxset button[data-w="live"]'); await tapSel('#resume');

  await tapSel('#tod'); await tapSel('#tod'); await wait(1500);
  await tapSel('#mapwrap'); await wait(2500); await shot('06-map');

  await browser.close(); server.close();
})().catch(e => { console.error(e); process.exit(1); });
