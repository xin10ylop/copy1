# copy1: operator 1, "him" (AHwJSnFN): from discovery to the live copy

Everything about **operator 1, "him"**, `AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2`, the first wallet we copied, in one
place: who he is, his decoded rules, every strategy built on him (rule bots, then the direct copy), every backtest, the
live trades, the code and how it ran. The other copied wallets (3yrJE1A8, JBokzLFR, CxyKYmQo, D5BDDkBt) are here too, as
S7. Wallet 4 (H9kuqGKN) and its long copy are in the **copy2** repo. Both repos carry the same code snapshot
(`xin10ylop/rugsnipe` at `7184554`, Oct 28).

**Agents: read [`CLAUDE.md`](CLAUDE.md) first.**

**Oct 28 review, before any restart: [`07-restart/README.md`](07-restart/README.md).** The copy did not fail, it ran
out of edge: the 125 live fills made +0.83 SOL on the curve and paid 0.88 in tips and fees, and the 5-day backtest's own
last two days give the same per-fill result (its +8.02 was Oct 21-23 and a few coins). Four reviews (the code, the
backtests re-run and extended, the box and the feed, the live copies decomposed), six code fixes with tests, a him-only
config template and a runbook for a measured small restart.

## Where things stand (Oct 28)

- **He is real money:** +151.6 SOL from Sep 24 to Oct 24 on 19 active days, 400-600 trades a day at 0.6-0.8 SOL, about
  half won, held 1-2 s, no withdrawals (docs/12 §1). In check.sh's window he made +8.9099 SOL; Oct 24-28 +31.32 SOL at
  about 30% lower volume. "No linked wallets" holds since Sep 4 only: before that he ran a 232-wallet fleet through
  this wallet and deployed his guard programs himself (01-who-he-is §4, the Oct 28 on-chain re-check).
- **We never made money on him.** The rule bots built from his behaviour (S0-S5) lost or made a fraction of his result:
  the exact replay of the box's rule bot made +1.1 SOL over 2.7 days against his +33.5 (docs/17 §8). The direct copy
  (S6) broke even: **−0.0479 SOL on 162 copies while he made +8.91** (check.sh window). We fill his weaker coins, and his
  better ones move past our 5% bound before we land.
- **Why:** the first spot behind a launch is an auction. He wins it on the coins worth having (median 8.0M bid above 40
  vSOL) and we win it when nobody else wants the coin (docs/17 §3).
- **The copy bot is stopped.** The daily-loss kill hit on Oct 27 07:50 UTC, set off by the **stuck coin 2RR6sfbi** (a
  wallet-4 copy that couldn't be sold, −0.57 SOL). The bot lost −5.13 SOL all time. fra1 was terminated on Oct 28. Nothing
  in this repo is running.

**Known problems, read before trusting any number:**
- **The stuck coin 2RR6sfbi**: the copy bot couldn't sell a coin that graduated in the seconds it held it, and that
  stopped every copy, his included. Fixed in code (`af681ad`), never deployed.
  → [`05-live/stuck-coin-2RR6sfbi.md`](05-live/stuck-coin-2RR6sfbi.md)
- check.sh's "since the start" counts closed trades only (−0.76 while the wallet lost 1.41).
- docs/13's tweet-rule numbers were overstated and are corrected by docs/14. Use the corrected figures.
- The operator-count copy rule may have been off live ("operator he bought < 0 times" in check.sh; S6 open questions).

## A to Z

| Folder | What's in it |
|---|---|
| [`01-who-he-is/`](01-who-he-is/README.md) | how he was found, his month and days, execution (guards, block position, tips, fees, senders), selection layers, operators, weak days, 6anjqMe, **a dated discovery timeline** |
| [`02-his-rules/`](02-his-rules/README.md) | his rules as decoded, one family each (entry, picks, tweet layer, follow layer, hold/exit, sizing, tips and fees): evidence, what the bot implements, whether it held out of sample |
| [`03-strategies/`](03-strategies/README.md) | **S0-S7**, one page each: [S0 LEAD](03-strategies/S0-lead-policy-dev-sniping.md) · [S1 operator wave](03-strategies/S1-operator-wave.md) · [S2 micro-scalp v2](03-strategies/S2-microscalp-v2.md) · [S3 tweet rule](03-strategies/S3-tweet-rule.md) · [S4 big rugs](03-strategies/S4-big-rugs.md) · [S5 follow](03-strategies/S5-follow-bundle-wallets.md) · [**S6 copy him**](03-strategies/S6-copy-him.md) · [S7 other wallets](03-strategies/S7-other-copy-targets.md) |
| [`04-backtests/`](04-backtests/README.md) | every backtest of S0-S7 in one index: period, result, source and script |
| [`05-live/`](05-live/README.md) | **check.sh exactly as pasted**, the copy bot's whole history by day, the live phases, by wallet, the stuck coin, the end, the money |
| [`06-infrastructure/`](06-infrastructure/README.md) | the boxes (fra1 terminated, Ohio), the code map, deploy files, runbooks, wallets; **[the box and feed study of Oct 28](06-infrastructure/box-and-feed-2026-10-28.md)**; [TradeWiz against our own box](06-infrastructure/tradewiz-vs-own-box-2026-10-28.md) (no) |
| [`07-restart/`](07-restart/README.md) | **the Oct 28 review and restart plan**: where he stands, the live copies decomposed, every decision re-explored, the code fixes, the box, the runbook; [the code review](07-restart/code-review-2026-10-28.md) |
| `docs/` | the original docs: 00-08 (the videos, mechanics, speed, strategy, validation, architecture, deploy, runbook), **09-19 (everything on him and the copies)**, `docs/research/`, `docs/PROJECT-README.md` (the original repo README) |
| `analysis/research/` | the studies: `2026-10-24/` (his month, tweets, rugs, corrected), `2026-10-25/` (follow, five days), `2026-10-26/` (fails, flush, holders, oprule, six, speed, w3, wallets, wallets2), `2026-10-27/` (refused copies, our own ledger), **`2026-10-28/`** (`copy_relook`: the copy backtests re-run and extended; `live_decomp`: the live copies decomposed) |
| `data/` | seeds and reports (`follow_seed.json`, `operators/`, `reports/` ...); `data/datasets/` = the fetched data behind the studies, compressed (CLAUDE.md "Datasets") |
| `crates/`, `deploy/`, `config/` | the code (Rust workspace), install and units, config templates (`config/copy-him.example.toml`: the him-only restart config) |

## The words used

- **curve**: pump.fun's bonding curve. **create**: the coin's creation transaction; **create + H**: H slots later
  (**slot** ≈ 0.4 s).
- **operator / create signer**: the wallet that launches coins; **bundle**: the dev's own buys in the creation slot.
- **launch buy**: a buy in the create slot or the next. **landed**: on chain. **refused**: our buy landed but the
  price was past our bound (fee only).
- **tip**: what a buy pays the block builder to land early; his tip signals his conviction (0-1M low, up to 48M high).
- **tape**: every trade of a coin over its first slots. **out of sample**: scored on data the rule wasn't picked on.
- **Beirut time** = UTC+2 on these dates (check.sh); the docs use UTC.

## Security

This repo is **public**. It has no private keys, API keys or config files with credentials. Wallet addresses are public
chain data. fra1's backup (keys included) stays on the Ohio box, root only, never in git. A pre-commit hook
(`.githooks/pre-commit`, enable with `git config core.hooksPath .githooks`) refuses key material.
