# His rules, as decoded (operator 1, AHwJSnFN)

> **In short:**
> - He sends one buy per launch. It lands in the create slot or the next, and only as the first trade behind the launch's own bundle. An on-chain guard makes any later buy fail for about 11,000 lamports ([docs/12][d12] §2).
> - He picks tweet coins from operators he follows by their bundle wallets and fee routing. He takes more of an operator's coins, and buys bigger, after its recent coins did well ([docs/16][d16] §8-10).
> - He sells everything at a fixed slot after the create (create + H, mostly 6 or 10), set per operator. Our copy sells one slot earlier, "his sell - 1" ([docs/14][d14] §3, [docs/17][d17] §9).
> - His tip is his conviction: 0-1M on coins he rates low, up to 48M on coins he rates high. The live copy fires on his landed buys with a tip of 2M or more, or a size of 2 SOL or more ([docs/17][d17] §5, §9).
> - His patterns held out of sample. Our profit from them has not yet: live, he made +8.9099 SOL while our 125 filled copies made -0.0479 SOL ([live check][live]).

Who he is, with his results and operators: [01-who-he-is][who]. Each rule below has four parts: the rule, the
evidence, what our bot does (config key or code path, where the docs name one), and whether it held out of sample.

**Words used here.** A **create** is the launch transaction. A **slot** is one Solana block, about 0.21 s
([docs/16][d16] §8), so "create + H" means H slots after the create's slot. The **curve** is pump.fun's bonding-curve
price for a new coin. It starts at 30 virtual SOL (**vSOL**), and the price rises as SOL goes in ([docs/11][d11] Q2);
**post-bundle** means the curve right after the bundle. The **bundle** is the buys the launch's own wallets (the
**creator set**) place right behind the create. An **operator** runs a series of launches. The **create signer** is
the create's fee payer and the key of our **operator table**; a **listed** signer is in it ([docs/09][d09]). A **tip**
pays for landing early and is charged only on landing: 1M = 1,000,000 lamports = 0.001 SOL, and **mSOL** = 0.001 SOL.
The **premium** is how far above the post-bundle price our buy may fill (`max_premium`). A **tape** is every
transaction on a coin over its first slots. **v10** is the price at create + 10 over the post-bundle price, minus 1
([docs/17][d17]). **Out of sample** means scored on data not used to choose the rule. A **copy** is our buy triggered
by his landed buy (`entry.copy`); a **rule fire** is a buy our own rule decides at the create.

## Status at a glance

| rule family | his rule | our bot (latest doc) | held out of sample? |
|---|---|---|---|
| 1. entry | first behind the bundle, create slot or next, exact-state guard | `require_bundle`, `max_premium = 0.05`. The copy is bounded by `copy_max_premium` | his: yes (6,304 buys). Our 5% bound: replay only |
| 2. picks | a template launch from a repeat operator | operator table, template keys, `max_post_bundle_sol = 40`. The copy needs a listed signer he bought 2+ times in 24 h | his: predictor AUC 0.86-0.87. The table goes stale in a day. The copy rule was positive on 4 of 5 days, largely from one operator |
| 3. tweet | tweet coins, 2-10 s after the tweet | `tweet_gate = "log"`, `tweet_feed = "log"` | the rule made +3.88% on a new half-day. The "exit" cut lost in every period |
| 4. follow | bundle wallet x fee routing | `entry.follow = "on"`, rate 0.3 (off in the copy-only bot) | yes: 79-83% in the backtest, 73% in a live replay |
| 5. hold | create + H per operator | flat create + 9 for rule fires. Copies sell at H - 1 | his H: yes (444/444). Our values: replay only |
| 6. stakes | 0.4 x 2^tier, 1.5x on hot operators, rare 2 SOL+ bets | flat 0.5 SOL, hot multipliers at 1.0, `copy_big_sol = 2.0` | hot value: yes (+7.72%). Sizing not adopted under the 0.5 cap |
| 7. tips and fees | a conviction tip, paid only on landing | sell tips at 0.5M. Copy key `copy_min_tip_lamports = 2_000_000` | tip key: 4 of 5 days. The live tip A/B is still open |

