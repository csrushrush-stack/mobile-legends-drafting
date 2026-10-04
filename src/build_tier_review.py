# -*- coding: utf-8 -*-
"""Per-lane tier list for review, with the stats behind every placement."""
import re, json, os, csv

OUT = os.path.dirname(os.path.abspath(__file__))
html = open(os.path.join(OUT, "draft_app.html"), encoding="utf-8").read()
D = json.loads(re.search(r"const DATA = (\{.*?\});\nconst HERO", html, re.S).group(1))
HEROES = D["heroes"]

LANES = ["EXP", "Jungle", "Mid", "Gold", "Roam"]

def tier_for(i, n, h=None):
    return (h or {}).get("tierNow", "D")

by_lane = {}
for L in LANES:
    rows = [h for h in HEROES if h["lane"] == L]
    rows.sort(key=lambda h: -h["jscore"])
    by_lane[L] = rows

# ---------------- console summary ----------------
for L in LANES:
    rows = by_lane[L]
    print("")
    print("=== %s  (%d heroes) ===" % (L.upper(), len(rows)))
    print("  %-3s %-14s %-6s %7s %7s %7s %7s %6s  %s" %
          ("#", "hero", "tier", "score", "rkWR", "rkBan", "rkPick", "proWR", "flex"))
    for i, h in enumerate(rows[:14]):
        rk = h["rk"] or {}; al = h["all"] or {}
        print("  %-3d %-14s %-6s %7.3f %7.2f %7.2f %7.2f %6s  %s" % (
            i + 1, h["name"], tier_for(i, len(rows), h), h["jscore"],
            rk.get("win", 0), rk.get("ban", 0), rk.get("pick", 0),
            ("%.1f" % al["wr"]) if al else "-",
            "FLEX " + "/".join(h["lanes"]) if h["flex"] else ""))

# ---------------- review sheet ----------------
def esc(s): return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def row_html(i, h):
    rk = h["rk"] or {}; al = h["all"] or {}
    t = tier_for(i, 0, h)
    return ('<tr class="t%s"><td class="rk">%d</td><td class="hb">%s</td>'
            '<td><span class="tb t%s">%s</span></td>'
            '<td class="num">%.3f</td><td class="num">%s</td><td class="num">%s</td>'
            '<td class="num">%s</td><td class="num">%s</td>'
            '<td class="num">%s</td><td class="num">%s</td>'
            '<td class="lanes">%s</td>'
            '<td class="mark"><span class="m ok">&#10003;</span>'
            '<span class="m no">&#10007;</span></td></tr>') % (
        t, i + 1, esc(h["name"]), t, t, h["jscore"],
        ("%.2f" % rk["win"]) if rk else "&ndash;",
        ("%.2f" % rk["ban"]) if rk else "&ndash;",
        ("%.2f" % rk["pick"]) if rk else "&ndash;",
        ("%.1f" % al["wr"]) if al else "&ndash;",
        ("%d" % al["picks"]) if al else "&ndash;",
        ("%.0f" % h["meta"]),
        "/".join(h["lanes"]))

sections = ""
for L in LANES:
    rows = by_lane[L]
    s_count = sum(1 for i in range(len(rows)) if tier_for(i, 0, h) == "S")
    sections += ('<section><h2>%s <span class="cnt">%d heroes &middot; %d S-tier</span></h2>'
                 '<table><thead><tr><th>#</th><th>Hero</th><th>Tier</th>'
                 '<th>Score</th><th>Rank WR</th><th>Rank Ban</th><th>Rank Pick</th>'
                 '<th>Pro WR</th><th>Pro games</th><th>Meta</th><th>Lanes</th>'
                 '<th>Right?</th></tr></thead><tbody>%s</tbody></table></section>'
                 ) % (L, len(rows), s_count,
                      "".join(row_html(i, h) for i, h in enumerate(rows)))

PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MLBB Tier Review - S tier by lane</title>
<style>
body{margin:0;background:#f5f6fa;color:#0f172a;font-family:Inter,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:13.5px}
.wrap{max-width:1100px;margin:0 auto;padding:26px 18px 70px}
header{background:linear-gradient(135deg,#0f172a,#1e3a8a 55%,#0891b2);color:#fff;border-radius:16px;padding:26px 30px;margin-bottom:20px}
header h1{margin:0 0 6px;font-size:24px;letter-spacing:-.4px}
header p{margin:0;opacity:.88;font-size:13.5px;max-width:820px}
.note{background:#fffbeb;border:1px solid #fde68a;border-left:4px solid #f59e0b;border-radius:10px;padding:13px 16px;font-size:12.5px;color:#78350f;margin-bottom:18px}
.note b{color:#92400e}
section{background:#fff;border:1px solid #e5e7eb;border-radius:13px;padding:16px 18px;margin-bottom:16px}
h2{margin:0 0 10px;font-size:16px;letter-spacing:-.2px}
h2 .cnt{font-size:11.5px;color:#94a3b8;font-weight:600;margin-left:6px}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th{background:#f1f5f9;text-align:left;padding:7px 8px;font-size:10px;text-transform:uppercase;letter-spacing:.4px;color:#475569;white-space:nowrap}
td{padding:6px 8px;border-bottom:1px solid #f1f5f9;white-space:nowrap}
tr:hover td{background:#f8fafc}
.rk{color:#94a3b8;font-size:11.5px;text-align:right}
.hb{font-weight:700}
.num{text-align:right;font-variant-numeric:tabular-nums}
.lanes{font-size:11px;color:#64748b}
.tb{display:inline-block;width:20px;text-align:center;border-radius:5px;font-weight:800;color:#fff;font-size:11px;padding:1px 0}
.tS .tb{background:#dc2626}.tA .tb{background:#ea580c}.tB .tb{background:#0891b2}
.tC .tb{background:#64748b}.tD .tb{background:#cbd5e1;color:#475569}
tr.tS td{background:#fff5f5}
tr.tS .hb{color:#b91c1c}
.mark{text-align:center}
.m{font-weight:800;font-size:13px;margin:0 3px;opacity:.25}
.m.ok{color:#16a34a}.m.no{color:#dc2626}
.mark:hover .m{opacity:1;cursor:pointer}
footer{margin-top:26px;padding-top:16px;border-top:1px solid #e5e7eb;color:#64748b;font-size:12px}
</style></head><body><div class="wrap">
<header>
  <h1>MLBB Tier Review &mdash; S tier by lane</h1>
  <p>Every hero, ranked inside its primary lane by the composite the draft app uses.
  Check the S-tier picks for each lane and mark anything that looks wrong.</p>
</header>
<div class="note"><b>How the score works.</b>
<b>score = 0.28&times;high-rank win rate + 0.24&times;high-rank ban rate + 0.16&times;high-rank pick rate
+ 0.16&times;pro win rate + 0.16&times;ranked meta</b>, each min&ndash;max normalised.
Rank columns are the official Mythical Glory+ numbers. <b>Pro WR</b> is the pooled Asian Games + MPL record,
with the sample size beside it &mdash; treat anything under ~15 games as noise.
S = top 5 in the lane, A = next 7, B = next 10, C = next 15, D = the rest.</div>
__SECTIONS__
<footer>Generated from patch 2.2.16 data &middot; ranked stats are the official Moonton Mythical Glory+ snapshot.</footer>
</div></body></html>"""

open(os.path.join(OUT, "MLBB_Tier_Review.html"), "w", encoding="utf-8").write(
    PAGE.replace("__SECTIONS__", sections))

with open(os.path.join(OUT, "MLBB_tier_by_lane.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Lane", "Rank", "Tier", "Hero", "Score", "RankWR", "RankBan", "RankPick",
                "ProWR", "ProGames", "Meta", "Lanes"])
    for L in LANES:
        for i, h in enumerate(by_lane[L]):
            rk = h["rk"] or {}; al = h["all"] or {}
            w.writerow([L, i + 1, tier_for(i, 0, h), h["name"], h["jscore"],
                        rk.get("win", ""), rk.get("ban", ""), rk.get("pick", ""),
                        al.get("wr", "") if al else "", al.get("picks", "") if al else "",
                        round(h["meta"]), "/".join(h["lanes"])])

print("")
print("wrote MLBB_Tier_Review.html and MLBB_tier_by_lane.csv")
