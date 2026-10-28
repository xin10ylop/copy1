# Him (AHwJSnFN) re-checked on chain, 2026-10-28

Wallet `AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2`. All times are **UTC** unless marked Beirut. Beirut was UTC+3
until Oct 25 and has been UTC+2 since. The live window Oct 26 15:00 to Oct 27 11:45:34 Beirut is Oct 26 13:00 to Oct
27 09:45:34 UTC. The scripts are in `scripts/` (README); the raw cache and the large data files stayed outside the repo.
Written by the on-chain review agent of the Oct 28 session; the owner's Triton endpoint; 19,656 RPC calls (about $0.20).

## Data, method, cost

| what | source | size |
|---|---|---|
| his full signature list, 2025-01-16 09:03:48 to 2026-10-28 14:56:35 | Triton `getSignaturesForAddress` (`sigs.py`) | 49,493 signatures (25,397 failed) |
| every tx since 2026-10-24 00:00, failed ones included | Triton `getTransaction` (`fetch.py recent`, `fetch1.py`) | 7,223 |
| every successful tx before 2026-09-24 13:11 | Triton (`fetch.py early`) | 8,620 |
| 2026-09-24 13:11 to 10-24 13:09 | the Oct-24 study's rows (`data/datasets/month.tar.xz`, `month/AHwJSnFN.jsonl`) | 30,499 |

- **The two sources agree.** The Triton signature list holds all 30,499 month signatures and nothing extra in that
  range. His balance before the month (64.9150 SOL) plus the month's deltas gives 218.7522 SOL. The first Triton tx
  after the month opens at exactly 218.7522 SOL (`balance.py`).
- **Net SOL** is the sum of his own account's balance deltas (`postBalances − preBalances`) over all his txs. It
  includes fees, tips, failed txs and dust.
- **tip** follows the bot's definition (`deploy/bin/rugsnipe-vs-him` `tip_of`): his top-level System transfers, except
  those to token accounts.
- **priority** is the tx fee minus 5,000 lamports per signature.
- **Month tips.** The month rows only flag known tip accounts. For the month, the 116 relay tip accounts that appear
  as top-level tips in his Triton trades are counted too (`norm.py`).
- **Version-1 transactions** exist on chain now. 31 txs in his list are version 1, and fetching them needs
  `maxSupportedTransactionVersion: 1`. All 31 are DeFG8i8z's (section 3d), not his.
- **RPC calls: 19,656**, counted per request including batch elements and retries. About 150 of those were wasted on
  the version-1 txs. At $10 per million that is about $0.20.

## 1. Is he still the same trader? Yes, the same machine at lower volume and lower profit per day

Scripts: `q1.py`, `tables.py`, `q1b.py`, `relays.py`. Every coin has exactly 1 buy and 1 sell, and all 1,401 are
closed. "Copy key" means tip ≥ 2M or size ≥ 2 SOL: the live bot's `entry.copy` with `copy_big_sol = 2.0`.

| UTC day | landed buys | failed buys | fail % | net SOL (all his txs) | per buy | win % | stake median / mean | tip ≥ 2M | copy key | tip+priority ≥ 2M | priority ≥ 0.1M | at create+0 | sold at create+6/+10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Oct 24 | 315 | 954 | 75% | +5.23 | +0.0166 | 48.3% | 0.593 / 0.777 | 33.3% | 34.3% | 46.7% | 19.7% | 60.6% | 67.6% |
| Oct 25 | 235 | 797 | 77% | +6.98 | +0.0298 | 43.0% | 0.593 / 0.829 | 39.6% | 42.1% | 57.0% | 23.4% | 62.6% | 60.4% |
| Oct 26 | 372 | 1,088 | 75% | +10.20 | +0.0275 | 50.0% | 0.593 / 0.789 | 39.8% | 41.4% | 57.0% | 22.0% | 62.9% | 62.9% |
| Oct 27 | 305 | 1,005 | 77% | +5.76 | +0.0189 | 46.2% | 0.593 / 0.749 | 38.7% | 39.3% | 58.4% | 24.3% | 68.9% | 65.6% |
| Oct 28 (to 14:56) | 174 | 473 | 73% | +3.15 | +0.0181 | 48.9% | 0.593 / 0.707 | 42.5% | 43.7% | 54.0% | 16.1% | 64.4% | 58.6% |
| **Oct 24-28** | **1,401** | **4,317** | 75% | **+31.32** | +0.0224 | 47.5% | 0.593 / 0.774 | 38.4% | 39.8% | 54.6% | 21.5% | 63.8% | 63.6% |
| Oct 17-23, average day | 437 | 1,263 | 74% | +15.30 | +0.0350 | 47.1% | 0.593 / 0.820 | 42.0% | 43.2% | 55.8% | 19.4% | 64.2% | 67.6% |
| Sep 24 13:11 to Oct 23, average day (18 trading days) | 343 | 952 | 74% | +8.49 | +0.0242 | 34.9% | 0.593 / 0.744 | 30.0% | 31.7% | 40.1% | 18.9% | 66.6% | 41.4% |