In the live check window (Oct 26 15:00 to Oct 27 11:45 Beirut time) the bot ran copies only
(`entry.rule_buys = false`). It sent 162 copies of his 377 launch buys: 125 filled, 33 were refused at the price
limit, and 44 of the 125 won ([live check][live]).

## 1. Entry: first behind the bundle

**Rule.** One buy per launch, allowed only in the create slot or the next. It must be the first trade after the
creator set's bundle; any other buy fails cheaply.

**Evidence.**
- On Oct 23, 430 of 430 landed with no outside buyer ahead: 278 in the create slot, 152 in the next ([docs/09][d09] rule 1).
- Over the month the window was width 1 on all 6,304 landed buys, 66% in the create slot and 34% in the next. The
  exact-state guard fails a late buy with custom error 100, for about 11,000 lamports ([docs/12][d12] §2).
- Failed buys are 74% of his buy transactions ([docs/16][d16], intro). His trades outside our rule fire the same way:
  51% at create + 0, 46% at + 1 ([docs/16][d16] §1). A bundle inside the create transaction is a hard skip: he took 3
  of 409 ([docs/16][d16] §9).

**In our bot.**
- `entry.require_bundle = true` parks the buy behind the bundle. If another trade comes first, the fire becomes
  `skip_not_first`. `entry.max_premium = 0.0` set `min_tokens_out` to the exact post-bundle quote
  (`setup::min_tokens_out_at`). Unlike his guard, ours lets a buy through behind a sell ([docs/09][d09], "How the bot
  does it", "What is not copied").
- That bound failed us right behind him. On the coins he landed, 80 of our 83 attempts failed on it (pump error 6042),
  and 618 of our 1,140 buys over Oct 21-25 failed that way. Replayed: premium 0 made +0.28 SOL, 5% +4.19, 10% +0.27,
  25% -6.51. The change is `max_premium = 0.05` ([docs/17][d17] §9).
- The copy is bounded at his post-trade reserve plus `copy_max_premium`: 0.05 in the changes list, though the "Built"
  text quotes 10%. Copies go out until create + `copy_late_slots` (2), and only his buys at create + 0 or + 1 trigger
  one ([docs/17][d17] §9, "Built: entry.copy").

**Out of sample.** His pattern held over his whole month ([docs/12][d12] §2). Our 5% bound was chosen on the replay
days themselves, and it lost on Oct 25 (-0.35 SOL). The docs report no separate test ([docs/17][d17] §9). Live, 33 of
162 sends were refused at the price limit, which costs only the fee ([live check][live]).

## 2. Picks: the template and the operator table

**Rule.** His launches share a template shape, and most of his profit comes from operators he has traded before. That
list turns over every day.

**Evidence.**
- The Oct 23 template: a round dev buy of 1-6 SOL, and a bundle of 3 wallets outside the creator set (69% of trades).
  Dev + bundle is about 7 SOL (p90 17), the post-bundle mcap is 36-65 SOL (vSOL about 37-47), and the hosts uxento.io,
  j7tracker.io and gg.sc are favoured over ipfs.io ([docs/09][d09], "Picks").
- He attempts 32% of coins with a dev buy of exactly 3.0 SOL, and only 3-5% at 1.05-2.95 SOL ([docs/12][d12] §3).
- The 33 create signers with 3+ trades carry 289 of the 430 trades and 13.6 of the 17.8 SOL ([docs/09][d09]). He
  attempts 91% of a creator's launches once he has attempted 5+ that day ([docs/12][d12] §4).
- Each day 60-70% of his trades come from operators absent from the previous day's table, so a daily table decays to a
  quarter of its volume ([docs/09][d09], "Keeping the table fresh").
- Coin mode: he takes 14% of holder-reward coins, 2% of those with a `creator_fee_bps`, and 0% of plain coins with one
  of 100 or more ([docs/16][d16] §11). After he skips a signer's coin, he skips its next holder-reward coin 78% of the
  time ([docs/17][d17] §5).
- The 40 vSOL cap is our rule, not his. Over five days his coins above 40 made him +25.57 SOL, 48% of his net
  ([docs/17][d17] §1). He wins them with high bids.

**In our bot.**
- The operator table: `entry.operators_file` and `entry.operators_only` (`skip_not_operator`, 0x54), keyed on the
  create's fee payer (`operators::create_signer`) ([docs/09][d09]). `analysis/scripts/strategy/operators_refresh.py`
  rebuilds it every 4 hours (`rugsnipe-operators.timer`), with 7 days of memory (`--source rpc --keep-days 7`)
  ([docs/13][d13] §6). `operator_clock.py` drops the losers ([docs/09][d09]).
- The template keys: `entry.bundle_wallets = [3]` (0x55); `dev_buy_round` / `dev_buy_sol` (0x50), later
  `dev_buy_ranges_sol = [[0.95, 1.05], [2.95, 4.05], [4.95, 5.05], [7.0, 1000.0]]`; `max_bundle_sol = 17.0` (0x58);
  `uri_hosts` (0x59), now `metadata.j7tracker.io`, `meta.uxento.io`, `m.rapidlaunch.io` ([docs/09][d09]; [docs/13][d13] §6).
- `entry.max_post_bundle_sol = 40` (`skip_bundle_too_big`, 0x57). docs/09 suggested 47 and docs/11 set 40. docs/17 §4
  keeps it, because at our bid we land his rejects above 40 (25 wins, -1.149 SOL).
- Coin mode is logged only (`mode plain|holder[+bps<n>]`) ([docs/16][d16] §11). docs/17 §6 calls a holder-reward skip
  "worth adding" and does not report it built.
- The copy requires `copy_listed_only = true`, and `copy_signer_min_buys = 2` within `copy_signer_window_h = 24` ("his
  current operators"). The counts survive restarts in `copy_signers.json` (`crates/rugsnipe/src/copybuys.rs`)
  ([docs/17][d17] §9).

**Out of sample.** The template alone carries no edge: tool host plus template dev buy made +0.2% ([docs/13][d13] §2,
on data that docs/14 later corrected). His pick predictor, trained on hours 0-7 and tested on 8-11, scored an AUC of
0.86-0.87 with his live attempts and 0.66-0.74 without them ([docs/12][d12] §4). The losers rule was decided on one
24 h window and scored on the other; the flagged operators' later launches lost -1.12 and -1.38 SOL ([docs/09][d09]).
The copy's operator rule was positive on 4 of 5 days (+4.22 SOL) ([docs/17][d17] §9). With the box's table lag it made
+8.15 SOL over 5 days, but only +2.36 without one operator, 8ZN71X. Brand-new operators lose for the copy: -0.72 SOL on
151 ([docs/17][d17] §10).

## 3. The tweet layer

**Rule.** Nearly every coin he attempts is a tweet coin. His rate is highest on coins created 2-10 s after their tweet.
He ignores whether the coin is the first one on its tweet.

**Evidence.**
- 31 of 31 attempts in the sampled hour link to a tweet, and 444 of 469 over 12 h ([docs/12][d12] §3).
- On first coins, by time from tweet to coin, his attempt rate is: under 2 s 51%, 2-5 s 82%, 5-10 s 67%, 10-60 s 49%,
  1-60 min 38% ([docs/14][d14] §6). docs/12 §3 measures a wider set and gets lower rates (2-5 s: 53%).
- He attempts 55-56% of first coins and 40-43% of copies, with the same H. A tweet feed with about a 2 s lag explains
  this: it calls 7 coins an hour, 95% of them truly first, and he attempted 75% of them ([docs/14][d14] §6).
- docs/13 built a rule on his deployers: tool host, template dev buy, post-bundle <= 40, first coin on a fresh tweet, a
  deployer he traded in 7 days, hold 10. Its +5.0% (342 trades) was overstated. The data left out the 1.25% pump fee
  (that alone added +1.6 points at hold 1 and +2.3 at hold 10), cut tapes at 150 transactions and dropped 111 of the
  biggest coins ([docs/14][d14] §1). Corrected on 1,881 coins: buy all and hold 10, +3.68% [+2.71, +4.69]; "exit"
  mode +2.97%; "on" mode +5.12% ([docs/14][d14] §2). "On" is out of reach, because the verdict takes 100-400 ms from
  Frankfurt ([docs/13][d13] §4).

**In our bot.** The tweet check is `crates/rugsnipe/src/tweet.rs` (`TweetBook`). `entry.tweet_gate` was "exit"
([docs/13][d13] §6) and is now "log", because the copy cut loses in every period ([docs/14][d14] §2); also
`tweet_max_age_s = 3600` and `tweet_late_slots = 1`. The tweet feed is `entry.tweet_feed` (TweetStream;
`rugsnipe/src/tweetfeed.rs`, `rugsnipe-feed/src/ws/tweetstream.rs`). It runs "log" first, then "on"
(`skip_tweetfeed_copy`, 0x60) once the copy calls prove real ([docs/14][d14] §8). The copy-only bot turns both off,
since they served the rule's buys only ([docs/17][d17] §9).

**Out of sample.** The corrected rule held on Oct 23 12-24 UTC, never measured before: +3.88% buying all and holding
10. Its weakest stretch was 16-20 UTC at +0.9% in "exit" ([docs/14][d14] §2). The tweet check alone and his deployer
list alone were each unstable across half-days ([docs/13][d13] §2, pre-correction). Tweet authors were ranked on Oct
23 00-12 and scored later: those he took 70% or more of made +6.44%, those he took 30% or less +1.85%
([docs/14][d14] §6). The fast-feed "copy" call is still a small sample, -2.49% (21) against +3.20% (76), and is to be
measured ([docs/14][d14] §7).

## 4. The follow layer: bundle wallets, fee routing, hot operators

**Rule.** He follows operators, keyed on the bundle wallets they reuse across fresh deployers. He splits each operator
by fee routing: either the dev keeps the creator fees, or a fresh third wallet gets them (holder-reward mode). Once
his attempts on an operator reach a 30-50% rate, he attempts about four in five of its coins. He takes more after its
recent coins rose.

**Evidence.**
- 64% of his picks outside our rule come from creators he never traded ([docs/16][d16] §2).
- Ex ante, at K 2 and R 0.5 (2+ of his attempts at a 50%+ rate, counted before the coin), out of sample: his rate is
  74% / 74% on followed rule coins and 11.7% / 8.6% on the rest, covering 72% / 79% of his rule picks
  ([docs/16][d16] §3).
- Keyed on (bundle wallet, fee routing): 82% / 83% at R 0.5 and 79% / 80% at R 0.3. Followed coins carry +16.19 of his
  +20.97 SOL (77%) ([docs/16][d16] §8).
- Speed matters. With his attempts known 1 h late, coverage falls to 54-69%; 6 h late, to 22-50% ([docs/16][d16] §3).
- Inside a followed operator he skips 18%. Those coins are still worth +2.81% (174), against +4.62% for his takes
  (840) ([docs/16][d16] §8).
- Hot operators: when an operator's last 3 coins made +10% or more, he takes 83% of its coins. Those coins are worth
  +7.72% (321), against +3.65% (883) for the other followed coins ([docs/16][d16] §9).

**In our bot.**
- `entry.follow = "on"`, `follow_wallet = "AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2"`, `follow_min_attempts = 2`,
  `follow_min_rate = 0.3` ([docs/16][d16] §7). His attempts arrive through the gRPC `copied` filter, failed
  transactions included. `rugsnipe::follow::FollowTracker` counts them, saves `follow.json`, and starts warm from
  `data/follow_seed.json`. The modes are `log`, `gate` (`skip_not_followed`, 0x61), `add` and `on` ([docs/16][d16] §5).
- Hot operators: `rugsnipe_feed::bundle::RunPrice` and `entry.follow_hot_min_value` (0.10); the verdict line ends in
  hot or cold ([docs/16][d16] §10).
- The rate: at premium 0, 0.6 beat 0.3 on every day ([docs/17][d17] §8). With the 5% bound, 0.3 stays best
  ([docs/17][d17] §9). The copy-only bot turns `follow` off ([docs/17][d17] §9, "Changes").

**Out of sample.** Yes. The follow rule was fit on Oct 23 00-12 and scored on Oct 23 12-24 and Oct 24 00-12. The
coins it adds were positive in every period: +5.5% in the fit period, +7.5% and +10.1% in the tests ([docs/16][d16]
§4). In a replay of Oct 25 09:13-13:07 he attempted 49 of 67 followed coins (73%) and made +0.584 SOL on them, against
+0.332 SOL for his whole window ([docs/16][d16] §9). Copying his exit per operator did not prove a gain (+0.57 points
[-0.39, +1.73]), so it was not built ([docs/16][d16] §8).

## 5. Hold and exit: "sell at create + H"; the copy sells at "his sell - 1"

**Rule.** He sells 100% at a fixed slot counted from the create. H is a per-operator setting that he repeats. It does
not react to the flow, and it is not the insiders' dump clock. He eats the dumps that come inside the hold.

**Evidence.**
- Oct 23: H is 10 (207 trades, 48%), 6 (186, 43%), 3 (27) or 1 (10), and never anything else. There is no take-profit,
  no stop, and no insider or idle trigger; none explains more than 28% of sells. The per-signer hold explains 93% of
  sells in sample and 74% out of sample ([docs/09][d09] rule 3).
- Counted from the create, he sells at +6 or +10 (146 of 154 full-tape trades; 2,930 of 3,407 since Oct 16). He
  repeats his previous setting on a deployer 86% of the time, win or lose. On 112 of the 154 the creator set had not
  sold by +12 ([docs/14][d14] §3).
- docs/12 §2 counts from his buy instead (k = 2, 3, 4, 5, 6, 9 or 10; 75% of sells land in exactly that slot) and per
  creator (the most common hold covers about half). The later docs count from the create, per signer.
- +10 is his latest sell slot. On hot coins his median hold is 6 slots, against 9 ([docs/16][d16] §10).

**The copy's exit, "his sell - 1".** His sell is the dump: copies that sell after seeing it lost 23.4 SOL. So the copy
sells one slot before his table hold. On his 0.7 SOL+ buys on listed signers, H - 1 made +6.55 SOL, against H +2.76,
H - 2 +5.30 and H - 3 +4.09. Under the live key, H - 1 made +5.64, against H +2.98 and flat +5 +4.43 ([docs/17][d17]
§9). check.sh prints this exit as "sold at his sell - 1" ([live check][live]).

**Our own rule fires.** For us, holding to create + 10 beat his per-deployer setting, +3.68% against +3.53%
([docs/14][d14] §3). At the 5% bound, flat + 9 made +5.41 SOL, against +4.39 at H and +4.81 at flat + 10
([docs/17][d17] §9). Reactive exits fail: take-profits, stops, and selling on the creator set's first sell or on a big
outside buy all cut the winners ([docs/09][d09], "Exit clocks"). Take-profits of +15% to +60% did not help the copy
either ([docs/17][d17] §9).

**In our bot.** `[exit.default] hold_to_create_slots` plus the table's `hold_slots`: `ExitReason::HoldTo` sells 100%
on the first slot at or past create + H. The other exits are off: `tp = []`, `insider_sell = "off"`,
`no_activity_ms = 0`, `phantom_sl = { after_ms = 0, drop = 0.0 }`, `max_hold_slots = 0`. `operator_clock.py` keeps his
hold as `hold_his` ([docs/09][d09]). `entry.operator_holds = false` with `hold_to_create_slots = 10` ([docs/14][d14]
§3), later 9 ([docs/17][d17] §9). The copy sells one slot before his table hold, whatever `operator_holds` says
([docs/17][d17] §9, "Built").

**Out of sample.** His H held. In the 6 h check, 132/132 offsets were in {1, 3, 6, 10}, 11 of 11 signers kept the same
H, and 58 of 62 fresh round trips sold at the listed H. In the 24 h run, 444/444 offsets fit and 47/47 signers kept
the same H. The clock with its both-periods check, scored on held-out periods, made +16.99 / +13.50 / +19.47 SOL,
against +13.78 / +9.07 / +18.18 for his holds ([docs/09][d09]). Flat + 9 and H - 1 were chosen on the replay and tape
days, and the docs give no separate test.

## 6. Stakes and sizing

**Rule.** His stake is 0.4 SOL x 2^tier, where the tier is his confidence in the operator, times 1.5^a, where a is
noise. He sizes up where his record with the creator is good, and on hot operators. Now and then he places a big bet
of 2 SOL or more with a low tip.

**Evidence.**
- About 82% of a signer's attempts are at its usual tier. His landed returns by tier are +2.3% / +7.3% / +21.3%
  ([docs/09][d09], "stake tier").
- His stake is 0.6 SOL base, up to 3.6. By his earlier P&L with the creator: new +1.34% a trade, negative +1.90%, above
  +2 SOL **+6.01%** ([docs/12][d12] §2).
- Coin value by tier (tier from his median stake on the deployer over the 7 days before): tier 0 +4.44% (1,620 coins),
  tier 1 +5.91% (170), tier 2 +10.87% (91) ([docs/14][d14] §4).
- On hot operators his median stake is 0.909 SOL, against 0.604 ([docs/16][d16] §9). On high-conviction coins it is
  0.6-1.8 SOL ([docs/17][d17] §5).
- His buys with a tip under 4M and a size of 2 SOL or more: 39 buys, +14.57 SOL, +0.374 a buy ([docs/17][d17] §9).

**In our bot.**
- The keys: `entry.stake_by_tier = [l0, l1, l2]`, `bid.by_tier`, `entry.min_stake_tier` (`skip_low_tier`), and the
  table's `stake_tier` ([docs/09][d09]).
- Flat 0.5 SOL: under a 0.5 ceiling every tier pays at the full 0.5. That makes +18.2 mSOL a trade, against +2.5 for
  his ladder scaled down. Size up on tiers 1-2 (1.0 / 2.0 SOL) once the wallet carries it ([docs/14][d14] §4).
- `entry.follow_hot_stake_mult` and `follow_cold_stake_mult` stay at 1.0. Flat 0.5 made +23.3 SOL, against +18.8 for
  0.5 hot and 0.33 cold. Set the hot multiplier to 1.5 when the cap rises ([docs/16][d16] §10).
- Copies trade at tier 0 stake and bid. `copy_big_sol = 2.0` copies his 2 SOL+ buys whatever their tip. Copy stakes of
  0.25 / 0.75 / 1.0 SOL made +2.50 / +8.83 / +12.05 SOL, against +5.64 at 0.5: "sizing, not a loss" ([docs/17][d17] §9).

**Out of sample.** The tiers are set ex ante, from the 7 days before each coin, but no held-out split is reported
([docs/14][d14] §4). The hot value held out of sample (+7.72%), but the multipliers stay off ([docs/16][d16] §9-10).
For `copy_big_sol`, the 6 extra copies made +1.42 SOL, positive on 1 of 5 tape days. His own month shows the bucket
positive on 7 of 12 days ([docs/17][d17] §9).

## 7. Tips and fees

**Rule.** He pays only when he lands. His buy tip tracks his conviction: about 1M or less on coins he rates low, up to
48M on coins he rates high, in fixed steps. His sells are cheap.

**Evidence.**
- docs/09 first saw a base fee plus a flat ~1.5M tip paid only on landing, fanned out to many relays behind one durable
  nonce (rule 4). docs/12 §2 found a 1.5M routine tip with no priority fee, and about 12M (an 8M tip) when he wants a
  launch badly.
- His median tip is 1.0M, hot or cold ([docs/16][d16] §10). His landed tips come in steps: 1.0, 1.5, 1.8, 2.4, 3.6,
  4.8, 7.2, 12, 18, 24M and up. On high-conviction coins the tip is 1-2% of the stake ([docs/17][d17] §5).
- The market bids up for the coins worth more. Above 40 vSOL, winning bids of 1.5M or less got a v10 of +8.2% (100
  coins), 8-16M got +15.8% (69), and 16-32M got +30.1% (52) ([docs/17][d17] §3).
- His month by tip (size < 2 SOL, creators he bought 2+ times in 24 h): 1.5-2M made +0.003 SOL a buy (487 buys), 2-3M
  +0.053, 3-4M +0.098, and 4M+ +0.053 ([docs/17][d17] §9).
- His sells cost 0.5M priority plus a 1M tip, later measured at about 1.3M ([docs/12][d12] §2, [docs/14][d14] §5). His
  median round trip is 3.3 mSOL (0.75%), against our 9.0 mSOL (1.77%) on Oct 24 ([docs/11][d11]).

**In our bot.**
- Bids: `[bid]` and `[senders]` fan out to five relays behind one durable nonce ([docs/09][d09]). Our bid is fixed by
  route at 1.5-7M, with a median of 3.99M on the races we won ([docs/17][d17] §3). A higher flat bid does not fix this:
  each setting is a bet on the few coins that go +100% ([docs/17][d17] §4).
- Sell tips are cut to his level: `dump_tip_lamports` and `sell_tip_lamports` from 2M to 0.5M. The buy A/B test is
  `bid.ab_by_tier` (commit c03c4cc), with a proposed second ladder of 1.5M / 6M / 12M ([docs/14][d14] §5).
- The copy keys on his tip. `copy_min_tip_lamports` started at 4,000,000 and was lowered to 2,000,000 after the
  ablation: +8.02 SOL against +5.64, better on every day. His tip is read from his top-level System transfers
  (`transfers_from`) ([docs/17][d17] §9). check.sh shows the 2M floor live ("tip under 2M") ([live check][live]).

**Out of sample.** On his weak days the tip key held up: tips of 4M or more at the 5% bound were positive on 4 of 5
days ([docs/17][d17] §9). The 2M floor was chosen on the tape days, but his own month supports it: 2-3M and 3-4M tips
were positive on 9 of 11 and 11 of 14 days ([docs/17][d17] §9). The live tip test on him since Oct 26 18:20 Beirut:

| our bid | copies | filled | avg positions behind | net SOL |
|---|---|---|---|---|
| 3.0M | 56 | 41 | 156 | -0.0169 |
| 8.0M | 79 | 59 | 149 | -0.4863 |

The test's rule is to keep the higher bid only if it lands closer and nets more per copy ([live check][live]).

## Sources

- [docs/09-operator-wave.md][d09], [docs/11-operator-bot-vs-copied-wallet-2026-10-24.md][d11],
  [docs/12-how-the-copied-wallet-trades.md][d12]
- [docs/13-tweet-coins.md][d13] (its numbers are corrected by docs/14), [docs/14-corrected-backtest.md][d14]
- [docs/16-who-he-follows.md][d16], [docs/17-newest-bot-vs-him-5-days.md][d17]
- [docs/18-copy-6anjqMe.md][d18] (why the bot copies him and not 6anjqMe: see [01-who-he-is][who] §10)
- [analysis/research/2026-10-24/README.md][r24], [analysis/research/2026-10-25/follow/README.md][r25f],
  [analysis/research/2026-10-25/five/README.md][r25v] (the scripts behind the numbers)
- [05-live/check-sh-2026-10-27.txt][live] (row "1 him", its section, and the tip test)

[d09]: ../docs/09-operator-wave.md
[d11]: ../docs/11-operator-bot-vs-copied-wallet-2026-10-24.md
[d12]: ../docs/12-how-the-copied-wallet-trades.md
[d13]: ../docs/13-tweet-coins.md
[d14]: ../docs/14-corrected-backtest.md
[d16]: ../docs/16-who-he-follows.md
[d17]: ../docs/17-newest-bot-vs-him-5-days.md
[d18]: ../docs/18-copy-6anjqMe.md
[r24]: ../analysis/research/2026-10-24/README.md
[r25f]: ../analysis/research/2026-10-25/follow/README.md
[r25v]: ../analysis/research/2026-10-25/five/README.md
[live]: ../05-live/check-sh-2026-10-27.txt
[who]: ../01-who-he-is/README.md
