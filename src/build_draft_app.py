# -*- coding: utf-8 -*-
"""Build draft_app.html - MLBB draft assistant with embedded data."""
import csv, json, os, math

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
 "Alucard":"EXP","Argus":"EXP","Cici":"EXP","Lapu-Lapu":"EXP","Benedetta":"EXP",
 "Nolan":"Jungle","Hirara":"Jungle","Hayabusa":"Jungle","Fanny":"Jungle","Suyou":"Jungle",
 "Harley":"Jungle","Sora":"Jungle","Lancelot":"Jungle","Ling":"Jungle","Joy":"Jungle",
 "Fredrinn":"Jungle","Julian":"Jungle","Bane":"Jungle","Baxia":"Jungle","Akai":"Jungle",
 "Gusion":"Jungle","Hanzo":"Jungle","Helcurt":"Jungle","Karina":"Jungle",
 "Natalia":"Jungle","Saber":"Jungle","Aamon":"Jungle",
 "Eudora":"Mid","Zhuxin":"Mid","Yve":"Mid","Lylia":"Mid","Novaria":"Mid","Cecilion":"Mid",
 "Valentina":"Mid","Vexana":"Mid","Lunox":"Mid","Gord":"Mid","Odette":"Mid","Harith":"Mid",
 "Selena":"Mid","Xavier":"Mid","Pharsa":"Mid","Kagura":"Mid","Cyclops":"Mid","Vale":"Mid",
 "Aurora":"Mid","Zetian":"Mid","Luo Yi":"Mid","Zhask":"Mid","Chang'e":"Mid","Valir":"Mid",
 "Faramis":"Mid","Nana":"Mid","Kadita":"Mid",
 "Brody":"Gold","Claude":"Gold","Moskov":"Gold","Miya":"Gold","Bruno":"Gold","Clint":"Gold",
 "Obsidia":"Gold","Karrie":"Gold","Melissa":"Gold","Beatrix":"Gold","Irithel":"Gold",
 "Wanwan":"Gold","Layla":"Gold","Lesley":"Gold","Natan":"Gold","Yi Sun-shin":"Gold",
 "Ixia":"Gold","Popol and Kupa":"Gold","Kimmy":"Gold","Hanabi":"Gold","Granger":"Gold","Grock":"Roam",
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
 "Bane":["EXP"], "Granger":["Jungle"],
 "Valentina":["Roam"], "Cecilion":["Roam"], "Pharsa":["Roam"], "Yve":["Roam"],
 "Kimmy":["Mid","Jungle"], "Natalia":["Gold"], "Ixia":["Mid"],
}

# ============================================================================
# USER TIER LIST - authoritative.
# These are the heroes the player rates as usable in the current meta, by lane.
# They drive the draft rules, flex detection and lane coverage.
# The data-derived tier is kept alongside as `tierNow` for comparison, but it is
# NOT used for recommendations: ranked ban rate measures the ranked ladder, not
# tournament priority, and the two disagree sharply (Claude has a 0.07% ranked
# ban rate but was picked in 52% of all 960 professional games).
# ============================================================================
USER_TIERS = {
 "EXP":    ["Aulus","Freya","Uranus","Carmilla","Barats","Gatotkaca","Esmeralda",
            "Minotaur","Sora","Masha","Atlas"],
 "Roam":   ["Belerick","Masha","Atlas","Gloo","Minotaur","Rafaela","Estes","Carmilla",
            "Gatotkaca","Kaja","Marcel"],
 "Mid":    ["Zhuxin","Eudora","Selena","Zetian","Novaria"],
 "Jungle": ["Nolan","Hirara","Harley","Aulus","Lukas","Paquito","Fanny"],
 "Gold":   ["Obsidia","Freya","Aulus","Clint","Brody","Paquito","Claude","Moskov","Miya"],
}

USER_LANES = {}
for _L, _names in USER_TIERS.items():
    for _n in _names:
        USER_LANES.setdefault(_n, []).append(_L)

# ---------------------------------------------- "can cover" assignments
# A hero can COVER a lane without it being its primary role: it is a genuine
# option there, but it is not what the hero is. The distinction matters in the
# draft - a roam who can cover EXP fills the slot, but you would still rather
# have a real EXP hero, so it scores as a filler rather than a natural fit.
# Player-confirmed: Atlas and Carmilla cover EXP + Roam; Rafaela covers Mid + Roam.
COVER = {
 "Atlas":    ["EXP"],
 "Carmilla": ["EXP"],
 "Rafaela":  ["Mid"],
}

# ---------------------------------------------- measured lane overrides
# LANE above is a hand-written guess. lane_roles.py carries the real thing:
# which lane each hero was actually fielded in, taken from the player's roster
# role on mldb.gg across every MPL PH S18 game. Where that evidence is thick
# enough it wins, because it is measurement rather than opinion - it is what
# showed Paquito is a jungler/gold pick, not the EXP hero this table claimed.
try:
    from lane_roles import MEASURED, MIN_N as MEASURED_MIN_N
except Exception:                                    # file absent: stay hand-coded
    MEASURED, MEASURED_MIN_N = {}, 6

