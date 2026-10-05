/* Headless smoke test for the ranked ban phase.
   Stubs just enough DOM to run draft_app.html's script and walks the whole draft. */
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, 'draft_app.html'), 'utf8');
const script = html.split('<script>')[1].split('</script>')[0];

/* ---- DOM stub ------------------------------------------------------- */
const ELS = {};
function mkEl(id) {
  const el = {
    id,
    _text: '',
    _html: '',
    value: '',
    dataset: {},
    children: [],
    get textContent() { return this._text; },
    set textContent(v) { this._text = String(v); },
    get innerHTML() { return this._html; },
    set innerHTML(v) { this._html = String(v); },
    classList: {
      _s: new Set(),
      add(...c) { c.forEach(x => this._s.add(x)); },
      remove(...c) { c.forEach(x => this._s.delete(x)); },
      toggle(c, on) { if (on === undefined) { this._s.has(c) ? this._s.delete(c) : this._s.add(c); } else if (on) this._s.add(c); else this._s.delete(c); },
      contains(c) { return this._s.has(c); },
    },
    addEventListener() {},
    querySelectorAll() { return []; },
  };
  return el;
}
function byId(id) {
  if (!ELS[id]) ELS[id] = mkEl(id);
  return ELS[id];
}
const document = {
  getElementById: byId,
  querySelectorAll() { return []; },
  body: mkEl('body'),
};
const window = {
  matchMedia: () => ({ matches: false, addEventListener() {} }),
  addEventListener() {},
  scrollTo() {},
};
const location = { hash: '' };
const alert = () => {};

const sandbox = { document, window, location, alert, console, Math, Set, Array, Object, JSON, parseInt, parseFloat, isNaN };
const fn = new Function('document', 'window', 'location', 'alert', 'console',
  script + '\n;return {SEQ,get SEQV(){return SEQ},setMode,assign,get cursor(){return cursor},set cursor(v){cursor=v},'
  + 'teamData,usedSet,banHidden,enemyHiddenNames,slotIndex,SEQ_RANKED,SEQ_TOURNEY,get mySide(){return mySide},set mySide(v){mySide=v},'
  + 'get blueBans(){return blueBans},get redBans(){return redBans},getSlot,setSlot,renderAll,canStillBan,roundEndAt,MODE,get MODEV(){return MODE}};');

const app = fn(document, window, location, alert, console);

let pass = 0, fail = 0;
function ok(cond, msg) {
  if (cond) { pass++; console.log('  PASS  ' + msg); }
  else { fail++; console.log('  FAIL  ' + msg); }
}

console.log('\n=== 1. sequence shape ===');
const R = app.SEQ_RANKED;
ok(R.length === 20, 'ranked sequence has 20 steps (got ' + R.length + ')');
const bans = R.filter(s => s.t === 'ban');
ok(bans.length === 10, '10 total bans (got ' + bans.length + ')');
const bb = bans.filter(s => s.s === 'blue');
const rb = bans.filter(s => s.s === 'red');
ok(bb.length === 5 && rb.length === 5, '5 blue bans + 5 red bans (got ' + bb.length + '/' + rb.length + ')');
ok(bb.slice(0, 3).every(s => s.b === 1) && rb.slice(0, 3).every(s => s.b === 1), 'round 1 is 3 bans each');
ok(bb.slice(3).every(s => s.b === 2) && rb.slice(3).every(s => s.b === 2), 'round 2 is 2 bans each');
/* grouped, not alternating */
const order = bans.map(s => s.s === 'blue' ? 'b' : 'r').join('');
ok(order === 'bbbrrrbbrr', 'bans grouped bbb rrr bb rr (got ' + order + ')');
const picks = R.filter(s => s.t === 'pick').map(s => s.s === 'blue' ? 'b' : 'r').join('');
ok(picks === 'brrbbrrbbr', 'pick order B1 R2 B2 R2 B2 R1 (got ' + picks + ')');

console.log('\n=== 2. reveal timing ===');
app.setMode('ranked');
app.mySide = 'blue';
ok(app.roundEndAt(1) === 6, 'round 1 ends at step 6 (got ' + app.roundEndAt(1) + ')');
ok(app.roundEndAt(2) === 10, 'round 2 ends at step 10 (got ' + app.roundEndAt(2) + ')');

/* enemy (red) round-1 bans are hidden early, then revealed */
app.cursor = 0;
ok(app.banHidden(3) === true, 'red ban #1 hidden at step 0');
ok(app.banHidden(0) === false, 'own ban never hidden');
app.cursor = 6;
ok(app.banHidden(3) === false, 'red round-1 ban visible once round 1 ends');
app.cursor = 6;   /* blue's turn in round 2 -> red's round-2 bans stay blind */
ok(app.banHidden(8) === true, 'red round-2 ban still hidden after round 1');
app.cursor = 10;  /* picks have begun -> everything is public */
ok(app.banHidden(8) === false, 'red round-2 ban visible once picks begin');
app.cursor = 3;   /* the enemy is banning -> we watch them do it */
ok(app.banHidden(3) === false, 'enemy ban visible while tracking the enemy turn');

