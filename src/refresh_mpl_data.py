# -*- coding: utf-8 -*-
"""Refresh the MPL data end to end.

Fetches the current season for the three tracked regions from the Liquipedia
MediaWiki API, validates the tables, rewrites the matching blocks in
league_data.py, then rebuilds the draft app.

Run:  python refresh_mpl_data.py [--no-build]

Safe to run on a schedule: if a region's numbers have not moved it writes the
same content and the rebuild is a no-op.
"""
import glob, io, json, os, re, subprocess, sys, datetime

import fetch_liq_stats as fls

PY = sys.executable
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


def find_node():
    """Newest managed node binary - the version directory changes over time."""
    pats = [
        os.path.expanduser('~/.workbuddy-ai/binaries/node/versions/*/node.exe'),
        os.path.expanduser('~/.workbuddy-ai/binaries/node/versions/*/bin/node'),
        'C:/Users/Acer/.workbuddy-ai/binaries/node/versions/*/node.exe',
    ]
    found = []
    for p in pats:
        found += glob.glob(p)
    found = [f for f in found if 'node_modules' not in f]
    if not found:
        return None
    found.sort()
    return found[-1]


def fetch_mlbbhub(slug, out):
    """Scrape mlbbhub for a region. It updates faster than Liquipedia, so it is
    the preferred source where it covers the region. Returns [] on any failure
    so the caller can fall back."""
    node = find_node()
    if not node or not os.path.exists('scrape_mlbbhub.js'):
        return []
    try:
        r = subprocess.run([node, 'scrape_mlbbhub.js', 'https://mlbbhub.com/mpl/%s/stats' % slug, out],
                           capture_output=True, text=True, timeout=180)
        if r.returncode != 0 or not os.path.exists(out):
            return []
        d = json.load(io.open(out, encoding='utf-8'))
    except Exception:
        return []
    rows = []
    for r_ in d.get('rows', []):
        if not r_.get('hero') or not r_.get('pick'):
            continue
        pick = int(r_['pick'])
        win = int(r_['win'] or 0)
        rows.append(dict(hero=r_['hero'], pick=pick, pick_w=win, pick_l=pick - win,
                         ban=int(r_['ban'] or 0)))
    return rows


REGIONS = [
    dict(lab='PH', var='PH18', page='MPL/Philippines/Season_18/Statistics',
         name='MPL Philippines S18', short='PH', region='Philippines',
         marker='MPL Philippines', mb='ph',
         note='Current MPL PH season. Hirara is the most-picked hero in the league.'),
    dict(lab='ID', var='ID18', page='MPL/Indonesia/Season_18/Statistics',
         name='MPL Indonesia S18', short='ID', region='Indonesia',
         marker='MPL Indonesia', mb='id',
         note='Current MPL ID season, and the deepest hero pool of the three.'),
    dict(lab='MM', var='MM4', page='MLBB_Super_League/Myanmar/Season_4/Statistics',
         name='MSL Myanmar S4', short='MM', region='Myanmar',
         marker='MSL Myanmar', mb=None,
         note='Myanmar won Asian Games gold off the back of this league.'),
]


def fetch(spec):
    """Liquipedia is the baseline (it has win/loss splits and covers Myanmar).
    Where mlbbhub covers the same region and is ahead on games played, prefer
    it - the player wants the freshest possible match data."""
    d = fls.api_get({'action': 'parse', 'page': spec['page'], 'format': 'json', 'prop': 'text'})
    if 'error' in d:
        raise RuntimeError('%s: %s' % (spec['lab'], d['error']['info']))
    rows = fls.parse_hero_table(d['parse']['text']['*'])
    liq_games = sum(r['pick'] or 0 for r in rows) / 10.0
    src = 'liquipedia'

    if spec.get('mb'):
        mb = fetch_mlbbhub(spec['mb'], 'mb_%s.json' % spec['mb'])
        mb_games = sum(r['pick'] or 0 for r in mb) / 10.0
        if mb_games > liq_games:
            print('     mlbbhub is ahead (%.0f vs %.0f games) - using mlbbhub' % (mb_games, liq_games))
            rows, src = mb, 'mlbbhub'

    if not rows:
        raise RuntimeError('%s: no hero rows parsed' % spec['lab'])
    rows = [r for r in rows if r['pick'] and r['pick'] > 0]
    rows.sort(key=lambda r: (-(r['pick'] or 0), -(r['ban'] or 0)))
    spec['src'] = src
    return rows


