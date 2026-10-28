# S0. LEAD policy: dev sniping, first behind the bundle

In short: the project started by testing the "rugger sniping" method of three French videos: buy a rugger's coin in
its creation block and sell at +100%. Validation on Oct 12-14 data found that method loses (-10.5% a trade on the
test split, -21.1% on a holdout) (docs/04 §1). One variant survived on history: the LEAD, a rank-1 micro-scalp that
buys first behind the dev's bundle in the creation slot and sells within 1-3 s (+3.5% a trade pooled out of sample)
(docs/04 §0). Run live as a probe on Oct 21-23, it lost -4.856 SOL over 469 attempts (docs/10 §1). Replaced on Oct 23
by the operator wave (S1); its rebuild (S2) was shelved. This page is background for the strategies built on him.

| | |
|---|---|
| Status | ran live as a probe Oct 21-23 (stages A and B), lost; replaced by S1 on Oct 23; rebuilt as S2, shelved |
| Built from | not from him: the videos' method (docs/00 §4), re-tested. S1 later reuses its entry, which matches his rule 1 (first behind the bundle) in [his rules](../02-his-rules/README.md) |
| Code | [`config/paper-lead.example.toml`](../config/paper-lead.example.toml) (shadow mode), [`config/probe-a.example.toml`](../config/probe-a.example.toml); entry bound and bundle park in `crates/rugsnipe/src/hot.rs` (`hot::entry_v_cap`, `hot::park_trade`, docs/06 §7.1); paper E1 lane `crates/rugsnipe/src/e1.rs`; test `crates/rugsnipe/tests/entry_bound.rs` |
| Config keys | `exit.default.tp = [[1.15, 1.0]]`, `exit.default.insider_sell = "bundle"`, `exit.default.no_activity_ms = 1000`, `exit.default.phantom_sl = {after_ms = 1000, drop = 0.15}`, `exit.default.max_hold_slots = 5`, `entry.max_premium = 0.02`, `entry.filter = "multi_bundle"`, `entry.filter_model`, `entry.filter_mode`, `risk.max_snipe_lamports`, `bid.split.bam`, `probe.stage` (docs/04 §6); `entry.require_bundle` (docs/08 §9 config table, 2026-10-22); `paper.fill_model = "e1"` (docs/04 §7) |
| Source docs | [docs/00](../docs/00-transcript-digest.md) §1, §4-6; [docs/01](../docs/01-claims-verification.md) C4, C6, C13, C24; [docs/04](../docs/04-strategy.md) §0-7; [docs/05](../docs/05-validation.md) §2-5 |
| Research | [`docs/research/`](../docs/research/) (gap-1..6, strategy-*.md); [`analysis/scripts/gap1`](../analysis/scripts/gap1), [`gap3_exits`](../analysis/scripts/gap3_exits), [`gap4`](../analysis/scripts/gap4); [`analysis/scripts/strategy/`](../analysis/scripts/strategy/) (`orchestrator_checks.py`, `critic_realistic.py`); [`data/reports/strategy/`](../data/reports/strategy/) (`critic_realistic.json`, `entry_filter_v1.json`); [`analysis/rugsnipe_analysis/strategy/pnl_model.py`](../analysis/rugsnipe_analysis/strategy/pnl_model.py) |

Words: a **create** is the transaction that launches a coin; a **slot** is one Solana block, about 200 ms since Oct 9
(docs/01 C6); the **curve** is pump.fun's bonding curve, the price formula a coin trades on before it graduates; a
**bundle** is the creator's own buys packed right behind the create; an **operator** is whoever runs a series of
launches; a **tip** pays the block producer or relay; the **premium** is what we pay over the post-bundle price; a
**tape** is a coin's full trade list; **out of sample** means scored on data the rule was not chosen on; **paper** and
**shadow** mean simulated fills with no money; a **probe** is a small real-money run to measure landing and costs.

## The rule

