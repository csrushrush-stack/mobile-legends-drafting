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

1. **Top-performing jungler** — secure the highest-impact slot with someone who is winning games here
2. **Flex hero** — a hero that plays two or more lanes, so the enemy cannot read your comp
3. **Top-performing mid or gold** — anchor your damage with a laner who is winning games here

A panel above the recommendations tracks which rules are satisfied and which one is being prioritised.
The list re-ranks itself to serve the highest unmet rule, then falls back to pure value once all three are done.

**Which heroes satisfy a rule is read from the dataset you have selected**, not from a fixed list — so the
rules move with the meta. Rule 1 does not name a jungler; it names whoever is actually winning in the
jungle right now. In the current data that is Nolan (59.5% over 131 games) ahead of Fanny and Hirara.

A hero needs at least 10 games in the selected dataset to qualify, so a rule cannot fire on a thin record.
AG 2026 is only 32 games, so it falls back to whoever got played rather than leaving the rule unsatisfiable.

A *flex hero* is one that can be played in two or more lanes. You pick it early without revealing where it
goes, so the enemy has to guess — Aulus (EXP/Jungle), Gloo (Roam/EXP), Kimmy (Mid/Gold).

**Flex is not the same as cover.** Some heroes can *hold* a lane without it being their role — Atlas and
Carmilla are roams that can cover EXP, Rafaela is a roam that can cover Mid. Those are marked `COV` in the
pool, and they score as a **filler**: they fill an open slot, but a true hero of that lane still outscores
them. Cover lanes do not satisfy the flex rule,
because a roam standing in EXP reveals nothing about your comp.

Rules only drive **your** recommendations. On the enemy's turn the list answers "what will they take",
so your own priorities are not applied.

### 4. Per-hero metrics

Every recommendation shows:

| Metric | Meaning |
|---|---|
| **Lineup win %** | Pooled pro win rate of your five heroes — how proven the lineup is |
| **vs their lineup** | Matchup estimate against the enemy's five, from the counter matrix |
| **Win rate over N pro games** | The hero's own record in the selected leagues, with its sample size |
| **Presence · picked · banned** | Picks + bans over games — how contested the hero is |

Every hero card in the pool shows its raw win rate with the sample size and its presence, instead of a
letter grade. A report breaking this down lane by lane is generated as `reports/MLBB_Lane_Review.html`.

---

## Data

410 professional games, and deliberately narrow: **Asian Games 2026 plus the current season of the three
MPL regions this tool drafts for.**

| League | Games | Heroes tracked |
|---|---|---|
| Asian Games 2026 | 32 | 15 |
| MPL Philippines S18 | 128 | 82 |
| MPL Indonesia S18 | 146 | 89 |
| MSL Myanmar S4 | 104 | 77 |

Past MPL seasons and the Malaysia / Türkiye / CIS leagues were **retired, not pooled**. Mixing seasons
blends two patches and double-weights a region in the pooled win rates — a drafting tool should read the
patch being played right now. PH and ID are on S18 (ends 30 Oct 2026); Myanmar is the current MSL S4.

### Keeping it current

`refresh_mpl_data.py` refreshes everything end to end: fetch, validate, rewrite `league_data.py`, rebuild
the app. It runs automatically every Monday morning via a scheduled task, and can be run by hand at any time.

It prefers whichever source is furthest ahead on games played. Liquipedia's MediaWiki API is the baseline —
the rendered pages sit behind a Cloudflare challenge, but `api.php?action=parse&prop=text` is not challenged
and returns the full table including win/loss splits. Where mlbbhub covers the same region and has more
games, it wins: it updates faster (it ran 5 games ahead on PH when this was written) and still exposes
Win/WR, so wins and losses are derivable. Myanmar has no mlbbhub page, so it is Liquipedia only.

Validation runs before anything is written, and a region that fails is **held rather than forced**:
total picks ÷ 10 and total bans ÷ 10 must agree within a margin, and wins + losses must equal picks for
every hero. PH and ID reconcile exactly; Myanmar runs about 2 games light on bans because a few of its
games have no bans recorded, so bans get a proportional margin instead of a hard equality check.

Plus patch 2.2.16 ranked statistics and a 133-hero counter matrix.

Plus **official Moonton ranked data for the highest tier (Mythical Glory+)**, pulled from the public
endpoint behind mobilelegends.com/rank. This is the publisher's own ranked dataset, not a third-party estimate.

**Three data sources, switchable at the top of the app:**

| Source | What it uses |
|---|---|
| `AG 2026` | The 32-game Asian Games sample only |
| `AG + MPL` | All 410 professional games pooled |
| `Ranked + All` | Official Mythical Glory+ ranked stats **and** the professional dataset |

