# 03. Strategies: every strategy built around him, in order

Each page follows the same layout: status, which of his rules it uses, code, config keys, sources, the rule, how it was
found, its backtests, its live result, the verdict and the open questions. **S6 is the one that traded real money on
him.** S0 is the project's start, before him. S1-S5 are rule bots built from his decoded behaviour. S7 points the S6
copy at other wallets (wallet 4's copies are in the copy2 repo).

| | Strategy | Status | Live | Best evidence |
|---|---|---|---|---|
| [S0](S0-lead-policy-dev-sniping.md) | **LEAD policy**: dev sniping, first behind the bundle (the videos' method, validated and narrowed) | ran live as a probe, lost; replaced by S1 | Oct 21-23 | backtest +3.7% a trade [+0.7, +6.6] on the fresh holdout, n = 150 (docs/04 §3); **live −4.856 SOL on 469 attempts** (docs/10 §1) |
| [S1](S1-operator-wave.md) | **Operator wave**: his entry, his operator table, his exit clock | live from Oct 23 19:18 UTC; the base of the rule bot until rule buys were switched off | Oct 23 → about Oct 25-26 | backtest operator clock +16.99 / +13.50 / +19.47 SOL over three rotations (docs/09); live Oct 24 00:00-12:29 −0.253 SOL against his +1.336 (docs/11) |
| [S2](S2-microscalp-v2.md) | **Micro-scalp v2**: the LEAD rebuilt on the live plumbing | built, shelved Oct 24 13:00 UTC, never deployed (commit `0f0d78a`, not on this branch) | never | the races we actually win lose −2.63% after costs (docs/10 §2) |
| [S3](S3-tweet-rule.md) | **Tweet rule**: his deployers' coins, first coin on a fresh tweet | live in "exit" mode from Oct 24 ~17:29 UTC until rule buys went off; the TweetStream skip only in "log" | Oct 24 → about Oct 25-26 | corrected backtest +3.68% [+2.71, +4.69] a trade on 1,881 coins (docs/14 §2; docs/13's +5.0% was overstated) |
| [S4](S4-big-rugs.md) | **Big rugs**: what predicts the −30% coins | research; the rapidlaunch dumper skip and the hidden dev buy fix shipped by Oct 25 | about Oct 25 | one rule held: skip dumper-list coins on rapidlaunch, +0.40 SOL over 36 h (docs/15 §3) |
| [S5](S5-follow-bundle-wallets.md) | **Follow the operators he follows**: bundle wallet × fee routing (`entry.follow`) | built; ran in the rule bot on Oct 25; idle since copy-only | Oct 25 | +4.74% a trade on 981 out-of-sample coins (docs/16 §8); exact replay +1.03 SOL in 2.7 days against his +33.5 (docs/17 §8) |
| [S6](S6-copy-him.md) | **Copy him** (`entry.copy`): buy behind his landed launch buy, sell a slot before his sell | **live on real money**; stopped by the daily-loss kill; reviewed Oct 28 for a restart ([07-restart](../07-restart/README.md)) | Oct 25 22:08 UTC → Oct 27 07:50 UTC | backtest +8.02 SOL on 298 copies, Oct 21-25 (docs/17 §9), of which Oct 24-25 +0.27 (−0.52 without the best 2; copy_relook); **live: he +8.9099, our 162 copies −0.0479** (curve +0.83, tips and fees −0.88) |
| [S7](S7-other-copy-targets.md) | **Copy other wallets** beside him (`entry.copy_more`): 3yrJE1A8, JBokzLFR, CxyKYmQo, D5BDDkBt (and wallet 4, see copy2) | live; wallets 3 and 5 removed Oct 27; stopped by the same kill | Oct 26 → Oct 27 07:50 UTC | 3yrJE1A8 at create + 29: +8.28 on 252 copies (docs/19 §5); live wallet 2 −0.0135 on 61, wallet 6 +0.0857 on 8; wallets 3 and 5 about −0.39 and −0.54 |

## How one led to the next

1. **S0** (Oct 12-23): the videos' method loses on data. One narrow variant (LEAD, first behind the dev's bundle) holds on
   history and goes live as a probe. It loses: the races we win are the ones nobody else wants.
2. **Oct 23: him.** The best wallet of the day (+17.8 SOL on 430 round trips) is decoded: the same entry, but only on
   repeat operators and with a per-operator exit clock. That's **S1**, live the same evening.
3. **Oct 24:** S2 tries the LEAD again on live plumbing and is shelved before deploy. **S3** adds his tweet-coin layer, and
   **S4** studies the big rugs on S3's coins.
4. **Oct 25:** **S5** finds who he follows (bundle wallets × fee routing). The exact replay shows the rule bot still makes
   a small fraction of what he makes, because he wins the first spot (an auction) on the coins worth having. So instead of
   predicting his picks, **S6** copies his landed buys directly. It goes live at 22:08 UTC. The rule buys are then
   switched off (`entry.rule_buys = false`; the bot buys copies only by Oct 26-27).
5. **Oct 26:** **S7** adds other wallets with `copy_more`. Searches find most profitable wallets can't be copied.
   3yrJE1A8, JBokzLFR, CxyKYmQo, D5BDDkBt and wallet 4 (H9kuqGKN, copy2) are added.
6. **Oct 27:** wallets 3 and 5 lose live and are removed. At 07:50 UTC the stuck wallet-4 coin 2RR6sfbi pushes the
   shared daily stop past −1 SOL, and the bot stops ([stuck coin](../05-live/stuck-coin-2RR6sfbi.md)). The hot bot is
   stopped and disabled; fra1 is terminated on Oct 28.

## What survives

- **The copy of him (S6)** broke even live (−0.0479 SOL on 162 copies) while he made +8.91. We filled his weaker coins
  and the 5% bound refused his better ones (+4.63 of his +8.92 was on the 33 refused). Every fix for refusals tested
  negative over 5 days (S6 page).
- **Nothing here is running.** The code for every strategy is in `crates/rugsnipe` (S2's only in commit `0f0d78a`). The
  config switches are in `config/rugsnipe.example.toml` and docs 09-19.
- The wallet that does make money as a copy target is wallet 4, but only on coins this bot can't see. That is the long
  copy, in the **copy2** repo.
