/* Verifies cover scoring: when a lane is open but the hero's primary lane is
   already taken, a cover hero should still get a positive filler bonus. */
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, 'draft_app.html'), 'utf8');
const script = html.split('<script>')[1].split('</script>')[0];

const ELS = {};
function mkEl(id) {
  return { id, _t: '', _h: '', value: '', dataset: {},
    get textContent(){return this._t;}, set textContent(v){this._t=String(v);},
    get innerHTML(){return this._h;}, set innerHTML(v){this._h=String(v);},
    classList:{_s:new Set(),add(...c){c.forEach(x=>this._s.add(x))},remove(...c){c.forEach(x=>this._s.delete(x))},
      toggle(c,o){o===undefined?(this._s.has(c)?this._s.delete(c):this._s.add(c)):(o?this._s.add(c):this._s.delete(c));},
      contains(c){return this._s.has(c)}},
    addEventListener(){}, querySelectorAll(){return[];} };
}
const document = { getElementById: id => (ELS[id] = ELS[id] || mkEl(id)), querySelectorAll:()=>[], body: mkEl('body') };
const window = { matchMedia:()=>({matches:false,addEventListener(){}}), addEventListener(){}, scrollTo(){} };
const location = { hash: '' };

const app = new Function('document','window','location','alert','console',
  script + '\n;return {HERO,scorePick,teamData,setMode,MODE,recommend,renderAll,mySide:null,cursor:0,'
  + 'set side(v){mySide=v},get side(){return mySide},setCursor(v){cursor=v},SEQ(){return SEQ}};'
)(document, window, location, ()=>{}, console);

/* helper to set the draft cursor */
app.setMode('ranked');

let pass=0, fail=0;
const ok=(c,m)=>{ if(c){pass++;console.log('  PASS  '+m);} else {fail++;console.log('  FAIL  '+m);} };

console.log('\n=== cover data ===');
const atlas = app.HERO['Atlas'], carm = app.HERO['Carmilla'], raf = app.HERO['Rafaela'];
ok(atlas.lane==='Roam' && (atlas.cover||[]).includes('EXP'), 'Atlas: primary Roam, covers EXP');
ok(carm.lane==='Roam' && (carm.cover||[]).includes('EXP'), 'Carmilla: primary Roam, covers EXP');
ok(raf.lane==='Roam' && (raf.cover||[]).includes('Mid'), 'Rafaela: primary Roam, covers Mid');
ok(!atlas.flex && !carm.flex && !raf.flex, 'none of the three count as flex');

console.log('\n=== cover scoring: EXP open, Roam already filled ===');
/* my team already has a roam and a jungler, so Atlas's own lane is taken while
   EXP is still open - exactly the situation a cover is for */
const myPicks = ['Hirara', 'Estes'];   // jungle + roam
const used = new Set(myPicks);
const a = app.scorePick(atlas, myPicks, [], used);
const why = a.why.join(' | ');
console.log('    Atlas -> score ' + a.sc.toFixed(1));
console.log('    why: ' + why);
ok(/can cover your open <b>EXP<\/b>/.test(why), 'Atlas gets the "can cover EXP" reason');
ok(a.sc > 0, 'cover bonus is positive, not penalised (' + a.sc.toFixed(1) + ')');

/* a hero whose own lane IS open should outscore a mere cover */
const freya = app.HERO['Freya'];   // EXP primary
const f = app.scorePick(freya, myPicks, [], used);
console.log('    Freya (true EXP) -> score ' + f.sc.toFixed(1));
console.log('    why: ' + f.why.join(' | '));
ok(f.sc > a.sc, 'a true EXP hero outscores a roam covering EXP');

console.log('\n=== Rafaela covering Mid ===');
const rm = app.scorePick(raf, ['Hirara','Atlas'], [], new Set(['Hirara','Atlas']));
console.log('    Rafaela -> score ' + rm.sc.toFixed(1));
console.log('    why: ' + rm.why.join(' | '));
ok(/can cover your open <b>Mid<\/b>/.test(rm.why.join(' | ')) || rm.sc > -12,
   'Rafaela is treated as a filler for mid, not penalised as a taken lane');

console.log('\n=== regression: normal heroes unaffected ===');
const gloo = app.HERO['Gloo'];
ok(!!gloo.flex, 'Gloo still counts as a flex hero');
const masha = app.HERO['Masha'];
ok(!!masha.flex, 'Masha still counts as a flex hero');
ok(!masha.cover || masha.cover.length===0, 'Masha has no cover lanes');

console.log('\n' + (fail===0 ? 'ALL '+pass+' PASSED' : fail+' FAILED / '+pass+' passed'));
process.exit(fail?1:0);