The high-rank meta is genuinely different from all-ranks. Aulus is 59.7% win / 21.1% ban across all ranks,
but **61.4% win / 69.4% ban** at Mythical Glory+. Use `Ranked + All` when you are drafting for ranked.

Sources: [Liquipedia](https://liquipedia.net/mobilelegends) tournament statistics pages, plus ranked data
aggregators. Game counts were verified by back-solving `bans ÷ ban%` — it returns the same integer for every
hero on a page, so those figures are certain rather than estimated.

---

## Methodology

### Scoring

**There are no tiers.** Nothing is graded S, A or B. Every candidate is ranked by one question: does
taking this hero make my team more likely to win the game?

```
pick = 22×laneOpen − 13×laneCover − 14×laneTaken
     + 2.2×(adjustedProWinRate − 50) × confidence
     + 14×presence
     + matchupEdge              (against the enemy's locked picks)
     + 24×measuredSynergy
     + 16×rankedWinRate         (only where that mode is on)
     + balance bonuses          (frontline, magic damage, physical damage)
     + 30 if it satisfies the highest unmet rule

ban  = 2.2×(adjustedProWinRate − 50) × confidence
     + 12×presence
     + 30×beatsYourPicks
     + 22×fitsEnemyComp
     + ranked ban rate and win rate (only where that mode is on)
```

Win rate is scored linearly in percentage points so the arithmetic is legible — every point above 50 is
worth 2.2. There is no composite index anywhere in the scoring: a hero that wins 58% of its games scores
above one that wins 52%, whatever anyone thinks of it.

### Three decisions worth explaining

**Win rate is faded in by sample confidence.** A 6–1 hero is not the same evidence as a 78–53 hero, so the
win-rate term is multiplied by `0.4 + 0.6 × min(1, games ÷ 30)` and small samples are shrunk first. Without
this, Hilda's 85.7% over 7 games outranked Nolan's 59.5% over 131 — which is how the weighting came to exist.

**Lineup win % is pooled, not averaged.** Averaging hero win rates lets a 6–0 hero report a "100% lineup".
The app sums total wins and divides by total picks across the five heroes instead.

**Small samples are shrunk before they are scored.** A hero with a lucky 9-game record would otherwise
outrank a proven 128-game hero. Scoring uses
`(wins + 12×0.5) ÷ (picks + 12)`, which pulls small samples toward 50%. The UI still displays the *raw* win
rate and the sample size — only the ranking uses the adjusted figure, and anything under 15 games is labelled.

**Matchup win % is capped at 30–70%.** It is derived from counter-matrix edges, not measured head-to-head
results, so it is deliberately prevented from making strong claims.

### Measured synergy

Where two heroes actually played together in the selected dataset, the app shows the real record
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
  refresh_mpl_data.py     fetch -> validate -> rewrite -> rebuild, on a weekly schedule
  fetch_liq_stats.py      Liquipedia MediaWiki API client (the Cloudflare workaround)
  verify_roster.py        checks every hero in the tables exists in the roster
  build_lane_review.py    lane-by-lane performance report
  rank_official.json      official Mythical Glory+ ranked stats
  fetch_rank.js           re-pulls the official ranked data
  draft_data.json         generated dataset
reports/
  MLBB_Lane_Review.html   per-lane performance from the current data
  MLBB_lane_performance.csv
  *.html                  full written analyses (meta, combinations, draft datasheet)
  *.csv                   the underlying tables
```

### Rebuilding

```bash
cd src
python build_draft_app.py      # regenerates ../draft_app.html
python build_lane_review.py    # regenerates the lane report
```

To add a league, append a dict to `LEAGUES` in `src/league_data.py` with its game count and
`(hero, picks, wins, losses, bans)` rows, then rebuild. For an MPL region, prefer
`python refresh_mpl_data.py` — it fetches and validates the table for you.

---

## Caveats

- **Small samples.** The Asian Games dataset is 32 games. The same draft can score 64% lineup win rate on
  that sample and 49% on the pooled 410-game data. Small samples flatter — the toggle lets you see both, but
  they are not equally solid.
- **A high pick rate is not a high win rate.** Hirara is the most-picked hero in the current data and wins
  only 47% of her games: she is contested because she is flexible, not because she wins. The app ranks on
  win rate and reports presence separately so the two do not get confused.
- **Counter data is ranked-play, not pro-play.** Pro teams exploit counters more consistently than solo queue.
- **Patch-specific.** Hero recommendations reflect patch 2.2.16. The method carries forward; the hero lists
  will not.
- **25 of 133 heroes** have no professional data in any tracked league. They are flagged rather than silently
  scored.

This is an unofficial fan project. Mobile Legends: Bang Bang is a trademark of Moonton.
