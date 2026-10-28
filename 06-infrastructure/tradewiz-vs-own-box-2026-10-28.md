# TradeWiz vs our Frankfurt box for copying him (AHwJSnFN), 2026-10-28

**Labels.** **VERIFIED** = our repo's numbers (file named), or measured by me today on chain through the public RPC
(`api.mainnet-beta.solana.com`, no keys; script and raw file named in §7). **SOURCED** = a web page (URL; date published
or fetched). **UNVERIFIED** = an inference, an estimate, or a vendor claim nobody has checked.
Times are UTC; Beirut is UTC+2 on these dates. Nothing was signed up for, sent or bought: read only.

---

## 0. The answer

**No. TradeWiz cannot do this copy, and it would be slower and dearer than our box.**

| | our box (live Oct 26-27) | TradeWiz |
|---|---|---|
| where the copy lands | 69% in his slot, 31% a slot later, median ~126 positions behind him (VERIFIED, 07-restart §2-§3) | its own published speed proof: **1 to 4 slots behind the target, median 2, none of 9 in the target's slot** (VERIFIED on chain, §2.3) |
| who to copy | his tip ≥ 2M or size ≥ 2 SOL, signers he bought ≥ 2 times in 24 h, listed signers only (VERIFIED, S6 page) | size range, market cap, liquidity, token age, platforms. **No filter on his tip or on the coin's signer** (SOURCED, settings list §2.1) |
| exit | create + H − 1, one slot before his usual sell (VERIFIED) | **on his sell** ("Copy Sell"), or a **timer in seconds** after its own buy, or TP/SL/trailing/dev-sell. Nothing tied to the create slot or to his per-operator hold (SOURCED) |
| fixed cost per 0.5 SOL round trip | **0.0046 SOL** (3M bid + 0.0016; VERIFIED, copy_relook §B, C8) | **0.0146-0.0166** at our bids (1% a side = 0.0100, plus the same bids, plus 0.002 token-account rent if it isn't reclaimed); **~0.022** at its own "Pump.fun speed" preset (SOURCED fee + preset; arithmetic mine) |
| keys | ours, on our box | **TradeWiz holds the signing key** (the bot signs every trade; a key exposure drained 20,932 user wallets on Sep 30 2026) (SOURCED) |

The 1% fee alone (0.0100 a fill) is larger than the whole curve edge the live copy earned per fill (+0.0067, VERIFIED).
At our own landing and our own exit, the 125 live fills would have netted **about −1.30 SOL instead of −0.048**
(−0.0004 − 0.0100 = −0.0104 a fill; arithmetic, VERIFIED inputs). TradeWiz cannot reach our landing or our exit,
so the real figure would be worse.

---

## 1. What TradeWiz is

| Item | Finding | Label |
|---|---|---|
| Product | Telegram trading bot built around copy trading, plus a web app (copy.fastradewiz.com) and a Chrome extension. Sniper (Pump.fun, LaunchLab/Bonk, Meteora DBC), limit orders (buy and sell, both directions), Auto Sell (TP/SL, trailing stop, Dev Sell, Time), tiered take-profit, "Reverse Copy" (buy when the target sells), Auto Trade, Smart Money wallet finder, multi-wallet | SOURCED: [tradewiz.gitbook.io/tradewiz/llms.txt](https://tradewiz.gitbook.io/tradewiz/llms.txt), [tradewizbot.pro/en/guides](https://tradewizbot.pro/en/guides) (both fetched Oct 28) |
| Chains | Solana (main bot). EVM bot for BSC and Base (live Dec 18 2025). "TradeWiz PVP" copy trading on Robinhood Chain (live Jul 15 2026, evm.fastradewiz.com, @TradeWiz_PVP_EVMbot) | SOURCED: [t.me/s/tradewizpub](https://t.me/s/tradewizpub) posts 19 and 25 (fetched Oct 28) |
| Custody | **It holds the key.** "Once you enter TradeWiz, we will create a Solana address for you" ([bot guide](https://tradewizbot.pro/en/guides/tradewiz-bot-guide)). Keys can be exported or imported. Its terms say the opposite: "Non-custodial ... TradeWiz does not hold or custody user assets. Transaction signing is performed by you" ([legal, last updated 2025-08-24](https://tradewizbot.pro/en/legal)). A copy bot that trades while you sleep must sign server-side, and the Sep 30 2026 drain used the users' own keys (§5) | Facts SOURCED (fetched Oct 28); "custodial in practice" is my reading, supported by the incident |
| Second signature | Every TradeWiz trade I sampled today carries a second signer, `7WuTYVTiYwsiWBnySR6WsDGYPwiQDF1EEb4RcZPNxy5u` (180 of 185). It is the **durable-nonce authority** (8 of 8 nonce transactions checked). Bitquery noted the same two-signature pattern | VERIFIED (on chain, §7); [Bitquery](https://bitquery.io/investigations/tradewiz-hack) SOURCED |
| Platform fee | **1% on every buy and every sell.** Plus priority fee, optional Anti-MEV (Jito) tip, pool fee, and 0.002 SOL token-account creation on the first buy of a token | SOURCED: [Fees guide](https://tradewizbot.pro/en/guides/fees), [GitBook fees](https://tradewiz.gitbook.io/tradewiz/fees.md) (fetched Oct 28) |
| Fee on chain | 2024: 5,000 lamports on 0.0005 SOL trades (exactly 1%) to `J5Mbvpsy2EMoVTZj94M6iPzHnL6Xcvx2nYK4KxjRWChD`. Oct 28 2026: round 1% amounts (0.0003 on 0.03 SOL, 0.01 on 1 SOL, 0.0259 on 2.59 SOL) to the fee wallet Bitquery named, `Aes35rP7kHZepsXrLkLkFGvqporpkHMDe9DsVoMTwJST` | VERIFIED (on chain) |
| Its own cost estimate | "A 0.5 SOL buy-and-sell round trip costs about 0.02 SOL, or roughly 4%, before slippage" (1% × 2, priority 0.002 × 2, tip 0.001 × 2, pool fee 0.25% × 2, account 0.002) | SOURCED: [blog, Aug 31 2026](https://tradewizbot.pro/en/blog/copy-trading-fees-solana-explained) |
| Suggested bids | Priority fee "0.002-0.003 SOL per trade. Above 0.005 SOL, you don't get noticeably faster"; tip 0.001-0.002. "Pump.fun speed" preset: fee 0.003 / tip 0.002 per side. Auto Trade defaults: gas 0.002, tip 0.001 | SOURCED: [settings blog, Sep 30 2025](https://tradewizbot.pro/en/blog/copy-trade-standard-settings), [Auto Trade guide](https://tradewizbot.pro/en/guides/auto-trade) |
| Anti-MEV | Sends through Jito; "with Anti-MEV on, failed trades aren't charged a fee"; Jito concurrency limits "might cause some slowdown" | SOURCED: [FAQ guide](https://tradewizbot.pro/en/guides/faq) |
| Referral / rebates | Referrer earns 25% (level 1), 3% (level 2), 2% (level 3) **of TradeWiz's 1% fee**; paid automatically at 0.05 SOL. Your own fee stays 1% ("The 1% fee on each trade is still charged as normal"). The "up to 45%" headline is not backed by these tiers | SOURCED: [Referral guide](https://tradewizbot.pro/en/guides/referral-program); [fees blog](https://tradewizbot.pro/en/blog/copy-trading-fees-solana-explained); [MadeOnSol review](https://madeonsol.com/blog/tradewiz-review-solana-copy-trading-bot) (May 31 2026, updated Sep 30 2026, affiliate) |
| Minimums | "Transfer at least 0.1 SOL ... to start trading"; keep the wallet at ≥ 0.01 SOL. Withdrawals in SOL only | SOURCED: [bot guide](https://tradewizbot.pro/en/guides/tradewiz-bot-guide), [FAQ guide](https://tradewizbot.pro/en/guides/faq) |

---

## 2. Copy-trading mechanics

### 2.1 What the settings allow (the ~30 settings of a copy task)

| Our requirement | TradeWiz | Label |
|---|---|---|
| Trigger on his landed buy | Yes: any target wallet. Platforms include PumpFun (bonding curve) | SOURCED ([copy-trading guide](https://tradewizbot.pro/en/guides/copy-trading)) |
| Pump.fun curve buys at launch | Yes. Today TradeWiz-signed pump.fun curve buys land at create + 0 and + 1 (§2.4) | VERIFIED (on chain) |
| How it detects the target's buy | **Not disclosed.** No RPC, gRPC, shred or provider named anywhere on the site, GitBook or channels | UNVERIFIED (absence on every page fetched; MadeOnSol says the same) |
| Claimed latency | "Copy smart money in 0.3s" (homepage pin); "Avg Speed 1.1s" (homepage board); "can mostly complete a trade within 1 seconds and trade in the same block as your trader" (GitBook); "within 0 seconds" (tradewizbot.pro guide) | SOURCED (claims); contradicted by its own board (§2.3) |
| Key on his tip (his conviction) | **No setting for the target's tip or priority fee** | UNVERIFIED (absent from the full settings list in the [GitBook copy task page](https://tradewiz.gitbook.io/tradewiz/copy-trade/new-copy-trade.md)) |
| Only his current operators (signer listed, ≥ 2 buys in 24 h) | **No.** There is "Only Copy Dev-Create" (copy when the target itself creates) and a Dev filter in the Sniper, nothing for the coin's creator in a copy task | SOURCED / UNVERIFIED (absence) |
| His size | "Trader Buy Limit" / "Min/Max SOL for Target Wallet": copy only when his spend is in a range | SOURCED |
| 0.5 SOL a copy | "Fixed Copy": a fixed amount per trade (or a ratio of his size) | SOURCED |
| Max premium over his fill | "Slippage: ... The buy price of the address you copied will be used as the basis for slippage." For Pump.fun, "PUMP Slippage" fixes the tokens and caps the extra SOL. Its own advice is 15-20% (33% PUMP); "Setting 5% ... most of your trades fail". Retries use "the price at the moment of the retry". The GitBook trade-settings page describes PUMP slippage the other way round (SOL fixed, fewer tokens) | SOURCED ([copy-trading guide](https://tradewizbot.pro/en/guides/copy-trading), [settings blog](https://tradewizbot.pro/en/blog/copy-trade-standard-settings), [GitBook trade settings](https://tradewiz.gitbook.io/tradewiz/trade-settings.md)); whether 5% can be set: UNVERIFIED |
| Sell one slot before his usual sell | **No.** No per-operator hold and nothing relative to the create slot | SOURCED (absence) |
| Mirror his sell | "Copy Sell" / "Sell Proportionally" / "First Copy Sell %": all react **after** his sell. Its own blog: "they sell first and you sell after, so your exit price is always lower" | SOURCED ([take-profit blog, Oct 1 2026](https://tradewizbot.pro/en/blog/take-profit-memecoin-auto-sell-trailing-stop)) |
| Time-based sell | **Yes, in seconds.** Auto Sell "Time: Set the delay before selling and the proportion of tokens to sell" (added Sep 19 2025; multi-tier time exits Nov 25 2025). The tiered-TP examples use "within 2 seconds" and "every 3 seconds". The minimum delay, its resolution and what starts the clock (its own buy, presumably) are not stated | SOURCED ([GitBook auto-sell](https://tradewiz.gitbook.io/tradewiz/auto-sell.md), [tiered TP](https://tradewiz.gitbook.io/tradewiz/auto-sell/tiered-take-profit-t-p-strategy.md), tradewizpub posts 10 and 17); resolution UNVERIFIED |
| TP / SL / trailing / dev sell | Yes, all four | SOURCED |
| Turbo Mode | Skips filters (MC, LP, renounce, size limits, proportional sell) "for maximum speed" | SOURCED ([Turbo guide](https://tradewizbot.pro/en/guides/turbo-mode)) |

### 2.2 TradeWiz's own view of copying a wallet like him

"If the target wallet is a sniper buying in the first block, an insider receiving tokens at creation, or a bundle wallet
buying alongside the dev, their entry price comes from position, not from decisions. You'll never have that position.
Every copy trade you make becomes their exit liquidity. **How to fix it: there's no settings fix. Switch wallets.**"
SOURCED: [Why You Lose Copying a Winning Wallet, Sep 15 2026](https://tradewizbot.pro/en/blog/why-you-lose-copying-a-winning-wallet).
He is exactly that wallet type: first behind the dev bundle, at create + 0/1 (VERIFIED, S6 page).

### 2.3 Its speed proof, checked on chain

The homepage "speed board" lists 9 target trades, each with the copy by TradeWiz, Maestro and Trojan as Solscan links.
I looked up all 36 transactions (slot and position in the block):

| | slots behind the target, 9 rows | median | in the target's slot | the board's "Avg Speed" |
|---|---|---|---|---|
| TradeWiz | 3, 1, 4, 2, 3, 1, 1, 2, 2 | **2** | **0 of 9** | 1.1 s |
| Maestro | 3, 1, 2, 2, 4, 7, 2, 4, 3 | 3 | 0 of 9 | 1.5 s |
| Trojan | 4, 2, 4, 4, 2, 5, 3, 11, 7 | 4 | 0 of 9 | 2.1 s |

- All 9 rows were Sep 24 2024, 09:39-09:50 UTC (slots 291,701,842-291,703,374); Raydium AMM v4 swaps of **0.0005 SOL**;
  one test target wallet (`6WJhukGv...`) and one TradeWiz wallet (`B8xM4ajV...`). A staged demo, two years old, not
  pump.fun. VERIFIED (on chain).
- Even TradeWiz's best case lands a full slot after the target. Our copy lands **in his slot 69% of the time**
  (VERIFIED, 07-restart §2). On the docs/17 §9 table his value falls to +0.10 SOL over 5 days at 150 positions behind
  him (VERIFIED); a slot later is usually several hundred positions behind (the blocks here held about 250-1,600
  transactions; VERIFIED on chain; the extrapolation is UNVERIFIED).
- There is no newer or independent benchmark. Searches found only vendor claims and affiliate reviews (UNVERIFIED).

### 2.4 TradeWiz today, on chain (Oct 28)

**Its pump.fun launch buys.** From the fee wallet's latest 1,000 transactions (10:53-15:44 UTC) I parsed 185. I could
find the create for 16 of the pump.fun curve buys. Of those 16, 1 landed in the create slot, 2 at create + 1, 1 at
+ 2, and 12 later (8 to 73,236 slots).
The create + 0 buy sat 73 positions after its create (block index 375 against 302), the 7th landed transaction on the
coin. The create + 1 buys were the 3rd and 11th transactions on their coins. These are probably Sniper-mode buys,
fired at the create, not copies. VERIFIED (on chain).

**TradeWiz on his coins.** Between 12:55 and 15:55 UTC I checked all 37 of his coins with a buy at create + 0/1
against all 579 transactions TradeWiz's co-signer signed in that window:
- TradeWiz transactions appear on 4 of the 37. Only one TradeWiz wallet bought near the launch (`7Vno6M...`, 0.03-0.06
  SOL buys, Helius Sender tip 0.0002 SOL, no priority fee):

| coin | his buy | TradeWiz buy | his sell | TradeWiz sell | that wallet's SOL change |
|---|---|---|---|---|---|
| HK9BssUT | create + 0 (idx 331) | + 1 (idx 170): the slot after his | + 10 | + 30 | −0.0206 |
| 8FGxZoeP | + 1 (idx 115) | + 1 (idx 192): his slot, 77 positions behind him | + 11 | + 5 | −0.0204 |
| GY8bt8gZ | + 1 (idx 31) | + 3: two slots after his | + 6 | + 31 | −0.0166 |

- That wallet made 10 round trips in the window, so 3 of 10 were his coins. Nothing shows that it copies him. It lost
  on all three, on 0.03-0.06 SOL buys. The fourth coin (7vB5CMev) was bought by another TradeWiz wallet at create + 410.
- **Nobody is copying him systematically through TradeWiz in this window** (4 of 37 coins). VERIFIED (on chain; a
  3-hour sample).

---

## 3. Infrastructure and sending path

| Question | Finding | Label |
|---|---|---|
| Where its servers run (Frankfurt / Amsterdam / NY ...) | **Not stated anywhere.** The site, GitBook, both TG channels and every review searched are silent on regions, nodes, RPC or feed providers | UNVERIFIED (absence) |
| Public latency benchmark | Only its own board (§2.3) and influencer posts (e.g. "1st @TradeWiz_Bot" of 6 free bots, Oct 9 2024, no method) | SOURCED (homepage testimonials); no independent test found |
| Own validators / SWQoS | No sign of either | UNVERIFIED |
| What its transactions actually do (185 sampled, Oct 28) | Its trades start with **AdvanceNonce** (a durable nonce, with the bot as nonce authority; 12 of 12 swaps decoded, and 8 of the first 10 sampled transactions: the other two were a plain transfer and one with no nonce), then 2× ComputeBudget, ATA, the swap, then two transfers: the 1% fee and a tip. That is the same fan-out-to-several-relays design our bot uses | VERIFIED (on chain) |
| Which relays land them (by tip account) | **Helius Sender 31** (median tip 0.0015 SOL), **Jito 25** (median 0.002; Anti-MEV), an unidentified relay with `BBtip...` tip accounts 23, **soyas 13**, **Falcon 7**, **NextBlock 4**, no recognized tip 82 (priority-fee only, or relays I could not name). Priority fee median 0.0001 SOL (p90 0.003). Tip accounts classified with our own lists (`crates/rugsnipe-tx/src/senders/providers.rs`, `crates/pump-codec/src/constants.rs`) and the prefixes in `analysis/research/2026-10-28/onchain/scripts/relays.py` | VERIFIED (on chain) |
| Same relays as him? | Yes. His buys land through helius 34.8%, nozomi 34.8%, node1 6.1%, soyas 4.7% ... (repo onchain report). TradeWiz rents the same commercial relays we do, so its edge, if any, would have to come from detection | VERIFIED (`analysis/research/2026-10-28/onchain/report.md`) |
| Its own words on where time goes | Detect → parse → decide → build → sign → submit → land; "Where does this bot remove latency?" No numbers, no providers | SOURCED ([blog, Aug 17 2026](https://tradewizbot.pro/en/blog/where-copy-trade-speed-is-lost)) |

For comparison, our box sits under 0.5 ms from every sender, and the feed, not the box, accounts for most of the ~90-126
positions we land behind him (VERIFIED, `06-infrastructure/box-and-feed-2026-10-28.md` §0, §2).

---

## 4. Economics for this exact use

### 4.1 Cost per filled copy, 0.5 SOL round trip

The pump.fun curve fee (1.25% a side) is the same either way and is already inside our curve P&L (VERIFIED, docs/02
§Fees; five/copy `second.py`).

| item | ours, live 3M bid | TradeWiz, our bids | TradeWiz, its "Pump.fun speed" preset |
|---|---|---|---|
| platform fee, 1% × 2 sides | 0 | 0.0100 | 0.0100 |
| buy and sell bids (tips and priority) | 0.0030 + part of 0.0016 | same as ours | 0.005 + 0.005 = 0.0100 |
| the rest (sell tip, base fees, refused-copy fees ...) | 0.0016 | same as ours | ~0.0001 |
| token-account rent | (not separated in our 0.0016) | +0.002 if not reclaimed (TradeWiz calls it a cost) | +0.002 |
| **total a fill** | **0.0046** (0.9%) | **0.0146-0.0166** (2.9-3.3%) | **~0.022** (4.4%) |

Ours: VERIFIED (copy_relook §B: 0.00465 a fill at 3M; §C8 "bid + 0.0016"). TradeWiz: SOURCED fee and preset, my
arithmetic. TradeWiz's own figure for a 0.5 SOL round trip is ≈ 0.0205 SOL (4.1%) (SOURCED).

### 4.2 What the 1% does to the copy, with everything else ours

| sample | as measured (ours) | with TradeWiz's 1% × 2 added (0.0100 a fill) |
|---|---|---|
| live, 125 fills, Oct 26-27 | curve +0.834, costs 0.882, **net −0.048** (−0.0004 a fill) | **≈ −1.30 SOL** (−0.0104 a fill); ≈ −1.55 if the 0.002 rent is lost |
| backtest 5 days, 2M key, live costs at 3M | **+7.77** on 298 copies (0.78 fills a copy ≈ 232 fills) | ≈ **+5.45** (−2.32) |
| backtest Oct 24-25 (the period most like live) | −0.0004 a fill at the live bid mix | ≈ −0.0104 a fill |

Inputs VERIFIED (07-restart §2; copy_relook §B). The subtraction is arithmetic. It assumes TradeWiz lands and exits
as we do, which it cannot (§2), so these are upper bounds.

### 4.3 What its exits are worth against our H − 1 (docs/17 §9, 0.5 SOL, our landing)

| exit | result over 5 days (Oct 21-25) | which set | source |
|---|---|---|---|
| **H − 1** (ours) | **+5.64** | ablation, 4M key, as live then | docs/17 §9 "Every rule tested" |
| H (his own sell slot) | +2.98 | same | same |
| H − 2 | +3.95 | same | same |
| flat create + 5 | +4.43 | same | same |
| flat create + 9 | +3.91 | same | same |
| H − 1 | **+6.55** (338) | his 0.7 SOL+ buys, listed signers | docs/17 §9 `scratch.py` |
| H / H − 2 / H − 3 | +2.76 / +5.30 / +4.09 | same | docs/17 §9 |
| H − 1, unlisted signers, best exit tried | −2.25 (313, flat + 5) | his 0.7 SOL+ buys | docs/17 §9 |
| H − 1, all his buys | +5.95 listed (780) / −6.13 unlisted (904) | all his buys | docs/17 §9 |
| **sold after seeing his sell** (= Copy Sell) | **−23.4** | all his buys | docs/17 §9; S6 page |

All VERIFIED (repo). **A disagreement in the brief:** "H − 2 +5.30" belongs to the `scratch.py` table (0.7 SOL+,
listed), not the ablation. In the ablation H − 2 is +3.95.

**What TradeWiz can actually set up for him:**
- **Copy Sell.** That is the −23.4 SOL row: his sell is the dump.
- **A seconds timer.** Its buy lands about create + 1 to + 5 (his create + 0/1 plus its 1-4 slots). A 1 s delay is
  ~4-5 slots at ~225 ms (07-restart §1), plus the time to see its own fill and send the sell. That puts the sell around
  create + 7 to + 12 (UNVERIFIED estimate). That is after his sell on his 6-slot operators and around it on his
  10-slot ones. The nearest backtest row is flat + 9: +3.91 against +5.64 for H − 1, and that is at our landing, with
  our tip and operator keys, and before the 1% fees. A 2 s timer lands after both his hold lengths.
- **No tip or operator key.** TradeWiz would copy every buy in the size range, so the base set is "all his buys" (−0.18
  at H − 1 with our landing) or "his 0.7 SOL+ buys" (+6.55 listed, −2.25 unlisted). It is not the +8.02 tip-keyed set.
- **Landing.** At TradeWiz's measured lag (§2.3) a copy sits past D = 150, where the D-table is already +0.10 over 5
  days (VERIFIED), and a 5% bound would refuse more copies.

Combining these, every TradeWiz configuration is negative before its fees. The direction is clear from VERIFIED rows;
the size is UNVERIFIED (no backtest at its exact lag and timer).

---

## 5. Reputation and risk

| Item | Finding | Label |
|---|---|---|
| Age | Influencer posts from Jul 11 2024 on (X status IDs decoded); its X scam warning Aug 2 2024; copyright "2024-2026". Bitquery: > 35,000 wallets paid the fee wallet or its predecessor since August 2025 | SOURCED (homepage links, [X post](https://x.com/TradeWiz_Bot/status/1819316289803862029), [Bitquery](https://bitquery.io/investigations/tradewiz-hack)) |
| Activity today | 1,000 fee-wallet transactions in 4 h 51 min (10:53-15:44 UTC), about 5,000 a day; 579 co-signed transactions in 12:55-15:55 | VERIFIED (on chain) |
| Team | Anonymous. No company, address or legal entity on any page. A "Marketing & Partnerships Manager" (@RedWorldo) is shown | SOURCED ([MadeOnSol](https://madeonsol.com/blog/tradewiz-review-solana-copy-trading-bot); homepage) |
| Audits | None published, none found | UNVERIFIED (absence) |
| **Incident, Sep 30 2026** | "Private key exposure in the key export feature of SOL PVP wallets". Bitquery: **20,932 wallets** touched Sep 28 - Oct 1 (test run Sep 28 18:40); main drain Sep 30 13:25-15:52 UTC; **3,523.29 SOL swept + 189.31 SOL of reclaimed rent + ~$14k of tokens ≈ $459k** at $120/SOL; plain transfers signed with the victims' own keys; 73% taken after the bot had stopped trading (14:06) | SOURCED ([Bitquery](https://bitquery.io/investigations/tradewiz-hack), figures verified Oct 1 2026, correction Oct 15; [Bitcoin.com, Oct 2 2026](https://news.bitcoin.com/the-459000-bot-hacker-was-a-customer-first-researchers-say/)) |
| Their response | Police report Oct 1; "more than 1,000 affected users have been compensated" (self-reported); **bot offline until Oct 13 2026**; everyone who used it before Sep 30 told to open a new Telegram account; old-wallet losses after Oct 2 not compensated; EVM services paused for checks | SOURCED ([incident page, Oct 22 2026](https://tradewizbot.pro/en/blog/tradewiz-security-incident-new-account); Bitcoin.com) |
| Earlier FAQ promise | "By not exporting your private keys, we can ensure 100% security of your assets" (quoted by Bitcoin.com). The drain came through that export path | SOURCED |
| Official handles | Official GitBook links: Sol bot **@TradeWizFast_Solbot** ("TradeWiz Bot_Merlin｜IGNORE ADS", 15,725 monthly users), group @TradeWiz_Official (12,493), updates @tradewizpub, X @TradeWiz_Bot, website **fastradewiz.com** (its Start link carries ref "OFFICIALWEB"). In Aug 2024 its X named @TradeWiz_Solbot as the only real bot. @TradeWizSolbot ("TradeWiz Bot_Merlin", 64,069 monthly users) also exists | SOURCED ([GitBook links](https://tradewiz.gitbook.io/tradewiz/links.md); t.me previews fetched Oct 28; X post) |
| **Is tradewizbot.pro the real one?** | **Probably a TradeWiz-run or affiliate second site, not confirmed.** It carries the guides, the incident notice and the same Solscan proof as fastradewiz.com, and its own Links page lists itself as "Website 2". **But:** the official GitBook links list only fastradewiz.com. Its "Start Bot" redirects (bot.tradewizbot.pro → 302) to a different handle, **@TradeWizLoki_Solbot**, with a referral code. The same referral code is on its extension link. Its homepage also carries a GMGN referral link ("Join GMGN"). No official channel I could read names "Loki". MadeOnSol (affiliate) calls tradewizbot.pro official | SOURCED (fetched Oct 28); official status UNVERIFIED |
| Impostors | tradewiz.live: a separate "investment broker" site with withdrawal-block complaints (Trustpilot; MadeOnSol calls it a confirmed scam). tradewiz.com is a parked domain for sale (Sedo). Its own warnings: "TradeWiz staff will never DM you first" | SOURCED ([Trustpilot](https://www.trustpilot.com/review/tradewiz.live); curl Oct 28; [support guide](https://tradewizbot.pro/en/guides/support)) |

---

## 6. Verdict

**TradeWiz cannot do this copy.** It can be told to copy his wallet's pump.fun buys at a fixed 0.5 SOL with a price
bound off his fill. Every part that makes our copy break even is missing:
- **His tip and his current operators.** TradeWiz has no filter on the target's tip and none on the coin's signer.
- **The landing.** Its own published proof lands 1-4 slots behind the target (median 2, none of 9 in the target's
  slot). Our box lands in his slot 69% of the time. It rents the same relays we do (Helius Sender, Jito, NextBlock,
  Falcon, soyas) and discloses no feed or region, so nothing suggests it lands closer.
- **The exit.** It cannot sell one slot before his sell. It can sell after his sell (Copy Sell), which the 5-day
  backtest puts at −23.4 SOL on all his buys. Or it can sell on a seconds timer from its own buy, which reaches about
  create + 7 to + 12. That is at best the flat + 9 row (+3.91 against +5.64 for H − 1, at our landing), and behind his
  dump on his 6-slot operators.
- **The price.** At 1% a side it charges 0.0100 SOL per 0.5 SOL round trip before any tip. That is more than the whole
  curve edge per fill the live copy earned (+0.0067), and it makes the total 0.0146-0.022 against our 0.0046. With our
  landing and our exit it would have turned the live −0.048 into about −1.30 SOL. With its own landing and exits it
  would be worse.
- **The key.** It holds the signing key, and that key path was drained on Sep 30 2026 (20,932 wallets, ≈ $459k).

**Not closer, not cheaper, not able to exit before him: no.**

---

## 7. What I measured and where it is

Scripts are in `(the session scratchpad, not in the repo)` and raw
outputs in `(the session scratchpad, not in the repo)`. Everything
went through the public RPC with no keys, 15:30-16:10 UTC Oct 28.

| what | script | raw output |
|---|---|---|
| the speed board's 36 transactions: slot, index, programs, fees | `speedcheck.py` (rows parsed from the homepage HTML, `speed_rows.tsv`) | `speedcheck.json` |
| 185 TradeWiz transactions from the fee wallet `Aes35rP7...`: kinds, signers, nonce, tips by relay, priority | `twsample.py` (+ `tipaccts.json`, built from our repo's tip lists) | `tw_oct28_tx.json` |
| TradeWiz pump.fun curve buys: create slot, block index | `createslot.py` (then a fully paginated re-run for the near-create four) | `tw_oct28_pumpbuys.json`, `tw_nearcreate.json` |
| his 37 launch coins (12:55-15:55 UTC) against all TradeWiz co-signed transactions | `himvstw.py` | `him_vs_tw.json` |

**Caveats:**
- The speed board is TradeWiz's own staged sample from Sep 2024, on Raydium, at 0.0005 SOL.
- The Oct 28 samples are a few hours long.
- A create is "resolved" only when the coin's full signature history could be paged (16 of 29 pump buys).
- The relay names `BBtip...` and the unrecognized recipients are not identified.

## 8. Sources

Repo (VERIFIED): `07-restart/README.md` §1-§3, §5; `03-strategies/S6-copy-him.md`;
`06-infrastructure/box-and-feed-2026-10-28.md` §0, §2; `docs/17-newest-bot-vs-him-5-days.md` §9 (the exit, copying his
landed buy, the D-table, "Every rule tested"); `analysis/research/2026-10-28/copy_relook/report.md` §B, §C8;
`analysis/research/2026-10-28/onchain/report.md` (his relays); `docs/02-pumpfun-mechanics.md` (fees);
`docs/research/rugger-ecosystem-2026.md` §6 (the earlier note on TradeWiz).

Web (SOURCED; fetched Oct 28 2026 unless dated):
- https://tradewizbot.pro/en (homepage: fees FAQ, speed board, testimonials, copyright 2024-2026)
- https://tradewizbot.pro/en/guides and /en/guides/{fees, faq, copy-trading, turbo-mode, auto-sell, trailing-stop,
  sniper, auto-trade, tradewiz-bot-guide, referral-program, links, support, web-new-copy-trade, web-trade-settings}
- https://tradewizbot.pro/en/legal (last updated 2025-08-24)
- https://tradewizbot.pro/en/blog/tradewiz-security-incident-new-account (Oct 22 2026)
- https://tradewizbot.pro/en/blog/copy-trading-fees-solana-explained (Aug 31 2026)
- https://tradewizbot.pro/en/blog/copy-trade-standard-settings (Sep 30 2025)
- https://tradewizbot.pro/en/blog/why-you-lose-copying-a-winning-wallet (Sep 15 2026)
- https://tradewizbot.pro/en/blog/take-profit-memecoin-auto-sell-trailing-stop (Oct 1 2026)
- https://tradewizbot.pro/en/blog/where-copy-trade-speed-is-lost (Aug 17 2026)
- https://tradewizbot.pro/en/blog/best-solana-copy-trading-bots-2026 (Oct 18 2026)
- https://tradewiz.gitbook.io/tradewiz/llms.txt and the .md pages: auto-sell, auto-sell/tiered-take-profit-t-p-strategy,
  copy-trade/new-copy-trade, trade-settings, fees, links, wallet, snipe, copy-trading
- https://fastradewiz.com (official website per GitBook; Start link to @TradeWizFast_Solbot)
- https://t.me/s/tradewizpub (posts 9-28, Aug 27 2025 - Sep 13 2026); t.me previews of @TradeWizFast_Solbot,
  @TradeWizLoki_Solbot, @TradeWiz_Solbot, @TradeWizSolbot, @TradeWiz_Official
- https://bitquery.io/investigations/tradewiz-hack (on-chain figures verified Oct 1 2026; correction Oct 15 2026)
- https://news.bitcoin.com/the-459000-bot-hacker-was-a-customer-first-researchers-say/ (Oct 2 2026)
- https://madeonsol.com/blog/tradewiz-review-solana-copy-trading-bot (May 31 2026, updated Sep 30 2026; affiliate)
- https://x.com/TradeWiz_Bot/status/1819316289803862029 (Aug 2 2024, scam alert naming @TradeWiz_Solbot)
- https://www.trustpilot.com/review/tradewiz.live (tradewiz.live, unrelated)
