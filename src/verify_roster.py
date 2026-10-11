# -*- coding: utf-8 -*-
"""Verify the trimmed league set loads, and that every hero named in the new
MPL data actually exists in the app's hero roster (so nothing is silently
dropped from the draft pool)."""
import json, io, sys
sys.path.insert(0, '.')

from league_data import LEAGUES

print('leagues kept:')
tot = 0
for lg in LEAGUES:
    tot += lg['games']
    print('  %-5s %-24s %4d games  %3d heroes' % (lg['id'], lg['name'], lg['games'], len(lg['rows'])))
print('  TOTAL %d games' % tot)

app = json.load(io.open('draft_data.json', encoding='utf-8'))
roster = set(h['name'] for h in app['heroes'])
print('\napp roster: %d heroes' % len(roster))

missing = {}
for lg in LEAGUES:
    bad = [r[0] for r in lg['rows'] if r[0] not in roster]
    if bad:
        missing[lg['id']] = bad
print('heroes in league data but NOT in the app roster:', missing if missing else 'none')

for lg in LEAGUES:
    if lg['id'] == 'ag':
        continue
    n = sum(1 for r in lg['rows'] if r[1] > 0)
    print('  %s: %d heroes with at least one pick' % (lg['id'], n))
