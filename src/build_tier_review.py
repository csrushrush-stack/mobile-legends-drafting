# -*- coding: utf-8 -*-
"""Tier review: the player's tier list against the data, lane by lane."""
import re, json, os, csv

OUT = os.path.dirname(os.path.abspath(__file__))
html = open(os.path.join(OUT, "draft_app.html"), encoding="utf-8").read()
D = json.loads(re.search(r"const DATA = (\{.*?\});\nconst HERO", html, re.S).group(1))
HEROES = D["heroes"]
USER = D["userTiers"]
TOTAL_PRO = sum(l["games"] for l in D["leagues"])
LANES = ["EXP", "Jungle", "Mid", "Gold", "Roam"]

USER_SET = {L: set(USER.get(L, [])) for L in LANES}
by_lane = {}
for L in LANES:
    rows = [h for h in HEROES if L in h["lanes"]]
    rows.sort(key=lambda h: (0 if h["name"] in USER_SET[L] else 1, -h["jscore"]))
    by_lane[L] = rows

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

print("PRO GAMES POOLED: %d" % TOTAL_PRO)
for L in LANES:
    yours = USER_SET[L]
    print("")
    print("=== %s  (you rate %d) ===" % (L, len(yours)))
    print("  %-14s %-6s %-6s %6s %6s %6s %8s %7s" %
          ("hero", "yours", "data", "ban%", "pick%", "win%", "proPres", "proWR"))
    for h in by_lane[L][:16]:
        rk = h["rk"] or {}; al = h["all"] or {}
        pres = (al["picks"] / TOTAL_PRO * 100) if al else 0
        print("  %-14s %-6s %-6s %6.2f %6.2f %6.2f %7.2f%% %7s" % (
            h["name"], "S" if h["name"] in yours else "-", h.get("tierNow", "?"),
            rk.get("ban", 0), rk.get("pick", 0), rk.get("win", 0), pres,
            ("%.1f" % al["wr"]) if al else "-"))

def row_html(h, L):
    rk = h["rk"] or {}; al = h["all"] or {}
    pres = (al["picks"] / TOTAL_PRO * 100) if al else 0
    mine = h["name"] in USER_SET[L]
    return ('<tr class="%s"><td class="hb">%s</td><td class="c">%s</td>'
            '<td class="c"><span class="tb t%s">%s</span></td>'
            '<td class="num">%s</td><td class="num">%s</td><td class="num">%s</td>'
            '<td class="num %s">%.2f%%</td><td class="num">%s</td><td class="num">%d</td></tr>') % (
        "mine" if mine else "", esc(h["name"]),
        "&#10003;" if mine else "",
        h.get("tierNow", "D"), h.get("tierNow", "D"),
        ("%.2f" % rk["ban"]) if rk else "&ndash;",
        ("%.2f" % rk["pick"]) if rk else "&ndash;",
        ("%.2f" % rk["win"]) if rk else "&ndash;",
        "hi" if pres >= 5 else "", pres,
        ("%.1f" % al["wr"]) if al else "&ndash;",
        al["picks"] if al else 0)

sections = ""
for L in LANES:
    rows = by_lane[L]
    sections += ('<section><h2>%s <span class="cnt">you rate %d &middot; data S-tier %d</span></h2>'
                 '<table><thead><tr><th>Hero</th><th>Yours</th><th>Data</th>'
                 '<th>Rank ban</th><th>Rank pick</th><th>Rank win</th>'
                 '<th>Pro presence</th><th>Pro WR</th><th>Pro picks</th></tr></thead>'
                 '<tbody>%s</tbody></table></section>') % (
        L, len(USER_SET[L]), sum(1 for h in rows if h.get("tierNow") == "S"),
        "".join(row_html(h, L) for h in rows))

PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MLBB Tier Review - your list vs the data</title>
<style>
body{margin:0;background:#f5f6fa;color:#0f172a;font-family:Inter,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:13.5px}
.wrap{max-width:1080px;margin:0 auto;padding:26px 18px 70px}
header{background:linear-gradient(135deg,#0f172a,#1e3a8a 55%,#0891b2);color:#fff;border-radius:16px;padding:26px 30px;margin-bottom:20px}
header h1{margin:0 0 6px;font-size:24px;letter-spacing:-.4px}
header p{margin:0;opacity:.88;font-size:13.5px;max-width:840px}
.note{background:#f0fdf4;border:1px solid #bbf7d0;border-left:4px solid #16a34a;border-radius:10px;padding:13px 16px;font-size:12.5px;color:#14532d;margin-bottom:18px}
.note b{color:#166534}
section{background:#fff;border:1px solid #e5e7eb;border-radius:13px;padding:16px 18px;margin-bottom:16px}
h2{margin:0 0 10px;font-size:16px;letter-spacing:-.2px}
h2 .cnt{font-size:11.5px;color:#94a3b8;font-weight:600;margin-left:6px}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th{background:#f1f5f9;text-align:left;padding:7px 8px;font-size:10px;text-transform:uppercase;letter-spacing:.4px;color:#475569;white-space:nowrap}
td{padding:6px 8px;border-bottom:1px solid #f1f5f9;white-space:nowrap}
tr:hover td{background:#f8fafc}
tr.mine td{background:#f0fdf4}
tr.mine .hb{color:#14532d;font-weight:750}
.hb{font-weight:650}
.c{text-align:center;color:#16a34a;font-weight:800}
.num{text-align:right;font-variant-numeric:tabular-nums}
.num.hi{color:#b91c1c;font-weight:650}
.tb{display:inline-block;width:19px;text-align:center;border-radius:5px;font-weight:800;color:#fff;font-size:10.5px;padding:1px 0}
.tS{background:#dc2626}.tA{background:#ea580c}.tB{background:#0891b2}.tC{background:#64748b}.tD{background:#cbd5e1;color:#475569}
footer{margin-top:26px;padding-top:16px;border-top:1px solid #e5e7eb;color:#64748b;font-size:12px}
</style></head><body><div class="wrap">
<header>
  <h1>Your tier list vs the data</h1>
  <p>Green rows are heroes you rate. <b>Yours</b> is your call, <b>Data</b> is the ban-rate-derived tier.
  Where the two disagree, the professional columns explain why.</p>
</header>
<div class="note"><b>The two columns measure different things.</b>
<b>Data</b> is built on ranked ban rate at Mythical Glory+. <b>Yours</b> reflects tournament usability.
They disagree most on heroes like Claude (0.07% ranked ban, but picked in 52% of all 960 professional games)
and Lukas (67% ranked ban, but 4 professional games). <b>For drafting, your column is the one that matters</b>
&mdash; the app now uses it for the rules.</div>
__SECTIONS__
<footer>Ranked columns: official Moonton Mythical Glory+ snapshot, patch 2.2.16.
Pro columns: 960 games across Asian Games 2026 and six regional leagues.</footer>
</div></body></html>"""

open(os.path.join(OUT, "MLBB_Tier_Review.html"), "w", encoding="utf-8").write(
    PAGE.replace("__SECTIONS__", sections))

with open(os.path.join(OUT, "MLBB_tier_by_lane.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Lane", "Hero", "YourTier", "DataTier", "RankBan", "RankPick", "RankWin",
                "ProPresence%", "ProWR", "ProPicks"])
    for L in LANES:
        for h in by_lane[L]:
            rk = h["rk"] or {}; al = h["all"] or {}
            w.writerow([L, h["name"], "S" if h["name"] in USER_SET[L] else "",
                        h.get("tierNow", ""), rk.get("ban", ""), rk.get("pick", ""),
                        rk.get("win", ""),
                        round((al["picks"] / TOTAL_PRO * 100) if al else 0, 2),
                        al.get("wr", "") if al else "", al.get("picks", "") if al else 0])

print("")
print("wrote MLBB_Tier_Review.html + MLBB_tier_by_lane.csv")