**The videos' method** (what he claims, docs/00 §4, §6): find a creator who pumps and dumps repeatedly; buy his next
coin in block 0, right after his bundle; take profit at +100%; no stop (the curve floor is the stop). Arm a rugger only
if 3 or more of his last 10 coins hit +100%, the first candle is at most $15k and the funding is traceable. Stake 5% of
capital. Method 2 copies the rugger's pump wallets (docs/00 §5).

**The LEAD** (docs/04 §2):
1. Universe: SOL-quoted, non-mayhem creates whose creation slot holds a bundle with at least one non-creator wallet.
2. Entry: 0.25-0.5 SOL, landing in the creation slot first behind the bundle; `max_sol_cost` capped at the post-bundle
   price +2%, so a rank-3 fill fails cheaply.
3. Exit at the first of: value +15%; any bundle-wallet sell; 1 s with no trade; -15% stop active after 1 s; a hard exit
   at landing slot + 5.

Median hold 1.6 s; the take-profit fires on 22% of entries at an average +31% (docs/04 §2).

## How it was found

- **Claims check** (docs/01): fees are 1.25% a side, not 1% (C4). At his headline numbers (33% hits, TP +100%, floor
  -80%) the expected value is about -27% of stake per snipe; break-even needs 43-48% hits (C24). Only 6.8% of random
  coins hit +100% from the end of slot 0 (C13).
- **Base rates** (docs/05 §2, random arm n = 396): ATH of 2x the post-slot-0 price on 9.3% of launches, bundled or not.
  The slot-0 wallets of bundled launches sell half their bag after a median 8 s.
- **Competition** (docs/05 §4): professional snipers (78 wallets) make 86% of winning slot-0 buys; bundled launches
  have an independent slot-0 winner 50.9% of the time.
- **Search** (docs/04 §3): stage 1 tried 25,397,064 configurations and nothing survived a multiple-testing correction,
  but it pointed to "block-0 entry, very short exit". Stage 2 searched 659,232 exits on the training split only and
  froze 5 policies at 11:34:40 UTC before a fresh holdout was pulled.

## Backtests

Results are per trade, as the docs give them (no SOL totals except the model row).

| Test | Period | Setting | Result | n | Source |
|---|---|---|---|---|---|
| Naive: buy at end of slot 0, TP 2x | random arm, Oct 12-14 | 0.3 SOL, fees, own impact | -18.6% [-23, -14] | 396 | docs/05 §2 |
| His arming rule, walk-forward | 16-day sample | 3+ of last 10 hit +100% | hit rate 18.6-21.8% out of sample (needs 43-48%) | 50-90 launches/day | docs/05 §5.3; `analysis/scripts/gap1` |
| His rule: TP +100%, no stop | test = last 40% of 675 bundled launches; deep = 133 random, Oct 12-14 | 0.25 SOL, base costs | -10.5% [-13.9, -6.9]; deep -21.1% | 675 / 133 | docs/04 §1 |
| His bot's exits on his rule | same | phantom SL, big-buy sell, idle 10 s | -0.8%; deep -4.6% | same | docs/04 §1 |
| Buy on dev sell / snipe delay | same | TP +100% | -13.1% / -16.9%; deep -22.0% / -28.5% | same | docs/04 §1 |
| LEAD, test split | last 40% by time | 0.5 SOL | +3.5% [+1.4, +5.8] | 200 | docs/04 §3 |
| LEAD, fresh holdout (the clean set) | pulled Oct 14 after the freeze | 0.5 SOL | +3.7% [+0.7, +6.6]; re-implemented +3.67% | 150 | docs/04 §3; `orchestrator_checks.py` |
| LEAD, pooled out of sample | Oct 12-14 | 0.5 SOL | +3.5% [+1.9, +5.2] | 427 | docs/04 §3 |
| LEAD, dense window | Oct 14 02:05-08:05 UTC | base costs | +2.5% [+1.6, +3.4]; quiet -0.9%, busy +9.4% | 915 | docs/04 §3 |
| LEAD, critic's holdout | Oct 14 08:43-13:43 UTC | rank 1 | +3.2% [+1.5, +4.9] | 222 | docs/04 §3 |
| LEAD at rank 2 | same | one sniper ahead | +0.8% | 222 | docs/04 §3 |
| LEAD, combined realistic fills | same | mean premium, 0.01 SOL, 1 in 3 followers fail | -0.4% [-2.0, +1.3] | 222 | docs/04 §3; `critic_realistic.py` |
| LEAD + entry filter, skip bottom tertile | 480 pre-registered launches, Oct 14 | frozen P(TP) | +4.6% against +3.2% plain | 480 | docs/04 §3a; model `data/reports/strategy/entry_filter_v1.json` |
| Per-operator arming on the LEAD | fresh holdout | posterior > 0 | +2.9% armed against +3.2% unarmed | not given | docs/04 §5 |
| Copy-trading pump wallets | 905 fresh launches | one slot late | -7.0% [-9.5, -4.5] | 905 | docs/04 §5 |
| SOL per day (a model, not a measurement) | - | 0.5 SOL, 20% landing, 0.003 SOL per failed attempt | +9.0 SOL/day [-5.0, +20.3] | about 1,150 trades/day | docs/04 §4; `pnl_model.py` |