/* duplicates: blue bans Nolan, then red bans Nolan too */
console.log('\n=== 3. duplicate bans ===');
app.blueBans[0] = 'Nolan';
app.redBans[0] = 'Nolan';
ok(app.blueBans[0] === 'Nolan' && app.redBans[0] === 'Nolan',
   'same hero can sit in a blue ban and a red ban');
const td = app.teamData('blue'), tdR = app.teamData('red');
ok(td.bans.includes('Nolan') && tdR.bans.includes('Nolan'), 'both teamData() report Nolan as banned');

/* a duplicate ban must NOT block the other side from banning it */
app.cursor = slot(6); // blue round 2
app.setMode('ranked'); app.mySide = 'blue'; app.cursor = 6;
ok(app.canStillBan('Nolan') === true, 'duplicate ban does not block re-banning');

console.log('\n=== 4. no leak of blind bans ===');
app.setMode('ranked'); app.mySide = 'blue'; app.cursor = 0;
app.blueBans[0] = 'Nolan'; app.redBans[0] = 'Gusion';
let hidden = app.enemyHiddenNames('blue');
ok(hidden.includes('Gusion') && !hidden.includes('Nolan'), 'blind enemy ban listed as hidden');
app.cursor = 6;
hidden = app.enemyHiddenNames('blue');
ok(hidden.length === 0 || !hidden.includes('Gusion'), 'enemy round-1 ban no longer hidden after reveal');

console.log('\n=== 5. slot indexing ===');
app.setMode('ranked');
ok(app.slotIndex('blue', 'ban', 0) === 0, 'blue ban 0 -> step 0');
ok(app.slotIndex('blue', 'ban', 2) === 2, 'blue ban 2 -> step 2');
ok(app.slotIndex('red', 'ban', 0) === 3, 'red ban 0 -> step 3');
ok(app.slotIndex('red', 'ban', 4) === 9, 'red ban 4 -> step 9');
ok(app.slotIndex('blue', 'pick', 0) === 10, 'blue pick 0 -> step 10');
ok(app.slotIndex('red', 'pick', 4) === 19, 'red pick 4 -> step 19');

console.log('\n=== 6. full draft walk (no crash) ===');
app.setMode('ag'); app.setMode('ranked');   // clean slate
app.mySide = 'blue';
let err = null;
try {
  for (let i = 0; i < 20; i++) {
    app.cursor = i;
    app.assign('HERO' + i);
  }
  app.renderAll();
} catch (e) { err = e; }
ok(!err, 'walking all 20 steps renders without throwing' + (err ? ' -> ' + err.message : ''));
ok(app.blueBans.filter(Boolean).length === 5, 'blue has 5 bans (got ' + app.blueBans.filter(Boolean).length + ')');
ok(app.redBans.filter(Boolean).length === 5, 'red has 5 bans (got ' + app.redBans.filter(Boolean).length + ')');

/* assign() must auto-advance through the ban phase, not skip to picks */
app.setMode('ag'); app.setMode('ranked');   // force a real sequence reset
app.mySide = 'blue';
app.cursor = 0;
app.assign('Nolan');
ok(app.cursor === 1, 'after 1st ban cursor advances to step 1 (got ' + app.cursor + ')');
app.assign('Gusion'); app.assign('Harith');
ok(app.cursor === 3, 'after 3rd ban cursor lands on red ban 1 (got ' + app.cursor + ')');

console.log('\n=== 7. tournament mode untouched ===');
const T = app.SEQ_TOURNEY;
ok(T.length === 20, 'tourney sequence still 20 steps');
app.setMode('ag');
ok(app.banHidden(0) === false && app.banHidden(1) === false, 'no blind bans outside ranked');
err = null;
try { app.renderAll(); } catch (e) { err = e; }
ok(!err, 'AG mode renders' + (err ? ' -> ' + err.message : ''));

console.log('\n=== 8. ranked full render ===');
app.setMode('ranked');
app.mySide = null;
err = null;
try { app.renderAll(); } catch (e) { err = e; }
ok(!err, 'ranked renders with no side chosen' + (err ? ' -> ' + err.message : ''));
app.mySide = 'red';
err = null;
try { app.renderAll(); } catch (e) { err = e; }
ok(!err, 'ranked renders as RED' + (err ? ' -> ' + err.message : ''));
app.mySide = 'blue';
app.cursor = 7;
err = null;
try { app.renderAll(); } catch (e) { err = e; }
ok(!err, 'ranked renders mid round 2' + (err ? ' -> ' + err.message : ''));

function slot(n) { return n; }

console.log('\n' + (fail === 0 ? 'ALL ' + pass + ' CHECKS PASSED' : fail + ' FAILED / ' + pass + ' passed'));
process.exit(fail === 0 ? 0 : 1);
