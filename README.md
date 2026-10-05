# Mobile Legends Drafting

### ▶ **[Open the draft assistant](https://csrushrush-stack.github.io/mobile-legends-drafting/)**

A draft assistant for Mobile Legends: Bang Bang tournament play. Pick your side, enter the draft as it
happens, and get recommendations driven by real professional match data — then a full game plan once both
teams are locked.

Runs entirely in the browser. No install, no account, no server — and it works offline once loaded.
Works on desktop and phone. On mobile the board and the draft are two tabs with a fixed bottom bar, and the
hero pool sits directly under the recommendations so picks and heroes are in one place.

A **Show more** button under the recommendations reveals further down the ranked list.

---

## What it does

### 1. Live draft recommendations

Follows the standard MLBB tournament draft order: 10 bans and 10 picks across two phases.

```
Phase 1 bans   B · R · B · R · B · R
Phase 1 picks  B1 → R1 → R2 → B2 → B3 → R3
Phase 2 bans   R · B · R · B
Phase 2 picks  R4 → B4 → B5 → R5
```

Tell it whether you are blue or red, then click heroes as they are picked or banned. On your turn it shows
the best options; on the enemy's turn it shows what they are likely to take.

**The draft order changes with the data source.** `Ranked + All` switches to the real ranked format —
**10 bans, five per team, in two blind rounds**:

| Phase | Order | Visibility |
|---|---|---|
| Round 1 | blue bans 3 → red bans 3 | each side is blind to the other's three until the round ends |
| Round 2 | blue bans 2 → red bans 2 | the enemy's pair is revealed only when picks begin |
| Picks | **B1 → R2 → B2 → R2 → B2 → R1** | all 10 bans are public by now |

Bans are **grouped, not alternating** — blue places all three of its round-1 bans before red starts.

**The same hero may be banned by both teams.** Because each side is blind inside a round, blue and red
can both ban the same hero; it only becomes visible when the round is revealed. Duplicate bans are
marked `DUPE BAN` on both rows.

While the ban phase is running, a hero you have banned stays in the pick pool — in ranked a ban never
removes a hero for the *other* side, since they may have banned something else. Heroes leave the pool
once the ban phase ends, or immediately if both sides banned them.

The other two sources use the tournament order (open bans, B1 → R2 → B2 → R1 in two phases).

### 2. Post-draft game plan

Once both teams have five picks, a game plan opens automatically:

- **Comp archetype** for each side, classified from hero traits
- **Strengths** and **weaknesses** derived from the actual picks
- **Macro plan** per side — 0–5 min, 5–12 min, 12 min+, fights, objectives, win condition, and what never to do
- **Verdict** — whether the draft is structurally even or one side has the edge, and why
- **Matchup edges** in both directions from the counter matrix

### 3. Draft rules

Every recommendation follows three priorities, applied in order:

1. **S-tier jungler** — secure a top-tier jungler first
2. **Flex hero** — a hero that plays two or more lanes, so the enemy cannot read your comp
3. **Meta mid or gold** — anchor your damage with a strong mid or gold laner

A panel above the recommendations tracks which rules are satisfied and which one is being prioritised.
The list re-ranks itself to serve the highest unmet rule, then falls back to pure value once all three are done.

The three lists are derived from the data, not hard-coded:

- **S-tier junglers** are ranked on high-rank win rate, ban respect, pick rate, professional record and
  ranked meta, restricted to heroes whose *primary* lane is jungle — so EXP heroes that can flex into the
  jungle do not head the list.
- **Flex heroes** are the 59 heroes with a second genuine pro-play lane.
- **Meta mid/gold** uses the same composite over mid and gold laners.

A *flex hero* is one that can be played in two or more lanes. You pick it early without revealing where it
goes, so the enemy has to guess — Aulus (EXP/Jungle), Gloo (Roam/EXP), Kimmy (Mid/Gold).

Rules only drive **your** recommendations. On the enemy's turn the list answers "what will they take",
so your own priorities are not applied.

### 4. Per-hero metrics

Every recommendation shows:

| Metric | Meaning |
|---|---|
| **Lineup win %** | Pooled pro win rate of your five heroes — how proven the lineup is |
| **vs their lineup** | Matchup estimate against the enemy's five, from the counter matrix |
| **Pro win rate** | The hero's own record in the selected leagues, with sample size |

---

## Data

960 professional games across 7 events:

