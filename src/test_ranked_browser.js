/* Drives the real draft_app.html in Chromium through a full ranked draft and
   screenshots each phase, so we verify what the user actually sees. */
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
  await page.waitForTimeout(400);

  /* switch to ranked */
  await page.click('#dRk');
  await page.waitForTimeout(200);
  await page.click('#pickBlue');
  await page.waitForTimeout(200);

  const readBoard = () => page.evaluate(() => {
    const grab = id => Array.from(document.querySelectorAll('#' + id + ' .slot'))
      .map(s => (s.textContent || '').trim().replace(/\s+/g, ' '));
    return {
      blueBans: grab('blueBans'),
      redBans: grab('redBans'),
      bluePicks: grab('bluePicks'),
      redPicks: grab('redPicks'),
      turn: (document.getElementById('turnLabel') || {}).textContent,
      reveal: (document.getElementById('revealWrap') || {}).textContent,
      seqBlind: document.querySelectorAll('.seqdot.blind').length,
    };
  });

  const out = {};
  out.step0 = await readBoard();
  await page.screenshot({ path: 'qa_ranked_1_phase1.png', fullPage: false });

  /* blue bans 3 */
  const poolNames = await page.evaluate(() =>
    Array.from(document.querySelectorAll('#pool .hcard')).map(c => c.dataset.hero));
  const pick = n => poolNames[n % poolNames.length];

  await page.click('#pool .hcard[data-hero="' + pick(0) + '"]');
  await page.waitForTimeout(120);
  await page.click('#pool .hcard[data-hero="' + pick(1) + '"]');
  await page.waitForTimeout(120);
  await page.click('#pool .hcard[data-hero="' + pick(2) + '"]');
  await page.waitForTimeout(200);
  out.afterBlueR1 = await readBoard();

  /* red bans 3 - we are tracking the enemy, their bans should be visible now */
  await page.click('#pool .hcard[data-hero="' + pick(3) + '"]');
  await page.waitForTimeout(120);
  await page.click('#pool .hcard[data-hero="' + pick(4) + '"]');
  await page.waitForTimeout(120);
  await page.click('#pool .hcard[data-hero="' + pick(5) + '"]');
  await page.waitForTimeout(250);
  out.afterRound1 = await readBoard();
  await page.screenshot({ path: 'qa_ranked_2_round1_done.png', fullPage: false });

  /* round 2: blue 2 */
  await page.click('#pool .hcard[data-hero="' + pick(6) + '"]');
  await page.waitForTimeout(120);
  await page.click('#pool .hcard[data-hero="' + pick(7) + '"]');
  await page.waitForTimeout(200);
  out.afterBlueR2 = await readBoard();

  /* red 2 */
  await page.click('#pool .hcard[data-hero="' + pick(8) + '"]');
  await page.waitForTimeout(120);
  await page.click('#pool .hcard[data-hero="' + pick(9) + '"]');
  await page.waitForTimeout(250);
  out.bansDone = await readBoard();
  await page.screenshot({ path: 'qa_ranked_3_bans_done.png', fullPage: false });

  /* picks */
  for (let i = 10; i < 20; i++) {
    const h = await page.evaluate(() => {
      const c = document.querySelector('#pool .hcard:not(.used):not(.banned)');
      return c ? c.dataset.hero : null;
    });
    if (!h) break;
    await page.click('#pool .hcard[data-hero="' + h + '"]');
    await page.waitForTimeout(100);
  }
  await page.waitForTimeout(250);
  out.done = await readBoard();
  await page.screenshot({ path: 'qa_ranked_4_done.png', fullPage: false });

  /* duplicate-ban probe: reset, ban the same hero on both sides */
  await page.click('#resetBtn');
  await page.waitForTimeout(200);
  const dupHero = 'Nolan';
  await page.click('#pool .hcard[data-hero="' + dupHero + '"]');
  await page.waitForTimeout(120);
  /* fill blue's remaining 2 round-1 bans */
  await page.evaluate(() => {
    const c = document.querySelectorAll('#pool .hcard:not(.used):not(.banned)');
    c[0] && c[0].click();
  });
  await page.waitForTimeout(120);
  await page.evaluate(() => {
    const c = document.querySelectorAll('#pool .hcard:not(.used):not(.banned)');
    c[0] && c[0].click();
  });
  await page.waitForTimeout(200);
  /* now red's turn - ban Nolan again */
  const dupClickable = await page.evaluate(() => {
    const el = document.querySelector('#pool .hcard[data-hero="Nolan"]');
    if (!el) return 'missing';
    return el.className;
  });
  if (dupClickable !== 'missing') {
    await page.click('#pool .hcard[data-hero="Nolan"]');
    await page.waitForTimeout(200);
  }
  out.dup = { heroClass: dupClickable, ...(await readBoard()) };
  await page.screenshot({ path: 'qa_ranked_5_dupe.png', fullPage: false });

  console.log(JSON.stringify(out, null, 2));
  console.log('\nERRORS: ' + (errors.length ? JSON.stringify(errors, null, 2) : 'none'));
  await browser.close();
  process.exit(errors.length ? 1 : 0);
})();