## Live

- **Probe, Oct 21-23, Frankfurt box (fra1):** 469 attempts, -4.856 SOL from chain SOL deltas, with failed copies of
  0.738 SOL shown in a separate column (docs/10 §1). The per-period table and its causes are on the S2 page.
- **Oct 22, stage B (0.25 SOL):** 145 landed fills, all on bundles averaging 0.79 SOL, against 61 slippage failures, 43
  of them bundles above the fixed 4 SOL bound, averaging 11.5 SOL. The bot was selecting the opposite population from
  the one the LEAD was scored on (docs/06 §7.1). Stage B's first 10 attempts were unbundled and all exited at -2.5%,
  which added `entry.require_bundle` (docs/08 §9 config table).
- **Sells:** at the shipped 50,000 / 200,000 lamport bids, 20 of 43 stage-B positions closed 3 to 8 slots late (docs/08
  §9 config table, `sell_tip_lamports`).
- **Landing by leader** (2026-10-23, 73 attempts): in the create slot 62% of the time with a European leader, 33% North
  American, 9% Asian (docs/08 §9 config table, `entry.leader_regions`).

## Verdict

- **The videos' method: dropped.** It loses on every test (docs/04 §0-1); his profitability rule is wrong (docs/01 E).
- **The LEAD: dropped live.** Its historical edge held only at rank 1 and only where other snipers followed (docs/04
  §3). Re-scored on the live races, the races we actually won lose -2.63% after costs at 0.5 SOL (docs/10 §2).
- **Replaced** on Oct 23 by S1, the operator wave, which keeps the LEAD's entry plumbing (park behind the bundle, bound
  at the post-bundle state) and changes the picks, the premium (0) and the exit (docs/09).

## Open questions

- Do followers follow known rival snipers, or do rivals know which launches will be pushed? (docs/10 §2).
- The entry filter's first clean out-of-sample test was to be shadow mode (docs/04 §3a); no result is reported.
- Everything was to be re-measured after Alpenglow, about Oct 21 (docs/04 §3, §7).

## Sources

- [docs/00-transcript-digest.md](../docs/00-transcript-digest.md), [docs/01-claims-verification.md](../docs/01-claims-verification.md)
- [docs/04-strategy.md](../docs/04-strategy.md), [docs/05-validation.md](../docs/05-validation.md)
- [docs/06-architecture.md](../docs/06-architecture.md) §7.1, [docs/08-runbook.md](../docs/08-runbook.md) §9 config table
- [docs/10-microscalp-v2.md](../docs/10-microscalp-v2.md) §1-2 (the live record)
- [docs/research/](../docs/research/), [analysis/scripts/strategy/](../analysis/scripts/strategy/), [data/reports/strategy/](../data/reports/strategy/)