| League | Games | Heroes tracked |
|---|---|---|
| Asian Games 2026 | 32 | 15 |
| MPL Philippines S17 | 169 | 75 |
| MPL Indonesia S17 | 205 | 83 |
| MPL Malaysia S17 | 164 | 81 |
| MSL Myanmar S4 | 86 | 74 |
| MTC Türkiye S7 | 142 | 15 |
| MCC S7 (CIS / E. Europe) | 162 | 14 |

Plus patch 2.2.16 ranked statistics and a 133-hero counter matrix.

Plus **official Moonton ranked data for the highest tier (Mythical Glory+)**, pulled from the public
endpoint behind mobilelegends.com/rank. This is the publisher's own ranked dataset, not a third-party estimate.

**Three data sources, switchable at the top of the app:**

| Source | What it uses |
|---|---|
| `AG 2026` | The 32-game Asian Games sample only |
| `AG + MPL` | All 960 professional games pooled |
| `Ranked + All` | Official Mythical Glory+ ranked stats **and** the professional dataset |

The high-rank meta is genuinely different from all-ranks. Aulus is 59.7% win / 21.1% ban across all ranks,
but **61.4% win / 69.4% ban** at Mythical Glory+. Use `Ranked + All` when you are drafting for ranked.

Sources: [Liquipedia](https://liquipedia.net/mobilelegends) tournament statistics pages, plus ranked data
aggregators. Game counts were verified by back-solving `bans ÷ ban%` — it returns the same integer for every
hero on a page, so those figures are certain rather than estimated.

---

## Methodology

### Scoring

```
pick = 20×laneOpen − 12×laneTaken
     + 26×measuredSynergy
     + 0.85×matchupEdge
     + 26×adjustedProWinRate
     + 18×rankedMeta
     + balance bonuses (frontline, magic damage, physical damage)

ban  = 24×rankedMeta + 30×beatsYourPicks + 22×fitsEnemyComp
     + 26×adjustedProWinRate + 10×presence + 14×banRate
```

### Three decisions worth explaining

**Lineup win % is pooled, not averaged.** Averaging hero win rates lets a 6–0 hero report a "100% lineup".
The app sums total wins and divides by total picks across the five heroes instead.

**Small samples are shrunk before they are scored.** A hero with a lucky 9-game record would otherwise
outrank a proven 128-game hero. Scoring uses
`(wins + 12×0.5) ÷ (picks + 12)`, which pulls small samples toward 50%. The UI still displays the *raw* win
rate and the sample size — only the ranking uses the adjusted figure, and anything under 15 games is labelled.

**Matchup win % is capped at 30–70%.** It is derived from counter-matrix edges, not measured head-to-head
results, so it is deliberately prevented from making strong claims.

### Measured synergy

Where two heroes actually played together at the 2026 Asian Games, the app shows the real record
(`Nolan + Gloo 4–2`). Where no such pair exists, it says so rather than inventing a number.

---

## Repository layout

```
index.html                redirects to the app (GitHub Pages entry point)
draft_app.html            the app itself
src/
  draft_app_template.html app source with a data placeholder
  build_draft_app.py      injects the dataset into the template
  league_data.py          per-league hero tables — edit here to add a league
  rank_official.json      official Mythical Glory+ ranked stats
  fetch_rank.js           re-pulls the official ranked data
  draft_data.json         generated dataset
reports/
  *.html                  full written analyses (meta, combinations, draft datasheet)
  *.csv                   the underlying tables
```

### Rebuilding

```bash
cd src
python build_draft_app.py     # regenerates ../draft_app.html
```

To add a league, append a dict to `LEAGUES` in `src/league_data.py` with its game count and
`(hero, picks, wins, losses, bans)` rows, then rebuild.

---

## Caveats

- **Small samples.** The Asian Games dataset is 32 games. The same draft can score 64% lineup win rate on
  that sample and 49% on the pooled 960-game data. Small samples flatter — the toggle lets you see both, but
  they are not equally solid.
- **Counter data is ranked-play, not pro-play.** Pro teams exploit counters more consistently than solo queue.
- **Patch-specific.** Hero recommendations reflect patch 2.2.16. The method carries forward; the hero lists
  will not.
- **25 of 133 heroes** have no professional data in any tracked league. They are flagged rather than silently
  scored.

This is an unofficial fan project. Mobile Legends: Bang Bang is a trademark of Moonton.
