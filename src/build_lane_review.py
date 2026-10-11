# -*- coding: utf-8 -*-
"""Lane review: how each hero actually performs in the current dataset.

This replaces the old tier review. Tiers were a letter grade derived from the
ranked ladder's ban rate, which said little about whether a hero would win the
game you are drafting for. This report instead shows the numbers the draft app
ranks on - win rate with its sample size, and how contested the hero is.

Output: MLBB_Lane_Review.html + MLBB_lane_performance.csv
"""
import csv, json, os

OUT = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(OUT, "draft_data.json"), encoding="utf-8"))
HEROES = D["heroes"]
LEAGUES = D["leagues"]
LANES = ["EXP", "Jungle", "Mid", "Gold", "Roam"]
GAMES = sum(l["games"] for l in LEAGUES)
MIN_PICKS = 5


def conf(n):
    return min(1.0, n / 30.0)


K_SHRINK = 12.0


def adj_wr(d):
    """Shrink the win rate toward 50% on small samples, exactly as the app does.
    A 6-1 hero reads as 63%, not 86%, because 7 games cannot support 86%."""
    return (d["wins"] + K_SHRINK * 0.5) / (d["picks"] + K_SHRINK) * 100.0


def score(h):
    d = h.get("all")
    if not d:
        return None
    return ((adj_wr(d) - 50) * 2.4 * (0.4 + 0.6 * conf(d["picks"]))
            + min(1.0, d["presence"] / 100.0) * 16)


def rows_for(lane):
    out = []
    for h in HEROES:
        if h["lane"] != lane:
            continue
        d = h.get("all")
        if not d or d["picks"] < MIN_PICKS:
            continue
        out.append((score(h), h, d))
    out.sort(key=lambda x: -x[0])
    return out


def cls(v, good, bad):
    return "g" if v >= good else ("b" if v < bad else "")


sections = []
csv_rows = []
for L in LANES:
    rows = rows_for(L)
    body = []
    for i, (s, h, d) in enumerate(rows, 1):
        rk = h.get("rk") or {}
        thin = d["picks"] < 15
        body.append(
            "<tr>"
            '<td class="n">%d</td><td class="h">%s</td>'
            '<td class="%s">%.1f%%%s</td><td class="m">%d</td>'
            '<td class="m">%d</td><td class="m">%d</td>'
            '<td class="%s">%.0f%%</td>'
            '<td class="m">%s</td><td class="m">%s</td>'
            "</tr>" % (
                i, h["name"],
                cls(d["wr"], 55, 45), d["wr"],
                (' <span class="thin" title="thin sample, shrunk toward 50%% for ranking">*</span>' if thin else ""),
                d["picks"],
                d["bans"], d["picks"] + d["bans"],
                cls(d["presence"], 60, 25), d["presence"],
                ("%.1f%%" % rk["win"]) if rk else "&ndash;",
                ("%.1f%%" % rk["ban"]) if rk else "&ndash;",
            ))
        csv_rows.append([L, h["name"], "%.1f" % d["wr"], d["picks"], d["bans"],
                         "%.1f" % d["presence"], rk.get("win", ""), rk.get("ban", ""),
                         "%.1f" % s])
    sections.append(
        '<section><h2>%s <span class="cnt">%d heroes with %d+ pro games</span></h2>'
        '<table><thead><tr>'
        '<th></th><th>Hero</th><th>Win rate</th><th>Games</th>'
        '<th>Bans</th><th>P+B</th><th>Presence</th>'
        '<th>Rank win</th><th>Rank ban</th>'
        '</tr></thead><tbody>%s</tbody></table></section>'
        % (L, len(rows), MIN_PICKS, "".join(body)))

league_rows = "".join(
    '<tr><td class="h">%s</td><td class="m">%s</td><td class="m">%d</td>'
    '<td class="m">%d</td></tr>' % (l["name"], l["region"], l["games"], l["heroes"])
    for l in LEAGUES)