def validate(spec, rows):
    """Structural checks. Picks must divide by 10 to the game count, and wins +
    losses must equal picks for every hero.

    Bans are a softer signal: PH and ID reconcile exactly, but Myanmar runs
    ~2 games light (a few games have no bans recorded), so the ban-derived
    count is allowed a proportional margin rather than failing the update."""
    picks = sum(r['pick'] or 0 for r in rows)
    bans = sum(r['ban'] or 0 for r in rows)
    games_p, games_b = picks / 10.0, bans / 10.0
    bad = [r['hero'] for r in rows if (r['pick_w'] or 0) + (r['pick_l'] or 0) != r['pick']]
    ok = True
    msgs = []
    if not rows:
        return False, 0, ['empty table']
    gap = abs(games_p - games_b)
    tol = max(2.5, 0.04 * games_p)
    if gap > tol:
        ok = False
        msgs.append('game count disagrees: picks->%.1f bans->%.1f (gap %.1f > tol %.1f)'
                    % (games_p, games_b, gap, tol))
    elif gap > 1.0:
        msgs.append('bans trail picks by %.1f games (unrecorded bans)' % gap)
    if bad:
        ok = False
        msgs.append('W+L != picks for %d heroes (%s)' % (len(bad), ', '.join(bad[:4])))
    return ok, int(round(games_p)), msgs


def render_block(spec, rows, games):
    head = '# ---- %s - %d games ' % (spec['name'], games)
    head = head + '-' * max(3, 78 - len(head))
    out = [head,
           '%s = dict(id="%s", name="%s", short="%s", region="%s",' %
           (spec['var'], spec['short'].lower(), spec['name'], spec['short'], spec['region']),
           '            games=%d, note="%s",' % (games, spec['note'])]
    parts = ['("%s",%d,%d,%d,%d)' % (r['hero'].replace('"', '\\"'), r['pick'], r['pick_w'], r['pick_l'], r['ban'])
             for r in rows]
    cur = '            rows=['
    for i, p in enumerate(parts):
        add = p + (',' if i < len(parts) - 1 else '])')
        if len(cur) + len(add) > 98:
            out.append(cur)
            cur = '                  ' + add
        else:
            cur += add
    out.append(cur)
    return '\n'.join(out) + '\n'


def splice(src, spec, block):
    """Replace a league block, located by its header marker, up to the next
    top-level header (or the LEAGUES line)."""
    m = re.search(r'^# ---- [^\n]*%s[^\n]*\n' % re.escape(spec['marker']), src, re.M)
    if not m:
        raise RuntimeError('block header not found for %s' % spec['marker'])
    start = m.start()
    tail = src[m.end():]
    nxt = re.search(r'^(?:# ---- |LEAGUES = )', tail, re.M)
    end = m.end() + (nxt.start() if nxt else len(tail))
    return src[:start] + block + '\n' + src[end:]


def main():
    build = '--no-build' not in sys.argv
    print('refresh started %s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))

    src = io.open('league_data.py', encoding='utf-8').read()
    summary = []
    for spec in REGIONS:
        rows = fetch(spec)
        ok, games, msgs = validate(spec, rows)
        old = re.search(r'^%s = dict\([^\n]*\n[^\n]*?games=(\d+)' % spec['var'], src, re.M)
        old_games = int(old.group(1)) if old else -1
        status = 'OK' if ok else 'FAIL'
        print('  %-3s %-11s %s  games %d -> %d  heroes %d %s'
              % (spec['lab'], spec.get('src', '?'), status, old_games, games, len(rows),
                 ('| ' + '; '.join(msgs)) if msgs else ''))
        if not ok:
            print('     refusing to write %s until the data validates' % spec['lab'])
            summary.append((spec['lab'], old_games, old_games, False))
            continue
        src = splice(src, spec, render_block(spec, rows, games))
        summary.append((spec['lab'], old_games, games, True))

    io.open('league_data.py', 'w', encoding='utf-8').write(src)

    changed = [s for s in summary if s[1] != s[2]]
    print('\n  regions updated: %s' % (', '.join('%s %d->%d' % (s[0], s[1], s[2]) for s in changed) or 'none'))
    print('  regions held   : %s' % (', '.join(s[0] for s in summary if not s[3]) or 'none'))

    if build:
        print('\n  rebuilding app...')
        r = subprocess.run([PY, 'build_draft_app.py'], capture_output=True, text=True)
        if r.returncode != 0:
            print('  BUILD FAILED')
            print(r.stdout[-2000:])
            print(r.stderr[-2000:])
            sys.exit(1)
        print('  ' + '\n  '.join(l for l in r.stdout.strip().splitlines()[:4]))
        print('  build ok')

    print('refresh done %s' % datetime.datetime.now().strftime('%H:%M'))


if __name__ == '__main__':
    main()
