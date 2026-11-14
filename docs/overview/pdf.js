// Prints overview.html to overview.pdf (US Letter). Usage: node docs/overview/pdf.js
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.join(__dirname, 'overview.html'), { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready); await p.emulateMedia({ media: 'print' });
  await p.pdf({ path: path.join(__dirname, 'overview.pdf'), format: 'Letter', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
  await b.close(); console.log('wrote overview.pdf');
})();
