# -*- coding: utf-8 -*-
"""Turn scraped mldb lineups into measured per-lane hero usage.

Joins each game's (player -> hero) scoreboard to the roster's (player -> role)
and counts how often each hero is actually fielded in each lane. This is the
ground truth the hand-coded LANE dict in build_draft_app.py was guessing at.

Usage: python analyze_roles.py [roles.json ...]
"""
import io, json, os, sys
from collections import defaultdict

ROLE = {"EXP LANER": "EXP", "GOLD LANER": "Gold", "MID LANER": "Mid",
        "JUNGLER": "Jungle", "ROAMER": "Roam"}
LANES = ["EXP", "Jungle", "Mid", "Gold", "Roam"]


def squash(s):
    return "".join(c for c in (s or "").lower() if c.isalnum())


def load(paths):
    per_hero = defaultdict(lambda: defaultdict(int))   # hero -> lane -> games
    per_hero_total = defaultdict(int)
    unmatched = 0
    games = 0
    for p in paths:
        for m in json.load(io.open(p, encoding="utf-8")):
            roles = m.get("roles") or {}
            roles_name = m.get("rolesName") or {}
            picks = m.get("picks") or []
            if not picks:
                continue
            games += len(picks) // 10
            for k in picks:
                slug = (k.get("playerSlug") or "").lower()
                role = roles.get(slug) or roles_name.get(squash(k.get("player")))
                lane = ROLE.get((role or "").strip().upper().replace("  ", " "))
                if not lane:
                    unmatched += 1
                    continue
                per_hero[k["hero"]][lane] += 1
                per_hero_total[k["hero"]] += 1
    return per_hero, per_hero_total, unmatched, games


def main():
    paths = sys.argv[1:] or ["mldb_ph18_roles.json"]
    per_hero, total, unmatched, games = load(paths)
    print("games parsed:", games, "| picks joined:", sum(total.values()), "| unmatched:", unmatched)

    rows = []
    for hero, lanes in per_hero.items():
        n = sum(lanes.values())
        top = max(lanes.items(), key=lambda kv: kv[1])
        rows.append((n, hero, top[0], top[1] / n * 100.0, dict(lanes)))
    rows.sort(key=lambda r: -r[0])

    print("\nhero                          n   primary      share   distribution")
    for n, hero, prim, share, lanes in rows:
        dist = "  ".join("%s %d" % (l, lanes[l]) for l in LANES if lanes.get(l))
        print("%-26s %4d   %-8s %5.1f%%   %s" % (hero, n, prim, share, dist))

    out = {hero: {"n": n, "primary": prim, "share": round(share, 1), "lanes": lanes}
           for n, hero, prim, share, lanes in rows}
    io.open("mldb_role_summary.json", "w", encoding="utf-8").write(
        json.dumps(out, indent=1, ensure_ascii=False))
    print("\nwrote mldb_role_summary.json (%d heroes)" % len(out))


if __name__ == "__main__":
    main()