- **Failed txs** cost 0.0466 SOL over Oct 24-28, at 11,001 lamports each.
- **The month total.** The month rows sum to +153.837 SOL. That matches the docs' "balance rose +153.8". The docs'
  +151.6 is `profile.py`'s trades-only figure. The figure for Sep 24 13:11 to Oct 23 24:00 is +152.809.
- **The early weeks were a different regime.** September drags the month's win rate (34.9%) and its create+6/+10
  share down. In September he sold at create +2 to +5; the +6/+10 holds started on Oct 16. The docs' 47-51% win rate
  and 400-600 trades a day describe Oct 17-23.

**Unchanged:**
- **Stake ladder.** Still 0.395 × 1.5^a, with doubling: 0.395 / 0.593 / 0.889 / 1.185 / 1.778 / 2.370 / 3.556 SOL.
  The 0.395 base share rose from 17.9% to 22.3%.
- **Failed buys.** Of 4,317, 4,119 fail with Custom 100 on instruction 2 (the state guard: someone traded first).
  161 fail with Custom 101: 156 on instruction 1 (the slot guard: too late) and 5 on instruction 2.
- **Tx layout.** AdvanceNonce, `A5c1eN`, `8jzqTj`, 2× ComputeBudget, ATA, the pump buy, then the tip.
- **Landing.** 63.8% in the create slot (Oct 17-23: 64.2%).
- **Sells.** Always one sell per coin. Either a 1.0M tip with 0.5M priority (797) or a 1.5M tip with no priority (604).
- **Hold.** Median 2 s (p10 1 s, p90 2 s).
- **Programs.** The same set: System, ComputeBudget, pump, the 2 guards, ATA, Token-2022 and SPL Token.
- **Relays.** The same mix lands his buys: helius 34.8%, nozomi 34.8%, node1 6.1%, soyas 4.7% … No new relay.
- **Nonces.** The same 100 durable nonce accounts, created Sep 12 and 15, authority him. 5,718 of his 7,119 own txs
  since Oct 24 use one.

**Changed:**
- **Volume.** About 30% fewer landed buys. Full days Oct 24-27 averaged 307 (235-372) against 437 (357-592) on Oct 17-23.
- **Profit.** About half the daily profit: +7.04 SOL a day against +15.30. Per buy: +0.022 against +0.035.
- **Hold.** A slight shift to the longer hold: planned H = 10 on 50.0% of coins, against 34-55% a day on Oct 17-23.

**Tip steps, landed buys:**

| tip (M) | <1 | 1.0 | 1.5 | 1.8 | 2.4 | 3.6 | 4.8 | 7.2 | 12 | 18 | 24 | other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Oct 17-23 (3,062) | 1.9% | 40.2% | 7.3% | 7.1% | 4.5% | 4.2% | 6.9% | 6.7% | 5.0% | 1.9% | 1.6% | 12.7% |
| Oct 24-28 (1,401) | 1.4% | 42.1% | 7.4% | 7.1% | 6.0% | 3.5% | 6.3% | 4.7% | 3.6% | 1.9% | 1.3% | 14.8% |

