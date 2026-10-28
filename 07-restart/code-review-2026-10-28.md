# Code review: the copy path (`entry.copy`) of rugsnipe-hot, copy1 snapshot (7184554)

Scope: what on the copy path cost money live (Oct 26 15:00 to Oct 27 11:45 Beirut, UTC+2) or could cost money on a
restart. File:line refs are to /home/user/copy1. "Paste" = `05-live/check-sh-2026-10-27.txt`. The box's live
`/etc/rugsnipe/rugsnipe.toml` is not in the repo, so every live setting below is either read from the paste or
inferred from it, and marked as such.

What I ran:
- `cargo build -p rugsnipe --tests`: builds in 1m36s with the pinned 1.97.1 toolchain.
- `cargo test -p rugsnipe --test sell_lifetime --test graduation --test copy`: 27 passed, 0 failed (copy 18, graduation
  3, sell_lifetime 6).
- A scratch harness against `rugsnipe-exit`, kept outside the repo
  (a scratch harness outside the repo; the repo test `crates/rugsnipe-exit/tests/scenarios.rs` `completion_behind_a_given_up_order_sells_on_the_pool` now covers it). It reproduces
  finding 5.1.
- Python over the paste's him table, and over the on-chain block times in `data/datasets/fails.tar.xz`.

## Headline numbers (my sums over the paste's 162 him copies)

| our bid | filled | tips+fees | our net | gross before tips/fees |
|---|---|---|---|---|
| 3.0M | 64 | 0.2975 | +0.4387 | +0.7362 |
| 8.0M | 61 | 0.5842 | -0.4862 | +0.0980 |
| refused (33) / not landed (4) | - | 0.0005 | -0.0005 | 0 |
| **all** | 125 | **0.8822** | **-0.0480** | **+0.8342** |

The copies made +0.83 SOL on the curve and paid 0.88 SOL in tips and fees. The 8M arm pays 4.93M more per fill
(0.00958 against 0.00465 a fill), about 0.30 SOL over its 61 fills.

---

## Q1. The operator-count rule (`copy_signer_min_buys`)

**1.1 The box ran `copy_signer_min_buys = 0`. check.sh read it correctly.** Confidence: high.
- How check.sh reads it: `cfgv() { sudo grep -m1 -E "^$1 = " "$CFG" | sed ...strip comment }`, with
  `CFG=/etc/rugsnipe/rugsnipe.toml` (deploy/bin/rugsnipe-check:40, :65). The status line prints
  `$(k=$(cfgv copy_signer_min_buys); echo "${k:-2}")` (:420).
  - A missing or differently spaced key prints the default **2**.
  - So "0" means the file literally has `copy_signer_min_buys = 0`.
  - sudo worked in that run: the same line printed "tip under 2M", which comes from `cfgv copy_min_tip_lamports`.
- The service loads that same file: `ExecStart=... --config /etc/rugsnipe/rugsnipe.toml`
  (deploy/systemd/rugsnipe-hot.service:29). The paste only edited `copy_more` lines.
- The behaviour agrees: none of the 377 him rows is "skip: op new" or "skip: op not listed"
  (deploy/bin/rugsnipe-trades:26 maps `skip_few`/`skip_unlisted` to those labels), and the counter `few` is 0.
- Impact: small, according to the backtest itself.
  - `copy_listed_only` still filtered on the 4-hourly table. That table is built from signers with ≥2 round trips
    and keeps unseen signers 3 days (operators_refresh.py `--min-n 2`, `--keep-days` 3.0 at :874;
    deploy/systemd/rugsnipe-operators.service).
  - docs/17 §10 "in the box's table, any count": +8.27 SOL on 399 copies, against +8.15 on 299 for the live rule
    (5 days).
- Fix: decide on purpose. Set it to 2 if you want the S6 rule as documented. Either way, fix 1.3 first.

**1.2 No bug makes `skip_few` always pass.** Confidence: high.
- The count excludes the current buy: it counts the stored slots in `[since, slot]` (hot.rs:2851-2856) before it
  stores this one (:2857-2860).
- `seed_his_signers` is called on the live start path: rugsnipe-hot.rs:766 `app::build` → app.rs:1030
  `hot.seed_his_signers(&c.loaded)`, loaded from `copy_signers.json` beside state.db (app.rs:884-907).
