// Query the official Moonton hero-rank API directly for the top rank tier.
const fs = require('fs');

const API = 'https://api.gms.moontontech.com/api/gms/source/2669606/2756567';
const FIELDS = ['main_hero', 'main_hero_appearance_rate', 'main_hero_ban_rate', 'main_hero_channel',
  'main_hero_win_rate', 'main_heroid', 'data.sub_hero.hero', 'data.sub_hero.hero_channel',
  'data.sub_hero.increase_win_rate', 'data.sub_hero.heroid'];

async function query(bigrank, matchType, pageSize) {
  const body = {
    pageSize: pageSize || 200,
    pageIndex: 1,
    filters: [
      { field: 'bigrank', operator: 'eq', value: String(bigrank) },
      { field: 'match_type', operator: 'eq', value: matchType }
    ],
    sorts: [
      { data: { field: 'main_hero_win_rate', order: 'desc' }, type: 'sequence' },
      { data: { field: 'main_heroid', order: 'desc' }, type: 'sequence' }
    ],
    fields: FIELDS
  };
  const r = await fetch(API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'https://www.mobilelegends.com',
               'Referer': 'https://www.mobilelegends.com/' },
    body: JSON.stringify(body)
  });
  const j = await r.json();
  const recs = (j.data && j.data.records) || [];
  return recs.map(x => {
    const d = x.data;
    return {
      name: d.main_hero && d.main_hero.data ? d.main_hero.data.name : '?',
      heroid: d.main_heroid,
      pick: +(d.main_hero_appearance_rate * 100).toFixed(2),
      win: +(d.main_hero_win_rate * 100).toFixed(2),
      ban: +(d.main_hero_ban_rate * 100).toFixed(2),
      counters: (d.sub_hero || []).map(s => ({
        heroid: s.heroid,
        delta: +(s.increase_win_rate * 100).toFixed(2)
      }))
    };
  });
}

(async () => {
  const out = {};
  for (const mt of [0, 1, 2, 3, 4]) {
    try {
      const rows = await query(9, mt, 200);
      const top = rows.slice(0, 3).map(r => `${r.name} ${r.win}%/${r.ban}%`).join(', ');
      console.log(`match_type=${mt}  rows=${rows.length}  top: ${top}`);
      out['mt' + mt] = rows;
    } catch (e) {
      console.log(`match_type=${mt}  ERROR ${e.message}`);
    }
  }
  // also grab the ALL-rank baseline for comparison
  try { out.all7 = await query(101, 2, 200); console.log('ALL ranks 7d rows:', out.all7.length); }
  catch (e) { console.log('ALL ranks error', e.message); }

  fs.writeFileSync('C:/Users/Acer/WorkBuddy AI/2026-10-04-13-37-19/rank_official.json', JSON.stringify(out, null, 1));
  console.log('saved');
})();
