# onchain: him re-checked on chain, Oct 28 (Oct 24-28, his whole history, the wallet's links)

The on-chain re-check of operator 1 run on Oct 28 2026 over the owner's Triton endpoint: his Oct 24-28 by day, his
hold, every SOL transfer of his history, who else uses his two guard programs (nobody), who deployed them (he did),
co-signers, and his coins in the live window against the copy key. The report is `report.md`; the curated reading is
`07-restart/README.md` §1. 19,656 RPC calls (about $0.20).

## Run

The scripts read the Triton URL from the environment (`scripts/run.sh` sources `$TRITON_ENV`, default
`~/.rugsnipe/triton.env`, one line `TRITON_URL=https://<endpoint>.mainnet.rpcpool.com/<token>`; never in the repo) and
cache every raw response under `cache/` beside them, so a re-run is offline once fetched. `scripts/rpc.py` is the client
(cache, call counter, redacted errors). Work from a copy of this folder outside the repo: the cache (186 MB) and the
large data files (`rows.jsonl`, `sigs_*.json`, `trips.json`) are not committed; `data/` here holds the small results
(`flows.csv`: all 1,946 SOL transfers of his history; `counterparties.csv`: the 610 counterparties with balance and last
activity; `q3b.json`: the guard programs' signers; `q3c.json`: the programs' upgrade authority; `q1.json`, `q4.json`,
`createslot.json`, `tokens_now.json`, `cp_now.json`, `q3dev.json`, `q3hops.json`, `oct1_cps.json`, `prof_key.json`).

| step | scripts |
|---|---|
| his full signature list, then every tx since Oct 24 (failed ones too) and every successful tx before Sep 24 | `sigs.py`, `fetch.py recent`, `fetch1.py`, `fetch.py early` |
| parse (his balance delta, tip as the bot defines it, priority = fee − 5,000 per signature, slot guards) | `parse.py`, `norm.py`, `trips.py` |
| Q1 the trader by day; Q2 the hold (create slot from his slot guard, checked on 80 creates) | `q1.py`, `q1b.py`, `tables.py`, `relays.py`, `balance.py`, `createslot.py` |
| Q3 the wallet's links: flows, counterparties, chains, the fleet, the guards' users, the upgrade authority, co-signers, tokens, the dev wallet | `q3flows.py`, `flowtable.py`, `q3late.py`, `q3cp.py`, `q3nonce.py`, `q3hops.py`, `q3chain.py`, `q3fleetnow.py`, `q3origin.py`, `q3far.py`, `q3treasury.py`, `q3dev.py`, `q3prog7.py`, `q3defg.py`, `q3b.py`, `q3c.py`, `q3d.py`, `profile_w.py`, `oct1deep.py` |
| Q4 his coins in the live window against the copy key, and the priority-fee finding | `q4.py`, `q4b.py` |

## Headlines

- Same trader, lower volume: Oct 24-28 +31.32 SOL on 1,401 landed buys (307 a day on full days against 437 on Oct
  17-23; +7.0 a day against +15.3). Win 47.5%, median stake 0.593, the same tip steps, 64% in the create slot, H = 6
  or 10 planned on 91.4%, landed on the planned slot 68.5% and one slot later 27.1%.
- The wallet: funded Jan 2025 (22.97 SOL through fresh pass-through wallets), restarted Aug 17 2026 with 199 SOL from
  Gj9srqLh, launched 37 coins himself (−2.93 SOL), was the hub of a 232-wallet fleet Aug 25 - Sep 3 (3,246 SOL in,
  3,212 out through 3-hop chains; 229 of 232 closed now), deployed both guard programs on Sep 6 (he is the upgrade
  authority; 80,951 signatures on them, 0 by anyone else), ran relay-landing tests from 55 fresh wallets on Oct 1, and
  has had no SOL in or out since Oct 3. One linked wallet is still active: 4yN2vFSi (2.97 SOL), his dev wallet, which
  deployed a new unused program on Oct 22.
- The copy key (tip ≥ 2M or ≥ 2 SOL) took 167 of his 377 launch buys in the live window (+7.52 SOL for him). 78 more
  had tip + priority fee ≥ 2M and made him +4.86 (+0.062 a buy); over Oct 16-28 that bucket made +23.5 on 637 buys,
  positive 12 of 13 days. As a copy it loses: the 130 coins that key adds over the 5 days make −0.83 SOL (copy_relook C9).