# These three are modelled as roam-primary heroes that COVER another lane. Their
# measured splits are close to even (48-61% roam), so measurement alone would
# flip them and erase the cover distinction the draft logic is built on.
PRIMARY_LOCKED = {"Atlas", "Carmilla", "Rafaela"}


def primary_lane(name):
    m = MEASURED.get(name)
    if m and m["n"] >= MEASURED_MIN_N and name not in PRIMARY_LOCKED:
        return m["primary"]
    return LANE.get(name, "Flex")


def lanes_of(name):
    base = primary_lane(name)
    out = [base] if base != "Flex" else []
    measured = (MEASURED.get(name) or {}).get("lanes") or []
    for l in measured + EXTRA_LANES.get(name, []) + USER_LANES.get(name, []) + COVER.get(name, []):
        if l not in out:
            out.append(l)
    return out or ["Flex"]

HEROES = []
for name, s in STATS.items():
    lane = primary_lane(name)
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
    primary = primary_lane(name)
    measured = MEASURED.get(name) or {}
    cover = [l for l in COVER.get(name, []) if l != primary]
    # FLEX means the hero has a second lane that is a real drafting option.
    # A mere cover (a roam who can hold EXP) is not flex - it is a filler.
    flex_lanes = [l for l in lanes if l != primary and l not in cover]
    HEROES.append(dict(
        name=name, lane=primary, lanes=lanes, cover=cover, flex=len(flex_lanes) >= 1,
        ls=measured.get("share") or None,      # measured lane split, when we have it
        ln=measured.get("n") or 0,
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

# ------------------------------------------------ no tiers
# The app no longer grades heroes. Tier letters told you nothing about whether
# picking a hero would win the game, and the ban-rate proxy behind them read the
# ranked ladder rather than the tournament the player is drafting for. Every
# recommendation is now scored directly on the current dataset - win rate,
# presence, and the matchup against what the enemy has actually locked.
#
# The three draft rules also read the live dataset at runtime (see topLane() in
# the template), so they follow the meta instead of a fixed list.
FLEXES = sorted([h["name"] for h in HEROES if h["flex"]])


DATA = dict(
    heroes=HEROES,
    pairs={"%s|%s" % (a, b): [g, w] for a, b, g, w, l in PAIRS},
    rankedMeta=RANKED_META,
    flexCount=len(FLEXES),
    leagues=[dict(id=x["id"], name=x["name"], short=x["short"], region=x["region"],
                  games=x["games"], note=x["note"], heroes=len(x["rows"])) for x in LEAGUES],
)

with open(os.path.join(OUT, "draft_data.json"), "w", encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, separators=(",", ":"))

with open(os.path.join(OUT, "draft_app_template.html"), encoding="utf-8") as f:
    html = f.read()
# The "where the data comes from" panel quotes live game counts. Fill them from
# the dataset so the copy can never drift out of sync with the tables again.
_GL = {x["id"]: x["games"] for x in LEAGUES}
for _tok, _val in (
    ("__AG_GAMES__", _GL["ag"]),
    ("__PH_GAMES__", _GL["ph"]),
    ("__ID_GAMES__", _GL["id"]),
    ("__MM_GAMES__", _GL["mm"]),
    ("__MPL_TOTAL__", _GL["ph"] + _GL["id"] + _GL["mm"]),
    ("__ALL_TOTAL__", sum(_GL.values())),
):
    html = html.replace(_tok, str(_val))
html = html.replace("/*__DRAFT_DATA__*/null", json.dumps(DATA, ensure_ascii=False, separators=(",", ":")))
with open(os.path.join(OUT, "draft_app.html"), "w", encoding="utf-8") as f:
    f.write(html)

print("heroes:", len(HEROES), "| pairs:", len(PAIRS), "| json KB:", round(len(json.dumps(DATA))/1024, 1))
print("flex heroes:", len(FLEXES))
print("no tiers: candidates are ranked on the live dataset at runtime")


# Sanity check - what the draft rules will surface, using the same formula the
# app applies to the currently selected dataset.
def rule_score(h, lanes):
    d = h.get("all")
    if not d or h["lane"] not in lanes or d["picks"] < 10:
        return None
    conf = min(1.0, d["picks"] / 30.0)
    adj = (d["wins"] + 12 * 0.5) / (d["picks"] + 12) * 100.0     # shrink like the app
    return (adj - 50) * 2.4 * (0.4 + 0.6 * conf) + min(1.0, d["presence"] / 100.0) * 16


for label, lanes in (("top junglers", {"Jungle"}), ("top mid/gold", {"Mid", "Gold"})):
    rows = [(rule_score(h, lanes), h) for h in HEROES]
    rows = [(s, h) for s, h in rows if s is not None]
    rows.sort(key=lambda x: -x[0])
    print("%s - by the app's rule formula:" % label)
    for s, h in rows[:6]:
        d = h["all"]
        print("   %-14s %-6s score %6.2f   WR %5.1f%%   presence %5.1f%%   n%d"
              % (h["name"], h["lane"], s, d["wr"], d["presence"], d["picks"]))
