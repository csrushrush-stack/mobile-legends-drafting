/* Verifies the blind window in a real browser: which enemy ban slots are locked
   at each point of the ranked ban phase. */
const { chromium } = require('C:/Users/Acer/.workbuddy-ai/binaries/node/workspace/node_modules/playwright');
const path = require('path');
const FILE = 'file:///' + path.join(__dirname, 'draft_app.html').replace(/\\/g, '/');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 980 } });
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });

  await page.goto(FILE);
  await page.waitForTimeout(300);
  await page.click('#dRk');
  await page.waitForTimeout(150);
  await page.click('#pickBlue');
  await page.waitForTimeout(150);

  const snap = label => page.evaluate(l => {
    const grab = id => Array.from(document.querySelectorAll('#' + id + ' .slot'))
      .map(s => (s.textContent || '').trim().replace(/\s+/g, ' '));
    return { label: l, cursorStep: document.querySelector('.seqdot.now') ?
        Array.from(document.querySelectorAll('.seqdot')).indexOf(document.querySelector('.seqdot.now')) + 1 : null,
      turn: (document.getElementById('turnLabel') || {}).textContent.replace(/\s+/g, ' ').trim(),
      blueBans: grab('blueBans'), redBans: grab('redBans') };
  }, label);

  const rows = [];
  rows.push(await snap('start (blue ban 1)'));

  /* blue bans its 3 */
  for (let i = 0; i < 3; i++) {
    await page.evaluate(() => { const c = document.querySelector('#pool .hcard:not(.used):not(.banned)'); c && c.click(); });
    await page.waitForTimeout(150);
  }
  rows.push(await snap('after blue R1 (red ban 1)'));

  /* red bans its 3 */
  for (let i = 0; i < 3; i++) {
    await page.evaluate(() => { const c = document.querySelector('#pool .hcard:not(.used):not(.banned)'); c && c.click(); });
    await page.waitForTimeout(150);
  }
  rows.push(await snap('after round 1 (blue R2)'));

  /* blue's 2 round-2 bans */
  for (let i = 0; i < 2; i++) {
    await page.evaluate(() => { const c = document.querySelector('#pool .hcard:not(.used):not(.banned)'); c && c.click(); });
    await page.waitForTimeout(150);
  }
  rows.push(await snap('after blue R2 (red R2 - blind)'));

  /* red's 2 round-2 bans */
  for (let i = 0; i < 2; i++) {
    await page.evaluate(() => { const c = document.querySelector('#pool .hcard:not(.used):not(.banned)'); c && c.click(); });
    await page.waitForTimeout(150);
  }
  rows.push(await snap('bans done (picks begin)'));

  for (const r of rows) {
    console.log('\n--- ' + r.label + '  [step ' + r.cursorStep + ']');
    console.log('    turn : ' + r.turn);
    console.log('    BLUE bans: ' + r.blueBans.join(' | '));
    console.log('    RED  bans: ' + r.redBans.join(' | '));
  }

  await page.screenshot({ path: 'qa_blind_check.png', fullPage: false });
  console.log('\nERRORS: ' + (errors.length ? JSON.stringify(errors) : 'none'));
  await browser.close();
  process.exit(errors.length ? 1 : 0);
})();