The "other" bucket is mostly more steps: 1.6, 3.2, 6.4, 8, 9.6, 10, 15, 16, 20, 30, 32 and 48M.

**Finding: part of his bid is a priority fee.**
- 21.5% of his landed buys carry a priority fee of 0.1M or more (19.4% on Oct 17-23, so not a new habit).
- Among nozomi-landed buys the share is 56%.
- Tip plus priority sits on the same ladder. For example, a 1.0M tip with 3.8M priority makes 4.8M, and 1.0M with
  6.2M makes 7.2M.
- A key on the tip alone therefore misses part of his conviction (section 4).

## 2. Hold: yes, still mostly create+6 or create+10

Scripts: `trips.py`, `createslot.py`, `tables.py`.
- **Sample:** all 1,401 round trips since Oct 24 00:00.
- **Create slot:** taken from his buy's slot-guard arguments `[lo, lo+1]`.
- **Check:** on 80 coins spread over Oct 24-28, each coin's oldest signature, which is its pump `create_v2`, was read.
  **80 of 80** had create slot = guard lo. The check cost 161 calls.

| H = slots after the create | planned (his sell guard's start) | landed (his first and only sell) |
|---|---|---|
| 1 | 30 (2.1%) | 20 (1.4%) |
| 3 | 90 (6.4%) | 56 (4.0%) |
| 6 | **581 (41.5%)** | 395 (28.2%) |
| 7 | – | 167 (11.9%) |
| 10 | **700 (50.0%)** | 496 (35.4%) |
| 11 | – | 178 (12.7%) |
| other (2, 4, 8, 12, 13) | 0 | 77 (5.5%) |

- **Planned:** 1,281 of 1,401 (91.4%) are planned at +6 or +10. Oct 17-23 ran 82-93% a day.
- **Landed:** at the planned slot 959 times (68.5%), one slot later 379 times (27.1%), 2-8 slots later 63 times.
- **From his buy:** a median of 9 slots, about 2 s.

## 3. Linked wallets

### 3a. Every SOL transfer over his whole history

Scripts: `q3flows.py`, `flowtable.py`, `q3late.py`. The full lists are `data/flows.csv` (1,946 rows) and
`data/counterparties.csv` (610 counterparties, with balance and last activity now).

| period (UTC) | in: transfers | in: SOL | in: wallets | out: transfers | out: SOL | out: accounts | dust in |
|---|---|---|---|---|---|---|---|
| 2025-01-16 to 01-19 | 1 | 22.975 | 1 | 2 | 24.090 | 2 | 28 |
| 2026-08-17 to 08-23 | 1 | 30.000 | 1 | 3 | 4.037 | 2 | 2 |
| **2026-08-25 to 09-03** | **1,081** | **3,246.362** | **232** | **220** | **3,211.658** | **220** | 118 |
| 2026-09-04 to 09-30 | 0 | 0 | 0 | 105 | 0.126 | 105 | 121 |
| 2026-10-01 to 10-02 | 55 | 12.348 | 55 | 55 | 14.035 | 55 | 3 |
| 2026-10-03 to 10-28 14:56 | **0** | **0** | 0 | **0** | **0** | 0 | 151 |

Dust means transfers under 0.0001 SOL. It is address-poisoning spam: 154 transfers from 136 payers since Oct 1.

**His history, from the chain.** Scripts: `q3flows.py`, `q3origin.py`, `q3far.py`, `balance.py`, `q3d.py`.

1. **Funding, 2025-01-16 09:03:48: 22.974744 SOL from `49Fr9YPNgzeFHDVrdwhqcfamV5YnmWbpjGtZq6uFGA9e`.** This is
   his first tx ever.
   - `49Fr9YPN` is a 2-tx pass-through wallet. It received the SOL 6 s earlier from
     `2vQv4MSouYFdzBhPwGZJ3LhS5amLX9Rk3ucqvxNY5d4b`, also 2 txs, which received it from
     `B8djRJNXkAAvCmKX1ZcbdogHuEQa2e6tq7rBWc8uP5XR`, also 2 txs. Every step is another fresh wallet.
   - On Jan 16 he launched 1 pump coin himself, with a 10 SOL dev buy.
   - On Jan 18 he sent out 24.077494 SOL to `Hr9ejPfd…`, a 2-tx hop that forwarded it 8 s later to `AJsaFJJg…`,
     another 2-tx hop. He also sent 0.0125 SOL to `4b4jxeXk…`, which looks like a bot's fee collector: 3,000+ txs,
     receive-only. That left his balance at 0.01 SOL.
2. **Restart, 2026-08-17 10:14:56: 30 SOL from `Gj9srqLhRMtmasG1zxbHdw86ymDHdmVEvCV3Cs9SYBWy`.**
   - Between Aug 17 and Sep 1, Gj9srqLh sent him 199.020 SOL in 5 transfers (30, 25, 35, 59.02, 50). He sent it
     49.0 SOL on Aug 29.
   - Gj9srqLh also received 83.72 SOL from the fleet's biggest sweeper, H2KbeD7H. It paid 46.29 SOL to `973AR4f9…`,
     a Raydium/token trading wallet active Dec 2024 to Sep 1, 2026. It holds 0.9996 SOL; its last activity, on Oct
     9, is someone else's spam.
3. **Launcher, Aug 17-18, 2026.** He created 36 pump coins himself (`create_v2`, mint co-signing, dev buys of
   0.49-6.9 SOL). With the Jan 2025 coin that makes 37, and his net on them is −2.931 SOL.
4. **Fleet hub, Aug 25 to Sep 3, 2026.** The docs never covered this.
   - **In:** 232 wallets swept 3,246.36 SOL into him in 1,081 transfers. Each sweep closes the sender's pump token
     accounts and sends its whole balance. In 59 of 60 sampled sweeps, the sender's previous tx was its own pump.fun
     trade (`q3hops.py`). The biggest sweeper, `H2KbeD7HvNcpVMo1uTJvyaLxmHCGsTqvJZrNZHrzp9h3`, swept 99 times for
     611.34 SOL.
   - **Out:** 3,211.66 SOL in 220 transfers to 220 fresh wallets, each with a separate Jito tip tx. All 60 sampled
     first hops forwarded the full amount in the same second (one bundle) to another fresh wallet. 12 chains followed
     hop by hop (`q3chain.py`) all went hop, hop, then split off 3.963, 5.000 or 7.300 SOL to a wallet that
     pump-traded and later swept back to him. 3 of the 12 ended at H2KbeD7H. Walking backwards from 12 sweepers: 4
     reach him in exactly 3 hops; 8 did not resolve within the read limits.
   - **What it means:** he ran a fleet of a few hundred sniper wallets out of AHwJ. He funded them through 3-hop
     chains and swept the money back.
   - **Now:** 229 of the 232 sweeper accounts are closed. Their last own activity was in August or September. The
     October hits on H2KbeD7H and 8rDNtWdy are third-party cNFT spam (`q3fleetnow.py`, `q3cp.py`).
5. **His own sniper, from Sep 6, 2026.** He deployed both guards that day (section 3c) and made 115 buys from AHwJ.
   On Sep 12 and 15 he created 100 durable nonce accounts (100 × 0.00105664 SOL, each nonce co-signing its
   `createAccount`, `q3nonce.py`). The other Sep 4-30 outflows are 2 program accounts, 2 ProgramData accounts, and a
   0.006 SOL top-up of `A3V7uW7h…`, a token account from his pump AMM swaps, probably his WSOL account, now closed.
6. **Test sends, Oct 1, 2026, 10:56:55 to 14:04:58** (`oct1deep.py`). He funded 55 fresh wallets: 45 × 0.25, 5 ×
   0.5, 2 × 0.10618, 2 × 0.02478 and 1 × 0.0227 SOL. All 55 were created by him that day, swept back the same day
   (12.348 SOL back; net cost 1.687 SOL) and are empty now. **None trades pump.fun.** 1,046 of their txs read: 100%
   System + ComputeBudget, 928 of them with a Memo; 928 transfers to relay tip accounts (0.838 SOL), 55 sweeps back
   to him, and 8 tiny ones (0.0085 SOL) to other addresses. They were relay-landing tests, not trading wallets.
7. **Since Oct 3, nothing in or out except dust.** No withdrawals; the profit sits in the wallet. Balance at day end:
   39.59 SOL on Sep 19, 102.62 on Sep 30, 217.72 on Oct 23, 249.05 on Oct 28.

### 3b. Who else invokes his guard programs? Nobody, ever

Script: `q3b.py`. **Every** signature of both programs was paged and his own removed; his list is complete up to
slot 462,516,181. The oldest signature of each program is its deploy; neither was ever upgraded.

| program | all signatures (Sep 6 to now) | up to his newest slot | his | anyone else | newer than his list |
|---|---|---|---|---|---|
| slot guard `A5c1eN7MzgYWAfBBbwogAkjjmoiRYP3CDGTV2Fa5x4hp` | 45,538 | 45,514 | 45,514 | **0** | 24 |
| state guard `8jzqTjEDKxxTppLGjyhUXUmDbHeUjJ5kkpGiWmC9jAez` | 35,413 | 35,392 | 35,392 | **0** | 21 |

### 3c. Who deployed them? He did

Script: `q3c.py` (getAccountInfo on each program and its ProgramData).

| program | ProgramData | upgrade authority | deployed (UTC) | deploy fee payer |
|---|---|---|---|---|
| `A5c1eN7M…` | `4FzdKmxTt7CtMKkKxxeW92uivEgU5EojMu9hdmfrm72j` | **AHwJSnFN (him)** | 2026-09-06 09:11:02, slot 444,755,378 | him |
| `8jzqTjED…` | `5EzjTsBpqh3BvDY53BsXj4bgkRtAHymTcn3hz6efrZFc` | **AHwJSnFN (him)** | 2026-09-06 13:59:37, slot 444,810,024 | him |

The authority is his own wallet, so there is no separate deployer to trace; its links are the ones in 3a.

### 3d. Co-signers, tokens, and wallets with his pattern

Scripts: `q3d.py`, `q3dev.py`, `q3prog7.py`, `q3defg.py`, `odd.py`.

- **Co-signers.** He signed 44,721 txs across the Triton and month rows; 44,654 have one signer. The 67 others are
  all his own new keys: 37 coin creates (the mint), 4 program deploys (the program key) and 26 nonce creations. **No
  other wallet co-signs.**
- **Tokens.** He holds one token account, a pump mint (`FNuPsfHE…pump`, 71,424 tokens). No non-pump tokens.
- **An active linked wallet: `4yN2vFSi9kFW2wwz5konV83QAao2rEJcpyTijgkh1Aea`.**
  - He funded it with 4.0 SOL on Aug 23 and 3.5 SOL on Aug 25. It sent him 3.49 SOL on Aug 25 and 12.11 SOL on Sep 1.
  - All 781 of its txs read. In August it took in 0.011 SOL amounts from fleet wallets (CaNQ6EY9, CLCWQEHj …) and
    paid out about 0.37 SOL each to 300+ wallets. It holds 2.967 SOL.
  - **Its last activity, 2026-10-22 02:27-02:32 UTC:** it deployed a new program,
    `7SVCZWEjXkjuWM982ogKSyHiLKj9YtUmERGkkwFfKUcG` (authority 4yN2vFSi, 2,189 bytes; 4 txs ever, all from this
    wallet), and sent 0.001 SOL with a memo to each of **his** relay tip accounts: soyas, astralane, nozomi, Falcon,
    LandX, 0slot, node1, jito, helius. This looks like his dev/test wallet, building something 6 days ago. Nothing it
    built is in use.
- **A third-party bot, `DeFG8i8zoJ3hN155nmvLq266ZVxWmNgRaTz5KQVHfe2S`**, using program `BYdq7NJX…` (authority
  `3ct4z3q2…`, deployed Jul 4, upgraded Oct 27), put his wallet read-only, and once his token account, into 31
  version-1 txs on 2 of his coins (Oct 26 09:28 and Oct 27 02:59), 1-6 slots after his buy, around his sell. It is a
  fast bot (1,000 txs in 7 min, 7.93 SOL). It is **not linked** to him; it watches his position on some coins.
- **His pattern.** Nobody else uses his guards (3b), and his nonce accounts all have him as authority.
- **Other payers in his signature list since Oct 24:** 71 address-poisoning dust txs (1 to 10,066 lamports), 1 memo
  spam and the 31 DeFG8i8z txs.
- **Verdict.** He has traded from AHwJ alone since Sep 4. Before that he ran a fleet of a few hundred wallets out of
  AHwJ (Aug 25 to Sep 3), funded by Gj9srqLh. His dev wallet 4yN2vFSi was active on Oct 22.

## 4. His coins against our window: the copy key took 167 of 377, and misses his priority-fee bids

Scripts: `q4.py`, `q4b.py`. "His net" is his own result on the coin, summed over all his landed txs on it.

**Live window, Oct 26 13:00:00 to Oct 27 09:45:34 UTC (15:00 to 11:45:34 Beirut)**

| | coins | his net | per buy | wins | without best 2 |
|---|---|---|---|---|---|
| all his launch buys | **377** (check.sh: 377) | +8.9216; failed txs −0.0116 (1,074; check.sh: 1,075); balance change +8.9100 (check.sh: +8.9099) | | | |
| copy key: tip ≥ 2M or ≥ 2 SOL | **167** (check.sh "we copied": 166, +7.7826) | **+7.5211** | +0.0450 | 94 | +4.9196 |
| not key | 210 (check.sh: "we skipped" 206, +1.4461; "did not see" 5, −0.3071) | +1.4004 | +0.0067 | 93 | +0.0200 |
| tip ≥ 2M alone | 160 | +7.1584 | +0.0447 | 90 | +5.1309 |
| not key, but tip + priority ≥ 2M | **78** | **+4.8560** | **+0.0623** | 38 | +2.5355 |
| tip + priority < 2M | 139 | −3.0928 | −0.0223 | 59 | −4.4320 |

**From Oct 26 13:00 UTC to Oct 28 14:56 UTC**

| | coins | his net | per buy | without best 2 |
|---|---|---|---|---|
| all | 758 | +16.7018 (failed −0.0241) | +0.0220 | |
| copy key | 313 | +10.5868 | +0.0338 | +7.6875 |
| not key | 445 | +6.1150 | +0.0137 | +3.7933 |
| not key, tip + priority ≥ 2M | 137 | +7.1750 | +0.0524 | +4.7352 |
| tip + priority < 2M | 318 | −0.0681 | −0.0002 | −2.2292 |

- **Why 167 against 166, and +7.52 against +7.78:** check.sh buckets coins by what the bot itself saw; here they are
  bucketed from the chain.
- **Out of the window, Oct 16-28 (13 days):**

| buys | count | his net | per buy | positive days |
|---|---|---|---|---|
| copy key | 1,985 | +103.199 | +0.052 | 13 of 13 |
| not key, tip + priority ≥ 2M | 637 | +23.518 | +0.037 | 12 of 13 |
| the rest | 2,386 | +21.963 | +0.009 | 10 of 13 |

- **A bid key** (tip + priority ≥ 2M, or ≥ 2 SOL) would have taken 240 of the 377 coins, on which his own net was +10.59.
- **Caution:** that is his result, not a copy's. A copy starts about 8 points behind him (docs/17 §9), and this rule is
  untested as a copy. It is a new angle for open item 3, and the bot already sees his ComputeBudget instruction in each
  tx. (The copy test is `copy_relook` C9.)

## Limits

- Transfer chains: forward chains were followed for 12 deposits and backward funding for 12 sweepers. The 2025 chain was
  followed 2 hops each way.
- Linked-wallet activity comes from samples of 8-60 txs each. The exceptions, read in full, are 4yN2vFSi (781 txs) and
  the Oct 1 wallets (1,046 txs).
- Each fleet wallet was not checked for pump.fun trading today. 229 of the 232 sweeper accounts are closed.
