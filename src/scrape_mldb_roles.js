/* Scrape real per-lane hero usage from mldb.gg.
 *
 * mldb match pages expose two things the stats tables don't:
 *   - a per-game scoreboard: player -> hero
 *   - the team roster block: player -> role (GOLD LANER / EXP LANER / ...)
 * Joining them gives the lane each hero was actually played in that game,
 * which is what the hand-coded LANE dict in build_draft_app.py guesses at.
 *
 * Usage: node scrape_mldb_roles.js <tournament name> <out.json> [maxMatches]
 */
const { chromium } = require('C:/Users/Acer/.workbuddy-ai/binaries/node/workspace/node_modules/playwright');
const fs = require('fs');

const TOUR = process.argv[2] || 'MPL Philippines Season 18';
const OUT = process.argv[3] || 'mldb_ph18_roles.json';
const MAX = parseInt(process.argv[4] || '0', 10) || 9999;

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36';

async function passChallenge(page) {
  for (let i = 0; i < 15; i++) {
    const t = await page.evaluate(() => document.body.innerText.slice(0, 200));
    if (!/security verification|Verifying|Just a moment/i.test(t)) return true;
    await page.waitForTimeout(2000);
  }
  return false;
}

(async () => {
  const browser = await chromium.launch({ headless: false, args: ['--disable-blink-features=AutomationControlled'] });
  const ctx = await browser.newContext({ viewport: { width: 1500, height: 1000 }, userAgent: UA, locale: 'en-US' });
  const page = await ctx.newPage();
  await page.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); });

  await page.goto('https://mldb.gg/matches', { waitUntil: 'domcontentloaded', timeout: 90000 });
  await passChallenge(page);
  await page.waitForTimeout(2500);

  // 1) match list
  const matches = await page.evaluate(async (tour) => {
    const token = document.querySelector('meta[name="csrf-token"]')?.content
      || document.querySelector('input[name="_token"]')?.value || '';
    const all = [];
    for (let start = 0; start < 6000; start += 200) {
      const body = new URLSearchParams();
      body.set('_token', token); body.set('draw', '1');
      body.set('start', String(start)); body.set('length', '200');
      body.set('search[value]', tour);
      const r = await fetch('/ajax/matchesTable', {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/x-www-form-urlencoded' },
        body: body.toString(),
      });
      const j = await r.json();
      const d = (j.data || []).filter(x => x.tournament_name === tour);
      all.push(...d);
      if (!j.data || !j.data.length || all.length >= (j.recordsFiltered || 0)) break;
    }
    return all;
  }, TOUR);

  const seen = new Set();
  const uniq = matches.filter(m => (seen.has(m.id) ? false : (seen.add(m.id), true)))
    .filter(m => m.status === 'completed')
    .sort((a, b) => a.timestamp - b.timestamp);
  console.log(`${TOUR}: ${matches.length} rows, ${uniq.length} completed`);

  // 2) per-match lineups
  const out = [];
  let n = 0;
  for (const m of uniq.slice(0, MAX)) {
    n++;
    try {
      await page.goto(m.url, { waitUntil: 'domcontentloaded', timeout: 90000 });
      if (!(await passChallenge(page))) { console.log('  ! challenge stuck', m.url); continue; }
      await page.waitForTimeout(1800);

      const data = await page.evaluate(() => {
        // roster roles: player slug -> role (display names differ from IGN, e.g.
        // "Kyle" vs ign "kyletzy", so the href slug is the only reliable join key)
        const roles = {}, rolesName = {};
        document.querySelectorAll('.mv2-player-details').forEach(d => {
          const ign = d.querySelector('.mv2-player-ign');
          const pill = d.querySelector('.mv2-player-role-pill');
          if (!ign || !pill) return;
          const slug = (ign.getAttribute('href') || '').split('/').pop().toLowerCase();
          const role = pill.textContent.trim();
          if (slug) roles[slug] = role;
          // fallback key: squashed display name ("Tracyyy" -> "tracyyy", slug "tracyy")
          const nm = ign.textContent.trim().toLowerCase().replace(/[^a-z0-9]/g, '');
          if (nm) rolesName[nm] = role;
        });

        // game tabs
        const tabs = [...document.querySelectorAll('[data-game], .mv2-game-tab, a[href*="game"]')]
          .filter(e => /^Game\s*\d+/i.test((e.textContent || '').trim()));

        const readPicks = () => [...document.querySelectorAll('.mv2-player-row')].map(row => {
          const cards = [...row.querySelectorAll('.mv2-player-card')];
          return cards.map(c => {
            const p = c.querySelector('.mv2-p-name');
            const h = c.querySelector('.mv2-p-hero');
            return {
              player: p ? p.textContent.trim() : null,
              playerSlug: p ? (p.getAttribute('href') || '').split('/').pop() : null,
              hero: h ? h.textContent.trim() : null,
            };
          });
        }).flat().filter(x => x.player && x.hero);

        return { roles, rolesName, tabs: tabs.length, picks: readPicks() };
      });

      out.push({
        match: m.id, date: m.date, url: m.url,
        teams: [m.team_one_acronym, m.team_two_acronym],
        score: [m.team_one_score, m.team_two_score],
        roles: data.roles, rolesName: data.rolesName,
        games: data.tabs,
        picks: data.picks,
      });
      console.log(`  [${n}/${uniq.length}] ${m.date} ${m.team_one_acronym} ${m.team_one_score}-${m.team_two_score} ${m.team_two_acronym}  roles=${Object.keys(data.roles).length} picks=${data.picks.length} games=${data.tabs}`);
    } catch (e) {
      console.log('  ! fail', m.id, e.message.slice(0, 80));
    }
    fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
  }

  console.log('wrote', OUT, 'matches', out.length);
  await browser.close();
})();