HTML = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MLBB lane performance review</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#f6f7f9;color:#0f172a;
  font:14px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:34px 20px 70px}
h1{font-size:25px;margin:0 0 6px}
.sub{color:#64748b;margin:0 0 22px}
.lead{background:#fff;border:1px solid #e2e8f0;border-radius:12px;padding:15px 18px;margin:0 0 26px}
.lead b{color:#0f172a}
section{margin:0 0 28px}
h2{font-size:16px;margin:0 0 10px;display:flex;align-items:baseline;gap:9px}
.cnt{font-size:12px;font-weight:500;color:#94a3b8}
table{width:100%;border-collapse:collapse;background:#fff;
  border:1px solid #e2e8f0;border-radius:12px;overflow:hidden}
th,td{padding:7px 11px;text-align:right;border-bottom:1px solid #f1f5f9}
th{background:#f8fafc;font-size:10.5px;text-transform:uppercase;letter-spacing:.4px;
  color:#64748b;font-weight:700}
td.n{color:#cbd5e1;font-variant-numeric:tabular-nums;width:34px}
td.h,th:nth-child(2){text-align:left;font-weight:700}
td.m{color:#475569;font-variant-numeric:tabular-nums}
td.g{color:#15803d;font-weight:700;font-variant-numeric:tabular-nums}
td.b{color:#b91c1c;font-weight:700;font-variant-numeric:tabular-nums}
.thin{color:#b45309;font-weight:700;cursor:help}
tbody tr:last-child td{border-bottom:0}
tbody tr:hover{background:#fafbfc}
.note{color:#64748b;font-size:12.5px;margin-top:26px}
</style></head><body><div class="wrap">
<h1>Lane performance review</h1>
<p class="sub">What the current MPL data says, lane by lane &middot; __GAMES__ games</p>
<div class="lead">
<b>No tiers.</b> A hero is not graded S or A here. The order is the draft app's own
formula: win rate above 50 scaled by how much the sample can be trusted, plus how
contested the hero is. <b>Win rate</b> is the pooled professional record across the
selected leagues, <b>Games</b> is how many times it was picked, <b>Bans</b> how often
it was denied, and <b>Presence</b> is picks + bans over total games. <b>Rank win</b> and
<b>Rank ban</b> are the publisher's Mythical Glory+ ladder figures, shown for contrast
&mdash; the ladder and tournament play disagree regularly.
</div>
<section><h2>Datasets pooled <span class="cnt">__LGAMES__ games across __NLEAG__ events</span></h2>
<table><thead><tr><th></th><th>League</th><th>Region</th><th>Games</th><th>Heroes</th></tr></thead>
<tbody>__LEAGUES__</tbody></table></section>
__SECTIONS__
<p class="note">Heroes with fewer than __MIN__ professional games are left out &mdash; a
record that thin cannot separate signal from luck. Ranked ladder figures are patch 2.2.16.</p>
</div></body></html>
"""

HTML = (HTML.replace("__GAMES__", str(GAMES))
            .replace("__LEAGUES__", league_rows)
            .replace("__LGAMES__", str(GAMES))
            .replace("__NLEAG__", str(len(LEAGUES)))
            .replace("__SECTIONS__", "".join(sections))
            .replace("__MIN__", str(MIN_PICKS)))

open(os.path.join(OUT, "MLBB_Lane_Review.html"), "w", encoding="utf-8").write(HTML)
with open(os.path.join(OUT, "MLBB_lane_performance.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["Lane", "Hero", "ProWR", "Picks", "Bans", "Presence%",
                "RankWin%", "RankBan%", "Score"])
    w.writerows(csv_rows)

print("wrote MLBB_Lane_Review.html + MLBB_lane_performance.csv")
for L in LANES:
    rows = rows_for(L)
    print("  %-7s %2d heroes | top: %s" % (L, len(rows), ", ".join(h["name"] for _, h, _ in rows[:5])))
