# -*- coding: utf-8 -*-
"""Build draft_app.html - MLBB draft assistant with embedded data."""
import csv, json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def load_csv(name):
    with open(os.path.join(OUT, name), encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

STATS = {r["Hero"]: r for r in load_csv("MLBB_S42_hero_stats.csv")}
CTR   = {r["Hero"]: r for r in load_csv("MLBB_S42_counters.csv")}

AG = {"Nolan":(23,11,12,6),"Hirara":(16,12,4,15),"Aulus":(16,11,5,16),"Eudora":(16,10,6,7),
      "Obsidia":(15,9,6,6),"Esmeralda":(14,7,7,8),"Atlas":(13,8,5,19),"Minotaur":(13,8,5,13),
      "Uranus":(13,5,8,12),"Zhuxin":(12,6,6,3),"Gloo":(11,7,4,6),"Paquito":(11,5,6,13),
      "Carmilla":(11,3,8,19),"Belerick":(9,2,7,4),"Valentina":(6,6,0,6)}
AG_GAMES = 32

PAIRS = [
("Nolan","Gloo",6,4,2),("Nolan","Obsidia",6,3,3),("Nolan","Eudora",5,3,2),
("Nolan","Carmilla",5,2,3),("Nolan","Uranus",5,2,3),
("Hirara","Aulus",5,4,1),("Hirara","Gloo",5,3,2),("Hirara","Atlas",4,4,0),
("Hirara","Obsidia",4,4,0),("Hirara","Claude",3,3,0),
("Aulus","Obsidia",5,4,1),("Aulus","Eudora",4,4,0),("Aulus","Minotaur",4,3,1),
("Aulus","Belerick",4,2,2),
("Eudora","Atlas",6,4,2),("Eudora","Paquito",5,3,2),("Eudora","Esmeralda",4,3,1),
("Obsidia","Esmeralda",4,3,1),
("Esmeralda","Atlas",4,2,2),("Esmeralda","Nolan",4,2,2),
("Atlas","Paquito",5,2,3),("Atlas","Obsidia",3,2,1),
("Minotaur","Paquito",4,2,2),("Minotaur","Eudora",3,3,0),("Minotaur","Nolan",3,3,0),
("Minotaur","Valentina",3,3,0),
("Uranus","Zhuxin",5,3,2),("Uranus","Eudora",3,1,2),("Uranus","Paquito",3,0,3),
("Uranus","Hirara",2,2,0),
("Zhuxin","Nolan",4,2,2),("Zhuxin","Hirara",3,3,0),("Zhuxin","Bruno",3,2,1),
("Zhuxin","Esmeralda",3,1,2),
("Gloo","Aulus",3,3,0),("Gloo","Obsidia",3,3,0),("Gloo","Rafaela",2,2,0),
("Carmilla","Cecilion",6,2,4),("Carmilla","Bruno",3,0,3),("Carmilla","Gloo",2,1,1),
("Carmilla","Minotaur",2,1,1),
("Belerick","Eudora",3,1,2),("Belerick","Nolan",3,0,3),("Belerick","Esmeralda",2,1,1),
("Belerick","Obsidia",2,1,1),
("Valentina","Aulus",3,3,0),("Valentina","Minotaur",3,3,0),("Valentina","Claude",2,2,0),
("Valentina","Esmeralda",2,2,0),("Valentina","Hirara",2,2,0),
]

LANE = {
 "Aulus":"EXP","Esmeralda":"EXP","Paquito":"EXP","Arlott":"EXP","Barats":"EXP","Uranus":"EXP",
 "Alice":"EXP","Ruby":"EXP","Masha":"EXP","Yu Zhong":"EXP","Lukas":"EXP","Badang":"EXP",
 "Guinevere":"EXP","Dyrroth":"EXP","Terizla":"EXP","Freya":"EXP","Hilda":"EXP","Chou":"EXP",
 "Aldous":"EXP","Sun":"EXP","Zilong":"EXP","Alpha":"EXP","X.Borg":"EXP","Thamuz":"EXP",
 "Khaleed":"EXP","Phoveus":"EXP","Silvanna":"EXP","Leomord":"EXP","Martis":"EXP","Jawhead":"EXP",
 "Balmond":"EXP","Edith":"EXP","Gatotkaca":"EXP","Yin":"EXP","Roger":"EXP",
 "Nolan":"Jungle","Hirara":"Jungle","Hayabusa":"Jungle","Fanny":"Jungle","Suyou":"Jungle",
 "Harley":"Jungle","Sora":"Jungle","Lancelot":"Jungle","Ling":"Jungle","Joy":"Jungle",
 "Fredrinn":"Jungle","Julian":"Jungle","Bane":"Jungle","Baxia":"Jungle","Akai":"Jungle",
 "Granger":"Jungle",
 "Eudora":"Mid","Zhuxin":"Mid","Yve":"Mid","Lylia":"Mid","Novaria":"Mid","Cecilion":"Mid",
 "Valentina":"Mid","Vexana":"Mid","Lunox":"Mid","Gord":"Mid","Odette":"Mid","Harith":"Mid",
 "Selena":"Mid","Xavier":"Mid","Pharsa":"Mid","Kagura":"Mid","Cyclops":"Mid","Vale":"Mid",
 "Aurora":"Mid","Zetian":"Mid","Luo Yi":"Mid","Zhask":"Mid","Chang'e":"Mid","Valir":"Mid",
 "Faramis":"Mid","Nana":"Mid","Aamon":"Mid","Kadita":"Mid",
 "Brody":"Gold","Claude":"Gold","Moskov":"Gold","Miya":"Gold","Bruno":"Gold","Clint":"Gold",
 "Obsidia":"Gold","Karrie":"Gold","Melissa":"Gold","Beatrix":"Gold","Irithel":"Gold",
 "Wanwan":"Gold","Layla":"Gold","Lesley":"Gold","Natan":"Gold","Yi Sun-shin":"Gold",
 "Ixia":"Gold","Popol and Kupa":"Gold","Kimmy":"Gold",
 "Gloo":"Roam","Atlas":"Roam","Minotaur":"Roam","Carmilla":"Roam","Belerick":"Roam",
 "Rafaela":"Roam","Angela":"Roam","Chip":"Roam","Mathilda":"Roam","Kalea":"Roam",
 "Marcel":"Roam","Tigreal":"Roam","Khufra":"Roam","Lolita":"Roam","Franco":"Roam",
 "Hylos":"Roam","Diggie":"Roam","Estes":"Roam","Floryn":"Roam","Johnson":"Roam",
 "Kaja":"Roam","Minsitthar":"Roam",
}
MAGIC = {"Eudora","Zhuxin","Yve","Lylia","Novaria","Cecilion","Valentina","Vexana","Lunox",
 "Gord","Odette","Harith","Selena","Xavier","Pharsa","Kagura","Cyclops","Vale","Aurora",
 "Zetian","Luo Yi","Zhask","Chang'e","Valir","Faramis","Nana","Kadita","Alice","Esmeralda",
 "Gloo","Atlas","Belerick","Rafaela","Angela","Chip","Mathilda","Kalea","Marcel","Diggie",
 "Estes","Floryn","Kimmy","Bane","Hylos","Gatotkaca","Barats","Uranus","Khufra","Johnson"}

MAXBAN = max(float(r["BanRate%"]) for r in STATS.values()) or 1.0

# ---------------------------------------------------------------- trait tags
TANKY = set("""Gloo Atlas Minotaur Belerick Tigreal Khufra Lolita Hylos Franco Gatotkaca
Johnson Baxia Akai Edith Chip Carmilla Minsitthar Barats Uranus Hilda Terizla Yu Zhong Alice
Esmeralda Balmond X.Borg Thamuz Ruby Grock Jawhead Alpha Silvanna Leomord Masha Fredrinn Kaja
Belerick Argus Sun""".split())
# Reliable engage/lockdown CC only. Deliberately excludes marksmen and assassins whose
# CC is incidental (Bruno ult, Moskov push) - counting those inflates the CC trait and
# misclassifies every comp as "Setup + AOE".
HARDCC = set("""Atlas Tigreal Khufra Franco Lolita Minotaur Johnson Gatotkaca Baxia Akai Hylos
Edith Chip Carmilla Minsitthar Barats Hilda Terizla Yu Zhong Balmond Ruby Chou Paquito
Badang Arlott Guinevere Eudora Aurora Vale Kadita Selena Lylia Vexana Valentina Kagura
Cyclops Zetian Luo Yi Nana Kaja Bane Sun Silvanna Leomord Martis Freya Yin Masha Grock
Belerick Alpha Jawhead Phoveus Khaleed Lukas Cici Sora Gloo Kalea Fredrinn Lapu-Lapu
Zilong Belerick Silvanna Khufra Aurora""".split())
SUSTAIN = set("""Estes Angela Floryn Rafaela Minotaur Carmilla Faramis Kalea Diggie Uranus Aulus
Yu Zhong Esmeralda Alice Ruby Fredrinn Alpha Balmond Belerick Hylos Masha Thamuz Phoveus
Terizla Barats Argus Sun Khufra Gatotkaca""".split())
DIVE = set("""Nolan Ling Hayabusa Fanny Lancelot Gusion Harley Suyou Joy Benedetta Julian Yin
Aamon Natalia Helcurt Karina Saber Arlott Paquito Badang Chou Masha Aldous Lapu-Lapu Yu Zhong
Freya Martis Leomord Dyrroth Guinevere Alpha Hilda Jawhead Khaleed Roger Benedetta Hirara""".split())
POKE = set("""Yve Pharsa Novaria Xavier Zhuxin Cecilion Gord Lylia Valir Brody Clint Kimmy
Lesley Layla Natan Beatrix Ixia Chang'e Nana Zhask Vale Selena""".split())
EARLY = set("""Nolan Fanny Ling Hayabusa Lancelot Gusion Harley Kimmy Paquito Badang Chou Masha
Hilda Balmond Jawhead Saber Karina Natalia Helcurt Aamon Benedetta Joy Suyou Brody Harith
Granger Popol and Kupa Khaleed Dyrroth Yu Zhong Martis Alpha""".split())
LATE = set("""Cecilion Aldous Melissa Moskov Miya Layla Wanwan Claude Alice Esmeralda Uranus
Valentina Irithel Karrie Natan Aulus Yu Zhong Thamuz Terizla Argus Silvanna Sun Lesley Beatrix
Ixia Lunox Gord Yve Pharsa Novaria Xavier Zhuxin Vexana Kagura Kadita Balmond Roger Barats""".split())
SPLIT = set("Masha Sun Zilong Aldous Chou Ling Hayabusa Fanny Argus Freya".split())
AOE = set("""Eudora Cecilion Gord Lylia Vexana Pharsa Yve Atlas Tigreal Khufra Kadita Aurora
Vale Valir Zhask Novaria Xavier Atlas Johnson Grock Yve Selena Kagura Lunox Odette Nana Zhuxin""".split())
PROTECT = set("Lolita Angela Chip Rafaela Edith Diggie Khufra Estes Floryn Carmilla Kalea Mathilda".split())
MOBILE = set("""Nolan Ling Hayabusa Fanny Lancelot Gusion Harley Suyou Joy Benedetta Julian Yin
Natalia Helcurt Karina Saber Chou Masha Aldous Paquito Badang Arlott Mathilda Chip Angela Ling
Lancelot Yi Sun-shin Claude Wanwan Harith Kimmy Benedetta Hirara Zetian Kalea""".split())
CARRIES = set("""Obsidia Claude Moskov Miya Bruno Clint Brody Beatrix Melissa Irithel Karrie
Wanwan Layla Lesley Natan Ixia Popol and Kupa Yi Sun-shin Kimmy Granger""".split())

TAGSETS = dict(tanky=TANKY, hardCC=HARDCC, sustain=SUSTAIN, dive=DIVE, poke=POKE,
               early=EARLY, late=LATE, split=SPLIT, aoe=AOE, protect=PROTECT,
               mobile=MOBILE, carry=CARRIES)

from league_data import LEAGUES

# ---- Official Moonton ranked stats, highest tier (Mythical Glory+) -----------
# Pulled from the public endpoint behind mobilelegends.com/rank with bigrank=9.
# This is the publisher's own ranked data, not a third-party estimate.
RANKED_OFFICIAL, RANKED_META = {}, {}
try:
    with open(os.path.join(OUT, "rank_official.json"), encoding="utf-8") as f:
        _rk = json.load(f)
    RANKED_OFFICIAL = {r["name"]: r for r in _rk.get("mt0", [])}
    RANKED_META = _rk.get("_meta", {})
except Exception:
    RANKED_OFFICIAL = {}

# ---------------------------------------------- multi-lane (flex) assignments
# A hero is a FLEX pick when it can be played in two or more different lanes.
# Only lanes that are a genuine pro-play option are listed.
EXTRA_LANES = {
 "Uranus":["Roam"], "Edith":["Roam"], "Gloo":["EXP"], "Lukas":["Jungle"],
 "Barats":["Jungle"], "Paquito":["Jungle"], "Fredrinn":["EXP"], "Yi Sun-shin":["Jungle"],
 "Kimmy":["Gold"], "Selena":["Roam"], "Kadita":["Roam"], "Esmeralda":["Mid"],
 "Alice":["Mid"], "Ruby":["Roam"], "Akai":["Roam"], "Hylos":["EXP"],
 "Belerick":["EXP"], "Gatotkaca":["Roam"], "Kalea":["EXP"], "Chip":["EXP"],
 "Faramis":["Mid"], "Masha":["Jungle"], "Guinevere":["Mid"], "Chou":["Roam"],
 "Jawhead":["Roam"], "Silvanna":["Mid"], "Terizla":["Roam"], "Julian":["Mid"],
 "Harley":["Mid"], "Joy":["EXP"], "Benedetta":["Jungle"], "Arlott":["Jungle"],
 "Suyou":["EXP"], "Grock":["EXP"], "Baxia":["Roam"], "Hilda":["Roam"],
 "Minsitthar":["EXP"], "Aulus":["Jungle"], "Sun":["Jungle"], "Aldous":["Jungle"],
 "Zilong":["Jungle"], "Yin":["Jungle"], "Roger":["Jungle","Gold"], "Alpha":["Jungle"],
 "Dyrroth":["Jungle"], "Thamuz":["Jungle"], "X.Borg":["Jungle"], "Leomord":["Jungle"],
 "Martis":["Jungle"], "Freya":["Jungle"], "Lapu-Lapu":["Jungle"], "Cyclops":["Jungle"],
 "Nana":["Roam"], "Badang":["Roam"], "Khaleed":["Roam"], "Phoveus":["Roam"],
 "Bane":["EXP"], "Granger":["Jungle"], "Yi Sun-shin ":["Jungle"],
 "Valentina":["Roam"], "Cecilion":["Roam"], "Pharsa":["Roam"], "Yve":["Roam"],
 "Natalia":["Gold"], "Melissa":["Mid"], "Ixia":["Mid"], "Layla":["Mid"],
}

def lanes_of(name):
    base = LANE.get(name, "Flex")
    out = [base] if base != "Flex" else []
    for l in EXTRA_LANES.get(name, []):
        if l not in out:
            out.append(l)
    return out or ["Flex"]

def norm(v, lo, hi):
    if v is None: return 0.5
    return max(0.0, min(1.0, (v - lo) / (hi - lo)))

HEROES = []
for name, s in STATS.items():
    lane = LANE.get(name, "Flex")
    tags = [t for t, st in TAGSETS.items() if name in st]

    per = {}
    for lg in LEAGUES:
        for row in lg["rows"]:
            if row[0] != name:
                continue
            if len(row) == 4:                      # (hero, picks, wr%, bans)
                _, picks, wrp, bans = row
                wins = round(picks * wrp / 100)
                losses = picks - wins
            else:                                  # (hero, picks, wins, losses, bans)
                _, picks, wins, losses, bans = row
            per[lg["id"]] = dict(picks=picks, wins=wins, losses=losses, bans=bans,
                                 wr=round(wins / picks * 100, 2) if picks else None,
                                 presence=round((picks + bans) / lg["games"] * 100, 2))
            break

    def agg(ids):
        p = w = b = 0; g = 0; n = 0
        for i in ids:
            d = per.get(i)
            if not d:
                continue
            p += d["picks"]; w += d["wins"]; b += d["bans"]
            g += next(x["games"] for x in LEAGUES if x["id"] == i)
            n += 1
        if not p:
            return None
        return dict(picks=p, wins=w, losses=p - w, bans=b, leagues=n,
                    wr=round(w / p * 100, 2), presence=round((p + b) / g * 100, 2) if g else 0)

    rk = RANKED_OFFICIAL.get(name)
    lanes = lanes_of(name)
    HEROES.append(dict(
        name=name, lane=lane, lanes=lanes, flex=len(lanes) >= 2,
        meta=float(s["RankedMetaScore"] or 0),
        ban=float(s["BanRate%"] or 0),
        tier=s["Tier"],
        magic=name in MAGIC,
        tags=tags,
        ag=per.get("ag"),
        all=agg([x["id"] for x in LEAGUES]),
        rk=dict(win=rk["win"], pick=rk["pick"], ban=rk["ban"]) if rk else None,
        per={k: v for k, v in per.items()},
        beats=[x.strip() for x in (CTR.get(name, {}).get("StrongAgainst") or "").split(";") if x.strip()],
        ctrBy=[x.strip() for x in (CTR.get(name, {}).get("CounteredBy") or "").split(";") if x.strip()],
    ))
HEROES.sort(key=lambda h: h["name"])

# ------------------------------------------------ S-tier junglers, derived from data
# Rank junglers on high-rank win rate, high-rank ban respect, pick rate, pro record and meta.
# Pick rate is included so a rarely-played hero with a flattering win rate does not top a
# list that is meant to describe the actual meta.
for h in HEROES:
    h["jscore"] = round(
        0.28 * norm(h["rk"]["win"] if h["rk"] else None, 45, 62) +
        0.24 * norm(h["rk"]["ban"] if h["rk"] else None, 0, 100) +
        0.16 * norm(h["rk"]["pick"] if h["rk"] else None, 0, 2.5) +
        0.16 * norm(h["all"]["wr"] if h["all"] else None, 40, 65) +
        0.16 * (h["meta"] / 100.0), 4)

# "Jungler" means the hero's PRIMARY lane is jungle. Heroes that merely flex into the
# jungle (Aulus, Masha, Paquito) are EXP picks and should not head a jungler list.
JUNGLERS = sorted([h for h in HEROES if h["lane"] == "Jungle"], key=lambda h: -h["jscore"])
S_JUNGLERS = [h["name"] for h in JUNGLERS[:5]]

# Meta mid or gold: primary lane is mid or gold, ranked on the same composite.
MIDGOLD = sorted([h for h in HEROES if h["lane"] in ("Mid", "Gold")], key=lambda h: -h["jscore"])
META_MIDGOLD = [h["name"] for h in MIDGOLD[:10]]

FLEXES = sorted([h["name"] for h in HEROES if h["flex"]])
S_FLEX = [h["name"] for h in sorted([h for h in HEROES if h["flex"]], key=lambda h: -h["jscore"])[:8]]

DATA = dict(
    heroes=HEROES,
    pairs={"%s|%s" % (a, b): [g, w] for a, b, g, w, l in PAIRS},
    maxBan=MAXBAN,
    rankedMeta=RANKED_META,
    sJunglers=S_JUNGLERS,
    metaMidGold=META_MIDGOLD,
    flexCount=len(FLEXES),
    leagues=[dict(id=x["id"], name=x["name"], short=x["short"], region=x["region"],
                  games=x["games"], note=x["note"], heroes=len(x["rows"])) for x in LEAGUES],
)

with open(os.path.join(OUT, "draft_data.json"), "w", encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, separators=(",", ":"))

with open(os.path.join(OUT, "draft_app_template.html"), encoding="utf-8") as f:
    html = f.read()
html = html.replace("/*__DRAFT_DATA__*/null", json.dumps(DATA, ensure_ascii=False, separators=(",", ":")))
with open(os.path.join(OUT, "draft_app.html"), "w", encoding="utf-8") as f:
    f.write(html)

print("heroes:", len(HEROES), "| pairs:", len(PAIRS), "| json KB:", round(len(json.dumps(DATA))/1024, 1))
print("flex heroes:", len(FLEXES))
print("S-tier junglers:", S_JUNGLERS)
print("meta mid/gold:", META_MIDGOLD)
print("S-tier flex:", S_FLEX)
print("top junglers by score:")
for h in JUNGLERS[:6]:
    rk = h["rk"] or {}
    print("   %-14s score %.3f  rankWR %s  rankBan %s"
          % (h["name"], h["jscore"], rk.get("win"), rk.get("ban")))
print("top mid/gold by score:")
for h in MIDGOLD[:8]:
    rk = h["rk"] or {}
    print("   %-14s %-6s score %.3f  rankWR %s  rankBan %s  meta %.0f"
          % (h["name"], h["lane"], h["jscore"], rk.get("win"), rk.get("ban"), h["meta"]))
