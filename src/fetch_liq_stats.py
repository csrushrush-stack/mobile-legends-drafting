# -*- coding: utf-8 -*-
"""Pull a Liquipedia MLBB tournament hero-stats table via the MediaWiki API.

Liquipedia's HTML pages sit behind a Cloudflare browser challenge, but the API
does not. The API also returns the fully rendered table, which is richer than
third-party aggregators: pick/win/loss totals, blue-side and red-side splits,
and ban counts.

Usage:  python fetch_liq_stats.py <Page/Title/With_Slashes> <out.json>
"""
import json, io, re, sys, urllib.request, gzip

API = "https://liquipedia.net/mobilelegends/api.php"
UA = "MLBBDraftApp/1.0 (contact: draft-app@example.com)"


def api_get(params):
    qs = "&".join("%s=%s" % (k, urllib.parse.quote(str(v), safe="")) for k, v in params.items())
    req = urllib.request.Request(API + "?" + qs, headers={
        "User-Agent": UA,
        "Accept-Encoding": "gzip",
    })
    raw = urllib.request.urlopen(req, timeout=90).read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8", "replace"))


def text_of(cell):
    t = cell.get_text(" ", strip=True)
    t = t.replace("\u00a0", " ").replace("\u2211", "").strip()
    return t


def num(s):
    s = re.sub(r"[^0-9.\-]", "", str(s or ""))
    if s in ("", "-", "."):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def parse_hero_table(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "lxml")

    best = None
    for tb in soup.find_all("table"):
        rows = tb.find_all("tr", class_="character-stats-row")
        if rows and (best is None or len(rows) > len(best[1])):
            best = (tb, rows)
    if not best:
        return []
    tb, rows = best

    out = []
    for tr in rows:
        tds = tr.find_all("td", recursive=False)
        if len(tds) < 20:
            continue
        hero = text_of(tds[1])
        hero = re.sub(r"\s+", " ", hero).strip()
        # strip a leading icon alt duplicate if present
        rec = dict(
            hero=hero,
            pick=num(text_of(tds[2])),
            pick_w=num(text_of(tds[3])),
            pick_l=num(text_of(tds[4])),
            pick_wr=num(text_of(tds[5])),
            blue=num(text_of(tds[7])),
            blue_w=num(text_of(tds[8])),
            blue_l=num(text_of(tds[9])),
            red=num(text_of(tds[11])),
            red_w=num(text_of(tds[12])),
            red_l=num(text_of(tds[13])),
            ban=num(text_of(tds[15])),
            pb=num(text_of(tds[17])),
        )
        out.append(rec)
    return out


def main():
    page = sys.argv[1]
    outfile = sys.argv[2] if len(sys.argv) > 2 else "liq_out.json"

    d = api_get({"action": "parse", "page": page, "format": "json", "prop": "text"})
    if "error" in d:
        print("ERROR:", d["error"]["info"])
        sys.exit(1)

    html = d["parse"]["text"]["*"]
    title = d["parse"].get("title", page)
    rows = parse_hero_table(html)

    tot_pick = sum(r["pick"] or 0 for r in rows)
    tot_ban = sum(r["ban"] or 0 for r in rows)
    payload = {
        "page": page,
        "title": title,
        "heroes": len(rows),
        "total_picks": tot_pick,
        "total_bans": tot_ban,
        "games_from_picks": tot_pick / 10.0,
        "games_from_bans": tot_ban / 10.0,
        "rows": rows,
    }
    io.open(outfile, "w", encoding="utf-8").write(json.dumps(payload, indent=1))
    print("page        :", page)
    print("title       :", title)
    print("heroes      :", len(rows))
    print("total picks :", tot_pick, "-> games", tot_pick / 10.0)
    print("total bans  :", tot_ban, "-> games", tot_ban / 10.0)
    print("top 5       :", json.dumps(rows[:5], ensure_ascii=False))


if __name__ == "__main__":
    import urllib.parse
    main()