- Saves happen every minute and at shutdown, with a prune (cold.rs:2938-2948, :1222).
- The test `a_restart_keeps_his_buys_per_signer` passes.

**1.3 Bug: the window is in 400 ms slots, but the chain runs about 212 ms slots.** Confidence: high.
- The code: `SLOTS_PER_HOUR = 9_000` ("400 ms slots", hot.rs:979). `copy_signer_window_slots = window_h * 9000`
  (hot.rs:488-491). The cold prune uses the same window (app.rs:899-903 → copybuys.rs `prune`).
- The chain: block times in `data/datasets/fails.tar.xz` (coins.json, slots 461,530,131 to 461,720,104, Oct 25-26)
  give 0.2124 s/slot, which is 16,949 slots/h. docs/16 §8 has the same (970,976 slots in 205,941 s), and docs/01 C6
  says 200 ms since epoch 1053.
- So `copy_signer_window_h = 24` acts as about **12.7 h**, and the saved counts are pruned after about 12.7 h.
- Impact (if set to 2 again): stricter than backtested, so fewer copies. docs/17 §9 has ≥2 in 4 h at +2.71, against
  +4.22 for ≥2 in 24 h.
- Fix: make the constant 17_000, or better, keep unix timestamps per buy instead of slots.
- The copy-bot-history header "~0.4 s each" is wrong for the same reason.

**1.4 Smaller points.** Confidence: high.
- His buys on creates that are not in `recent` are never counted. That covers creates that failed the class filter,
  were not decoded, or arrived after his trade (copy_trade returns at hot.rs:2643-2650 before `signer_buys_then_note`).
- `HisBuy` goes over the cold ring and is dropped when the ring is full (hot.rs:1984-1989).

## Q2. Stake size

**2.1 Where the stake is set.** This is hot.rs `decide_from_watch`; e1.rs is paper only.
1. The signed ArmSet op `size` (watchlist class arm, hot.rs:3283-3302).
2. Capped by `max_probe_lamports` in probe mode, else `max_snipe_lamports` (:3306-3314).
3. `tier = 0` for every copy (:3318-3324), then `stake_by_tier[0]` (:3329-3333).
4. `stake_fits_balance` (:3463-3490): `free = wallet − min_hot_balance − stakes+bids of the last 6 s − bid − 5M`.
   If the stake is above `free` and `free ≥ stake_min_sol` (0.15), the stake becomes `free`.
5. The risk gate's `SpendCap` and `BalanceLow` checks (risk.rs:478-500).

**2.2 The A/B arms do not touch stakes.** Confidence: high.
- `[ab] small_arm`, `small_lamports` and `size_jitter` are parsed (config.rs:921-932) and read nowhere else.
  `grep -rn` over crates/ finds only config.rs.
- `[ab] skip_p` is only an on/off switch (hot.rs:433). The probability is the ArmSet's `op.ab_skip_p` (hot.rs:3560-3568).
  It does apply to copies, as `skip_ab`. Live it evidently was 0: only 4 him rows are "copied, not sent".

**2.3 Live, the reduced stakes were rare and came from `stake_fits_balance` on the shared wallet. They were not the
norm.** Confidence: high on the counts, medium on the cause of the BTRwpBmx row.
- OUR NET / our % gives `cost` (rugsnipe-trades:353). 112 of 118 measurable fills are 0.50 ± 0.03.
- The reduced ones:

  | coin | time (Beirut) | stake |
  |---|---|---|
  | FMo3m6Ce | 08:03 | 0.443 |
  | F4sw1HnJ | 08:55 | 0.430 |
  | 3ndMDGDD | 09:16 | 0.356 |
  | 28kvwz6r | 09:33 | 0.225 |
  | BTRwpBmx | 03:59 | 0.151 |

- The first four came after the stuck 2RR6sfbi locked 0.51 SOL at 06:55 and losses drained the wallet. The
  history file's "last 10 trades" (0.215-0.443) are all in that 08:03-09:47 stretch.
- BTRwpBmx's 0.151 sits right at `stake_min_sol` 0.15. It fired with other wallets' copies in flight (03:59:34,
  03:59:40, 04:00:28), which fits the 6 s in-flight deduction.
- That is about 5% of him fills (6 of 125). The money effect is small.
- Fix for a restart:
  - Give him his own wallet, funded at least `min_hot_balance + 2×(stake+bid) + margin` (about 1.2 SOL at 0.5 stakes).
  - Raise `stake_min_sol` to about 0.35-0.4. At 0.25 SOL an 8M fill costs 3.8%; a 3M fill costs 1.9%.

## Q3. Bid and tip

**3.1 How the copy's bid is chosen.** Confidence: high.
- `bid = bid_by_tier[0]` (else `bid.lamports`), capped at `max_bid` (hot.rs:3436-3446).
- If `ab_by_tier[0] > 0` and the mint's first byte is odd, the bid is `ab_by_tier[0]` (:3451-3455). The "pump"
  suffix fixes the last byte, hence the first.
- Then `min(op.ev_cap)` (:3457).
- The split per leader class (bid.rs:203-216): priority = `max(bid·p, min_priority)`, clamped to the class cap minus
  the base fee; tip = `bid·t`.
  - Primary variant for the create-slot leader's class; secondary for the next slot's class only if its plan
    differs (hot.rs:3664-3672, :3734).
  - The sender re-signs one variant per sender with that provider's tip account and `max(plan tip, provider
    min_tip)`, all on the intent's one durable nonce (sender.rs:180-262). Jito gets the primary only.

**3.2 The live split was tip-only on every class, so the 3M/8M was a tip everywhere and the priority fee was the
10,000 floor.** Confidence: medium (inferred).
- Every one of the 33 refused copies cost exactly 0.000015 = 5,000 base + 10,000 priority. The ledger's "90 refused
  buys −0.00114" agrees.
- With the repo's example split (`bam/harmonic/other = [1.0, 0.0]`, probe-a.example.toml:123, class caps 9M) a refused
  copy on those leaders would have cost 3.005M or 8.005M.
- **Impact:**
  - The repo's own measurements say BAM, Harmonic and other leaders order by priority fee (bid.rs:24-35; docs/03 §6).
    They hold about 73% of slots (BAM 37.9%, Harmonic 25.1%, other 9.8%: paper-lead.example.toml:134).
  - On those slots our copy carries the lowest CU price in the block, and the 3M/8M tip buys no position.
  - probe-a.example.toml:123 records the same effect for the rule ("at the 10,000-lamport floor those copies queued
    behind every competing buy, 113-208 positions").
  - The tip is still paid on every fill: 0.0046 (3M) or 0.0096 (8M) per fill, which is 0.9% or 1.9% of 0.5 SOL.
  - The 8M arm landed 7 positions closer on average (TIP TEST) and cost about 0.30 SOL more over the window.
- Fix:
  - Drop the 8M arm: it fails its own rule.
  - Test a cheaper tip (the sender floor is 1M where `min_tip` applies).
  - Separately, test a priority-fee share on BAM/Harmonic only. It is paid on refusals too: 26% of copies were
    refused, so at 3M that is about 0.1 SOL over this window.
  - Measure `d` by leader class before and after (sends.leader is recorded).

**3.3 The tip on a refused buy.** Confidence: high.
- The tip is a System transfer after the buy in the same transaction (template.rs:9-17; bid.rs:11-17). A buy that
  fails on its bound reverts it.
- So a refused copy pays the base fee plus its priority fee: 15,000 lamports live.
- A failed Jito bundle costs nothing.

## Q4. The exit at H − 1

**4.1 The hold.** Confidence: high.
- `copy_policy_for` (hot.rs:575-583): `hold_to_create_slot = max(H−1, 1)` for a listed signer.
- With no table entry (only possible with `copy_listed_only = false`) it keeps `[exit.default]`'s
  `hold_to_create_slots`, or none.
- The rest of the policy is `[exit.default]` as is: tp, phantom_sl, no_activity_ms, max_hold_slots, insider_sell,
  and the retries (finding 4.4).

**4.2 Is H = 6 sold at create + 5? Yes.** Confidence: high.
- `eval_normal` fires the HoldTo dump sell at the first event whose slot is ≥ create + 5, on the hot loop's
  feed-derived clock (decide.rs:344-366; position.rs:269-277).
- There is no lead-time guard: it fires when the slot starts, not before.
- Live it landed on time. Sell slot after the create, from the paste's at + landed + held:

  | sold at | copies | our net | his net |
  |---|---|---|---|
  | create + 5 | 52 | +0.70 | +1.98 |
  | create + 6 | 3 | | |
  | create + 9 | 60 | **−1.67** | +0.03 |
  | create + 10 | 7 | | |
  | other | 3 | | |

- Every one of the 125 exits was `hold_to`.
- The H = 10 operators (sold at +9) lost −1.67 SOL on 60 copies, against +0.70 on 52 for H = 6. That is a strategy
  observation from one 20 h window, not a code bug.

**4.3 H ≤ 3 cannot be copied as designed.** Confidence: high on the code; no such copies in this window.
- H = 3 gives a hold of 2, and H = 1 gives a hold of 1, which is his own sell slot (`max(1)`).
- Our copy lands at create + 0..2 (paste: 86 in his slot, 38 at +1, 1 at +2). A fill at or after the hold slot sells at
  once (`hold_due_at_open`, decide.rs:319-326), so it pays a full round trip of fees for nothing. With H = 1 it sells
  behind his dump.
- The repo's tables do list such signers: ahw-2026-10-24-tier.json has H = 1 ×1, 3 ×2, 6 ×32, 10 ×19.
- Fix: in copy_trade, skip with a journaled reason when `hold_slots < 4`, or more generally when H − 1 ≤ his slot + 1.

**4.4 There is no time-based sell backoff in the hot bot. Retries are bounded per process, can be revived, and stop
for good after exhaustion.** Confidence: high.
- Retries: every `every_slots` (2), tip × `tip_mult` (2.0), until `max_tries` (15) or `max_sell_spend_lamports`
  (20M) (decide.rs:70-79, :643-700).
  - The spend cap counts every attempt's **budgeted** tip, including attempts whose tip reverted.
  - With a 2M dump tip the order is exhausted after **4 tries, 8 slots (about 1.7 s)**. Reproduced in the harness:
    tips 2/4/8/6M, then `SellExhausted` at +8.
- After exhaustion:
  - `has_pending()` stays true, so `eval_normal` never places a new order (decide.rs:344-350; position.rs:358).
  - The `Alert` is only an rslog record and a metric (hot.rs:5141-5152). No journal line, no Telegram.
  - Only the guard handoff after 5 s alerts (hot.rs:5274-5294, 5246-5271). The guard sells on the curve until its
    own `max_sell_spend`, then gives up (guard.rs:523-534).
- The hot loop's journal line says "retrying every slot" (hot.rs:5260). For an exhausted order that is false.
- An exhausted order can be revived: `unsent()` sets `exhausted = false` and refunds the tip (decide.rs:623-640).
  It runs on any late `SellUnsent` (hot.rs:4099-4123), and the 4-hourly restarts re-adopt the position with a fresh
  spend cap.
- So for a sell that keeps failing on chain (not graduation) you get bursts of failed fees (each failed sell pays base
  plus priority; the stuck coin averaged 227k lamports), and between bursts the position sits unsold, at its full stake.
- Fix: port the long bot's schedule (stuck-coin page: 3 at once, then 5 s / 30 s / 2 min, then every 10 min after
  `max_sell_fail_sol`, never give up, a CRITICAL journal line). Also make "exhausted" a timed state, not a dead end.

## Q5. The graduation fix (af681ad)

**5.1 The pool-sell path is in the snapshot, but a race can still leave a graduated coin unsold.** Confidence: high
(code read, and reproduced on the exit engine).
- Present in the snapshot:
  - `HotIn::CurveComplete` (msgs.rs:312-316; hot.rs:4152-4181), raised from a sell that failed with
    `custom_6005` (cold.rs:2334-2355, with `LaneCmd::Pool`).
  - `HotIn::PoolState` (hot.rs:4182-4206).
  - The pool `sell_v2` template (`Templates::amm_sell` setup.rs:260; used at hot.rs:5450-5500).
  - `own_pool_sell` (real.rs:312, used at :968).
  - No guard handoff for a PumpSwap position (hot.rs:5253).
  - Tests `tests/sell_lifetime.rs` and `tests/graduation.rs` exist and pass.
- The race:
  - `on_complete` re-sends only orders that are **not** exhausted (decide.rs:282-300, `!p.exhausted` at :296).
  - If the 6005 report arrives after the curve order is exhausted (about 1.7 s at a 2M dump tip), the venue
    switches but no pool sell is ever sent: `has_pending()` blocks `eval_normal`, and `handoff` refuses a PumpSwap
    venue.
  - The 6005 report path: the lane's 400 ms status poll (real.rs:51), then `getTransaction` within the keeper's RPC
    budget (retried on the next poll if not yet available, real.rs:996-1001), then cold, then hot.
  - Harness: after `Complete`, the engine emits `VenueChanged` only, and 0 sells in the next 170 slots.
  - The test `a_graduated_coin_sells_on_its_pumpswap_pool` pushes `CurveComplete` one slot after the first sell,
    which is the best case.
- Impact: when it happens, the full stake stays in the wallet (0.5 SOL), marked to market until the next restart re-adopts the
  position.
- Fix:
  - In `on_complete`, re-arm exhausted orders (clear `exhausted`, refund their spend) or drop them so `eval_normal`
    places a fresh pool order.
  - Add a test with `CurveComplete` after `SellExhausted`.
- **5.2** Graduation is detected only from a failed sell. There is no proactive check from the feed (no
  CompleteEvent use; hot.rs:4174 is the only `ExitEvent::Complete`). So every graduation costs at least one failed
  sell and the report delay.
  - Fix: switch the venue when our or another trade's post-trade reserves reach completion, or on pump's
    CompleteEvent.
  - Also skip a copy whose `v_entry` (his post-trade vSOL) is near graduation. Today only `max_entry_vsol_lamports`
    (115 SOL in probe-a) bounds it (risk.rs:492).

## Q6. The daily stop and the caps

**6.1 How the daily stop is marked to market.** Confidence: high.
- Every second, in real modes, the cold thread computes
  `mtm = realized_today(UTC day) + Σ over open real positions (value at sell quote net of fees + proceeds − cost)`
  (cold.rs:3146-3159; triggers.rs:419-453).
- Hot sends each held position's mark every second (hot.rs:4924-4932). At the cap the kill latches and survives
  restarts.
- realized_today includes:
  - closed P&L;
  - failed buys' fees (risk.rs:379-388);
  - every landed buy's or sell's fee plus tip, and failed sells' fees (cold.rs:2316-2341; risk.rs:390-407).
- A single unsellable position cannot trip 1 SOL on its own at a 0.5 stake (at worst −cost).
  - But it uses up to half the room.
  - It **carries into the next UTC day**: `realized_today` resets, the mark does not.
  - Two stuck positions at max_open = 2 trip it alone.
  - Oct 27: realized −0.7085 + 2RR6sfbi about −0.50 = −1.2075, the logged −1207492396.
- Fix:
  - Him alone in his own wallet.
  - A per-position "unsellable" alert.
  - Optionally exclude a known-graduated position's mark only after a pool quote exists.

**6.2 Which caps bind on a copy-only run.** Confidence: high on the code; the live values are unknown.
- Every copy is attributed to one ArmSet op (the class arm, watchlist.rs:194-205). So `max_buys_per_op_per_day`
  counts all copied wallets together.
- Every sent attempt reserves the hourly, op-day and probe-day counts, and they are not given back when the buy is
  refused or dropped (risk.rs:588-618; only `open_positions` is released, risk.rs:340-346).
- `spread_buys_per_hour` (probe-a sets true) releases 1 buy per 3600/cap s; at the top of each UTC hour only one copy
  can go.
- Live, him alone: 162 sent in 20.75 h (about 7.8 an hour, about 187 a day; the backtest had about 60 a day).
  So a 40/h cap and 300/day fit him alone, but not six wallets.
- **"Copied, not sent" in the paste:**
  - Him: 4 rows. Three are after the 09:50:35 kill (EKRxxsfB 10:23, 7kbPaAyJ 10:33, GJWq6mT8 10:41): reason
    `skip_killed`. The fourth is DCZHN6qp at 15:18:02 Oct 26: reason not recoverable.
  - Other wallets: 3yrJE1A8 BFnsFRnx/EN2dKTbE/2BUHHLXg 15:00-15:14 Oct 26, the rest after the kill.
  - So no cap demonstrably bound for him.
  - The 15:00-15:18 cluster fits a cap with six wallets, or startup (nonces `UNKNOWN_SLOT` refuse claims until the
    keeper reads them, nonce.rs:242). Unverified.

## Q7. The copy window and every place a copy can drop

**7.1 Timing.** Confidence: high.
- His trade must be at create + 0 or + 1 (hot.rs:2652). create + 2 is never copied; he never buys there.
- The send is allowed while `slot_now ≤ create + copy_late_slots` (STALE uses `max(max_age_slots, copy_late_slots)`,
  hot.rs:3412-3420; LATE_SLOT at :3548-3558).
- Live: 86 of 125 fills in his slot, 38 at +1, 1 at +2. There is enough time.
- The clock is the feed's own (`advance_slot`, hot.rs:1846-1854). A stream lagging 1-4 slots also lags `slot_now`,
  so STALE and LATE never trip on a late event. Only `drift` (> 8 slots, every 10 s) and `feed_stale` pause buys.

**7.2 Every gate, in order, and what the journal or check.sh shows for it.** Silent means no journal line.

| # | where | condition | shows as |
|---|---|---|---|
| a | grpc/mod.rs:1466-1472 | the adapter forwards his trade only if the create was decoded first (adapter `recent`, slot ≤ create + 3) | "not seen" (silent) |
| b | hot.rs:1915-1923, 1954 | trades from shreds (pre-exec) are never copied; only post-exec gRPC | n/a by design |
| c | hot.rs:2191-2204 | the create was already fired for this class, free-class deferred, or the mint is held/pending (no `recent`) | "not seen" (silent) |
| d | hot.rs:2218-2224 | class filter: not SOL quote, mayhem, not Token-2022, cashback | "not seen" (silent; his buys there are not counted either) |
| e | hot.rs:2643-2653 | no `recent` entry (ring of 32, hot.rs:968), or his buy not at +0/+1 | "not seen" (silent) |
| f | hot.rs:2661-2676 | `skip_small` / `skip_unlisted` / `skip_few` | "skip: tip/size low" / "op not listed" / "op new" |
| g | hot.rs:2679-2681 | `copy_claim`: mint in `bought` (32) or already held | counter `passed` only |
| h | hot.rs:2684-2689 | `copy = log` | "logged only" |
| i | hot.rs:3283-3302 | watchlist: no class arm (`NO_MATCH`), a Creator entry with no class arm (`SHADOW`), op missing (`BAD_OP`) | "copied, not sent" |
| j | hot.rs:3412-3420 | `STALE` | "copied, not sent" |
| k | hot.rs:3498-3530 | risk: killed; SpendCap; BidCap; EntryTooHigh (>115 SOL); BalanceLow; DailyLoss; OpLatched; MaxOpenPositions; MaxBuysPerHour; MaxBuysPerOpPerDay; MaxProbesPerDay; or forced to paper (regime freeze, ArmSet not verified or expired, op not armed) | "copied, not sent" |
| l | hot.rs:3532-3537 | `TOO_HIGH`: his post-trade vSOL ≥ ArmSet `v_max` | "copied, not sent" |
| m | hot.rs:3555-3558 | `LATE_SLOT` | "copied, not sent" |
| n | hot.rs:3560-3568 | `SKIP_AB` (ArmSet `ab_skip_p` with `[ab].skip_p > 0`; its default is 0.2, config.rs:929) | "copied, not sent" |
| o | hot.rs:3571-3580 | `NO_BLOCKHASH`, `FEED_PAUSED` | "copied, not sent" |
| p | hot.rs:3582-3599 | `NO_POSITION_SLOT` (64) | "copied, not sent" |
| q | hot.rs:3619-3622 | `BAD_KEYS` | "copied, not sent" |
| r | hot.rs:3624-3635; nonce.rs:189-246 | `NO_NONCE`: one nonce chosen by mint hash, no fallback; busy, changed at or after the create slot, or unknown after a restart | "copied, not sent" |

- **Finding:** for rows i-r the copy line says `-> buy` (hot.rs:2684) before `decide_from_watch` runs. The reason
  exists only in the rslog `Decision` and in the metrics, so check.sh cannot say why a copy was not sent.
  - Fix: journal `copy <mint> not sent: <skip name>` for copies.
- Note: `v_cap = min(his vSOL·√1.05, op.v_max)` (hot.rs:3643-3647). A low ArmSet `v_max` quietly tightens the 5% bound.
  Check the class arm's `v_max` and `armset_max_age_s` freshness before a restart.

## Q8. Other findings

**8.1 A sell with no exits lease is treated as sent.** Confidence: high on the code, low on the odds.
- When `!owned`, `sell()` counts `sells_not_owner` and falls through as if it sent (hot.rs:5369-5371). It does not
  take the `unsent` path.
- So during a lease loss the engine burns its tries and exhausts in about 1.7 s. When the lease comes back the hot
  loop never sells, and the guard sells only on a 30% drop, on `grace_s` (60 s) or on a handoff.
- Fix: treat `!owned` as unsent.

**8.2 The tip key.** Confidence: high on the code.
- His tip is the sum of his top-level System `Transfer`s in the transaction (grpc/mod.rs:1447-1458, 1619-1640). Any
  SOL he moves in that transaction counts.
- A tip paid by CPI, or a priority fee, reads as 0.
- When the logs are truncated, the event fallback sets `tip: 0` (grpc/mod.rs:606-612), so a 2M+ buy under 2 SOL
  becomes `skip_small`.
- Fix: recognise the known tip accounts only, count a missing tip as unknown rather than 0, and journal it.

**8.3 Shreds against post-exec.** Confidence: high.
- Copies trigger only on the post-exec gRPC trade. Pre-exec trades go to the bundle gate only and are excluded from
  dedup so the executed copy still arrives (hot.rs:1915-1928; mux.rs:59-66).
- The measured gain from shreds is 6 ms median (docs/17 §10, `grpc_behind_shreds`). He has 1,075 failed transactions
  in the window against 377 landed launch buys, so copying pre-exec would copy his failures. Keep it as is.

**8.4 The nonce pool.** Confidence: high, low impact for him alone.
- `index_for(mint) = xxh3(mint) % pool` and there is no second choice (nonce.rs:189-191). With 32 nonces, a few
  percent of copies drop when intents overlap.
- After a restart, no copy can claim until the keeper has read the nonce values (`UNKNOWN_SLOT`).

**8.5 The blockhash.** Buys pause only with no fresh blockhash (60 slots, hot.rs:191-196) for longer than
`max_blockhash_age_ms` **and** no free sell nonce (hot.rs:1765-1787). Low risk.

**8.6 `recv_ns`** feeds only the latency histograms (hot.rs:3727-3730). Nothing gates on the event's wall-clock age.
See 7.1.

**8.7 The exit policy is coupled to the rule's.** Copies inherit `[exit.default]` whole (hot.rs:576). Re-enabling
`no_activity_ms`, `max_hold_slots = 5` or `tp` for any reason cuts the copies before H − 1. With 212 ms slots,
`no_activity_ms = 1000` is about 5 slots.

**8.8 The 4-hourly restarts** (rugsnipe-operators.timer `try-restart`) miss his buys for about 5-20 s each.
- A copy open at a restart is held by the guard: 60 s grace or a 30% drop, not H − 1.
- The new process starts with nonces unknown.
- Low, and recurring.

**8.9 The hot path's work.** Low. Before each copy, `signer_buys_then_note` scans 1,024 entries linearly (hot.rs:2837-2877).
That is microseconds against a lag of about 150 block positions.

## What to do before going live with him alone (ordered by SOL impact)

1. **Bid:** drop the 8M arm (about −0.30 SOL over this window); test about 1M against 3M as tips. Decide the class
   split per 3.2 and measure `d` by leader class.
2. **Exit robustness (code):** fix 5.1 (re-arm on Complete), 4.4 (timed backoff, never dead), 8.1 (`!owned` = unsent).
   Each has a minimal test next to `tests/sell_lifetime.rs`.
3. **Wallet and stop:** him alone in his own wallet; size the funding so `stake_fits_balance` never fits; raise
   `stake_min_sol`; 1 SOL stop with a stuck-position alert (6.1).
4. **Rules:**
   - Skip H < 4 signers (4.3).
   - Set `copy_signer_min_buys` on purpose and fix `SLOTS_PER_HOUR` (1.1, 1.3).
   - Check the H = 10 group, −1.67 on 60 copies here, on the 5-day data before keeping it (4.2).
5. **Observability:** journal why a copy was not sent (7.2); journal `SellExhausted`.
