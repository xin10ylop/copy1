# 07. Restart the copy of him (plan of 2026-10-28)

> **In short** (filled in at the end of the review)
>
> [PENDING: verdict, the three changes that matter, the numbers]

Everything below is dated Oct 28 2026. Times are UTC unless marked Beirut (UTC+2). Every figure has a source: a
page of this repo, a script, or a paste of the owner's. Nothing is running: fra1 was terminated on Oct 28.

## 1. Where he stands today (Oct 28)

[PENDING: the on-chain re-check: Oct 24-28 by day, tips, hold, the wallet's links]

What was checked from this session directly (Triton JSON-RPC, 15:00 UTC):
- He is trading now: his newest transaction at 15:01:18 UTC (`operators_refresh.py --source rpc --hours 2`).
- His balance: 249.068 SOL (`getBalance`).
- His last two hours (13:03-15:01 UTC): 66 landed trades on 33 coins, 33 round trips, +1.018 SOL, 106 failed
  transactions. Sell slot minus create slot: 10 on 18 coins, 6 on 14, 3 on 1 (33 of 33 in his usual set). His buy
  landed at create + 0 on 22 and + 1 on 11. His stakes 0.403-2.426 SOL (0.403 the most common). Only 4 of the 26
  signers in the window had two of his buys. Source: the refresh script's own log, run from this container.

## 2. What the live copy really did (Oct 26 15:00 - Oct 27 11:45 Beirut), decomposed

The `== 1 him` table of [`05-live/check-sh-2026-10-27.txt`](../05-live/check-sh-2026-10-27.txt), 377 rows, parsed
row by row (script in §8). The stake of each filled copy is OUR NET / our %.

| the 125 filled copies | SOL |
|---|---|
| curve P&L (sold minus paid, before costs) | **+0.834** |
| tips and fees on those 125 fills | **-0.882** |
| net | -0.048 |

**The copies made money on the curve and the fixed costs ate all of it.** The stake was 0.5 SOL on 122 of 125
(median 0.499); only the last three, on Oct 27 morning, were smaller as the wallet emptied (`stake_fits_balance`).

| cut | n | won | our net | fees | curve | his net on the same coins | per copy |
|---|---|---|---|---|---|---|---|
| bid 3.0M | 64 | 25 | +0.439 | 0.298 | +0.736 | +2.22 | +0.0069 |
| bid 8.0M | 61 | 19 | -0.486 | 0.584 | +0.098 | -0.19 | -0.0080 |
| Oct 26 (Beirut day) | 69 | 25 | +1.052 | 0.457 | +1.510 | +5.52 | +0.0153 |
| Oct 27 | 56 | 19 | -1.100 | 0.425 | -0.675 | -3.48 | -0.0196 |
| his tip 2-4M | 38 | 18 | -0.012 | 0.272 | +0.259 | +0.36 | -0.0003 |
| his tip 4.8-7.2M | 41 | 5 | -1.437 | 0.298 | -1.139 | -1.70 | -0.0351 |
| his tip 8M+ | 46 | 21 | +1.402 | 0.312 | +1.714 | +3.37 | +0.0305 |
| his size >= 2 SOL (`copy_big_sol`) | 9 | 2 | -0.509 | 0.063 | -0.446 | -2.58 | -0.0566 |
| landed in his slot | 86 | 29 | -0.456 | 0.609 | +0.153 | +0.01 | -0.0053 |
| landed one slot later | 38 | 15 | +0.410 | 0.263 | +0.673 | +1.97 | +0.0108 |

- **The 8M bid cost 0.005 SOL more per fill and landed 7 positions closer** (TIP TEST, d_avg 149 against 156).
  Over 61 fills that is -0.30 SOL of tips for nothing. The 3M arm alone was +0.44 SOL on 64 copies.
- **Oct 26 was in line with the backtest** (+0.015 a copy; the backtest's +8.02 over 298 copies is +0.027 at 0.5
  SOL). **Oct 27 was his weak day** (he lost -3.48 on the coins we copied, -0.72 on the day's 156 rows), and the copy
  lost more than him, as docs/17 §9 warned it does on his weak days.
- **Seven dumps did it**: CSMc5K1u -0.305, HvjYQ3VW -0.298, DR8or4ud -0.284, 3Ye1Wgff -0.278, 7QsUeqFq -0.270,
  4s85HKoM -0.235, 4q3ser1u -0.167: -1.84 SOL, five of them between 03:49 and 03:57 Beirut on Oct 27. He lost on six of
  the seven himself. Without the two worst the fills were +0.56; without the two best, -1.09.
- **The 33 refused copies**: his net +4.63 on them, 18 at tips of 8M or more. 15 of the 33 landed a slot after him
  (the reactors with 18-50M tips went first, docs/19 §9). Every fix for refusals tested negative over 5 days (docs/19
  §9-§10); nothing here changes that.
- **His 4.8-7.2M tips lost 5 of 41 live.** In the 5-day backtest that bucket was positive (docs/17 §9: 2-4M copies
  +2.37 on 66, positive every day; the backtest keyed at 2M on all buckets). [PENDING: the re-run by bucket]

## 3. Every decision, re-explored

[PENDING: the table rule by rule: kept / changed / why, with the re-run's numbers]

## 4. What changed in this commit (code and config)

| change | file | why |
|---|---|---|
| **him-only config template** | `config/copy-him.example.toml` | the live file was probe-a plus edits nobody has (the box is gone). This one carries the copy's every key with its reason, validated with `rugsnipe-ctl config validate` against a signed stage-b ArmSet (only the credential and feed refusals remain, as for probe-a) |
| **the copy counter is seeded from chain** | `analysis/scripts/strategy/operators_refresh.py --copy-signers-seed`, `deploy/systemd/rugsnipe-operators.service` | `copy_signer_min_buys = 2` counts his buys per signer live and starts empty on a fresh box: a count started empty keeps 99 of the 226 copies (docs/17 §9). The refresh now writes his last 24 h of launch buys per signer as `copy_signers.json`, the file the hot unit loads at start, whenever the hot unit is not running. Tested against today's chain: 26 signers, 33 buys in 2 h, 135 RPC calls, 18 s |
| **the ArmSet's size is a flag** | `analysis/scripts/make_paper_armset.py --size-sol` | the copy's stake is min(ArmSet size, `[probe] b.max_probe_lamports`, `entry.stake_by_tier[0]`). Stage b's default size is 0.25 SOL; the live copies staked 0.5, so the live ArmSet was signed by hand. `--probe-stage b --size-sol 0.5` makes it a command |
| **check.sh reconciles the wallet** | `deploy/bin/rugsnipe-check` | "results since the start" counted closed trades only (-0.76 while the wallet lost 1.41). It now prints the open positions at cost and the rest (failed sells' fees, nonce rent), and warns when more than 0.02 SOL left the wallet outside closed trades and open positions |

[PENDING: anything the code review adds]

## 5. The box

[PENDING: the infrastructure review]

## 6. Runbook: from the Ohio backup to the first copy

Everything the owner runs, one block each, with what it should print. `~/rugsnipe` is a clone of **this repo
(copy1)** on each box: the code is the Oct 28 snapshot plus this commit. (The upstream `xin10ylop/rugsnipe` does not
carry this commit; point the boxes here.)

### 6.0 On Ohio now: what the backup holds (prints names and config lines, never key contents)

```bash
sudo ls -la /root/fra1/etc/rugsnipe/ /root/fra1/etc/rugsnipe/keys/ /root/fra1/var/lib/rugsnipe/
sudo grep -nE '^(mode|stage|rule_buys|copy|follow|max_buys_per_hour|spread|max_probe|max_snipe|max_daily|stake|lamports|ab_by_tier|by_tier|sell_tip|dump_tip|hold_to|max_premium|operators_file|tweet|dumper|leader_regions|min_hot|cu_limit)' /root/fra1/etc/rugsnipe/rugsnipe.toml
sudo python3 -I -c 'import json;d=json.load(open("/root/fra1/var/lib/rugsnipe/copy_signers.json"));print(len(d),"signers",sum(len(v) for v in d.values()),"of his buys kept")' 2>&1 | tail -1
```
What it should print: the key files `probe-keypair.json` and `api-keys.toml` listed (0400); the config lines, among
them `copy_signer_min_buys = ...` (this settles the "operator he bought < 0 times" question of the S6 page: if it
reads 0, the operator rule was off live); the copy counter's signer count, or "No such file" if the backup has none.
**Paste the output back.** It holds no secret: the config names credentials, it never holds them.

### 6.1 Rent the box and accept it

[PENDING: the box choice] Then `deploy/frankfurt-checklist.md` §2: `bash deploy/latency_probe.sh 30` on the test IP,
accept only below 0.2 ms to `64.130.50.88` (Jito FRA) and `64.130.50.91` (Helius fra-sender).

### 6.2 Install (on the box, as the ops user)

```bash
cd ~ && git clone https://github.com/xin10ylop/copy1 rugsnipe && cd rugsnipe && git checkout claude/affectionate-allen-nrv6o7
git config core.hooksPath .githooks
bash deploy/install.sh --role hot --dry-run | tail -20
sudo bash deploy/install.sh --role hot
sudo /opt/rugsnipe/bin/tune-hot.sh --apply && sudo systemctl enable rugsnipe-tune.service
cat /opt/rugsnipe/REVISION
```
What it should print: the dry run's planned actions, then the real install ending in the REVISION line with this
commit's hash and `role=hot`. The build takes 10-20 minutes the first time (`cargo build --release --locked`).

### 6.3 Keys: copy the two files from the backup, never their contents

On your laptop (two hops through it; `OHIO` and `BOX` are the hosts):
```bash
scp -3 ubuntu@OHIO:/tmp/k/probe-keypair.json ubuntu@OHIO:/tmp/k/api-keys.toml ops@BOX:/tmp/
```
Before that, on Ohio, root copies them to a place `ubuntu` can read, and removes that copy right after:
```bash
sudo mkdir -p /tmp/k && sudo cp /root/fra1/etc/rugsnipe/keys/probe-keypair.json /root/fra1/etc/rugsnipe/keys/api-keys.toml /tmp/k/ && sudo chown ubuntu /tmp/k/* && sudo chmod 600 /tmp/k/*
# ... scp ...
sudo rm -rf /tmp/k
```
On the box:
```bash
sudo install -d -m 0700 /etc/rugsnipe/keys && sudo install -m 0400 -o root -g root /tmp/probe-keypair.json /tmp/api-keys.toml /etc/rugsnipe/keys/ && rm -f /tmp/probe-keypair.json /tmp/api-keys.toml
sudo nano /etc/rugsnipe/keys/api-keys.toml
```
In the editor, set these lines (values from the Triton portal's **backend** endpoint; every value in double quotes):
```toml
GRPC_TOKEN = "<the token part of the backend URL, after the last />"
TRITON_URL = "https://<endpoint>.mainnet.rpcpool.com/<token>"
RPC_URL = "https://<endpoint>.mainnet.rpcpool.com/<token>"
```
Keep `HELIUS_KEY`, `NOZOMI_KEY`, `ASTRALANE_KEY`, `BLOCKRAZOR_KEY`, `TG_TOKEN`, `TG_CHAT` as they were. Then
`sudo chmod 0400 /etc/rugsnipe/keys/*`. The probe wallet is the old one, `4g49xGbgHZk3QYR1o6QSfDUbHmJZFwN6iDp6Vco1skff`
(emptied Oct 27, its token accounts closed). **The Triton token was pasted in a chat on Oct 28: rotate it in the
portal once the box is stable, then update these two lines.**

### 6.4 The ArmSet (on Ohio, where the signing key is), stage b at 0.5 SOL

```bash
cd ~/rugsnipe && git fetch -q origin claude/affectionate-allen-nrv6o7 && git checkout -q claude/affectionate-allen-nrv6o7 && git pull -q
sudo rm -rf /tmp/armset-copy-b
python3 -I analysis/scripts/make_paper_armset.py --kind class --ver 201 --probe-allowed --probe-stage b --size-sol 0.5 --valid-hours 360 --out /tmp/copy-b.json
sudo /opt/rugsnipe/bin/rugsnipe-ctl armset sign --key /etc/rugsnipe/keys/armset-signing.key --in /tmp/copy-b.json --out-dir /tmp/armset-copy-b
ls /tmp/armset-copy-b/
```
What it should print: `valid 360 h (until <15 days ahead>)`, then `ver 201 sha256 <64 hex> signer <pubkey> ...
probe_allowed=true`, and two files `armset-201-SHA.json` and `.json.sig`. Write the SHA down. Copy the two files to
the box (`scp -3` through the laptop as above) into `/var/lib/rugsnipe/armsets/` with
`sudo install -m 0640 -o rugsnipe -g rugsnipe`. The signer pubkey printed here is `[secrets] armset_pubkey` below.

### 6.5 The config

```bash
sudo install -m 0640 -o root -g rugsnipe /opt/rugsnipe/src/config/copy-him.example.toml /etc/rugsnipe/rugsnipe.toml
sudo nano /etc/rugsnipe/rugsnipe.toml      # armset_pubkey, cold_wallet (your Phantom 4ZLrCvjc...), grpc.url (https://<endpoint>.mainnet.rpcpool.com)
sudo /opt/rugsnipe/bin/rugsnipe-ctl config validate /etc/rugsnipe/rugsnipe.toml --armset /var/lib/rugsnipe/armsets/armset-201-SHA.json --clock-offset-ms 0.05 --post-exec-healthy
```
What it should print: `armset: ArmSet ver 201 ... probe_allowed=true probe_stage=b`, then exactly two REFUSED lines,
`credential "probe-keypair" missing` and `credential "api-keys" missing` (the known false alarm of this check; the dry
run of 6.8 is the real one). Any other REFUSED line: stop and paste it.

### 6.6 Nonces (0.042 SOL of rent for 32 buy and 8 sell accounts) and funding

Send **2.5 SOL** from Phantom to `4g49xGbgHZk3QYR1o6QSfDUbHmJZFwN6iDp6Vco1skff` first (0.5 x 2 open copies, the
0.1 floor, the nonce rent, tips, and room for the 1 SOL daily stop). Then:
```bash
sudo /opt/rugsnipe/bin/rugsnipe-ctl nonce create --keypair /etc/rugsnipe/keys/probe-keypair.json --rpc-url cred:RPC_URL --count 32 --dry-run | tail -3
sudo /opt/rugsnipe/bin/rugsnipe-ctl nonce create --keypair /etc/rugsnipe/keys/probe-keypair.json --rpc-url cred:RPC_URL --count 32 | tail -2
sudo /opt/rugsnipe/bin/rugsnipe-ctl nonce create --keypair /etc/rugsnipe/keys/probe-keypair.json --rpc-url cred:RPC_URL --count 8 --pool sell | tail -2
```
What it should print: the dry run's `would create` rows and `DRY RUN: nothing was signed or sent`; then
`done: created 32, existed 0, failed 0` and `done: created 8, existed 0, failed 0`. **Never start the hot unit before
both say done** (docs/08 §9 step 3c: a missing pool account is quarantined for good).

### 6.7 The operator table and the copy counter's seed (hot unit NOT running)

```bash
sudo systemctl start rugsnipe-operators.service; sudo journalctl -u rugsnipe-operators -n 12 --no-pager
sudo python3 -I -c 'import json;d=json.load(open("/etc/rugsnipe/operators.json"));print(len(d),"signers in the table")'
sudo python3 -I -c 'import json;d=json.load(open("/var/lib/rugsnipe/copy_signers.json"));print(len(d),"signers,",sum(len(v) for v in d.values()),"of his launch buys,",sum(1 for v in d.values() if len(v)>=2),"signers with 2+")'
```
What it should print: the refresh's lines `(a) ... landed trades`, `(b) ... round trips`, `wrote N signers`, and
`copy seed: N signers, M of its launch buys ... -> /var/lib/rugsnipe/copy_signers.json`; then the two counts. The
table needs 20 round trips in his last 24 h (he does 400-600 a day). If the service fails, paste its journal.

### 6.8 The Jito relay, the dry run, the start

Jito relay: the four install lines at the top of `deploy/nginx/jito-relay.conf`, then its curl check. Then docs/08 §9
steps 5 (dry run), 6a (no stray tokens in the wallet), 6b (the hot unit's drop-in with `--armset
/var/lib/rugsnipe/armsets/armset-201-SHA.json --rpc-url cred:RPC_URL`), 6c (`install.sh --role hot --probe-armset
...`, enable guard, hot and the target), 6d (`sudo systemctl start rugsnipe.target`). Then:
```bash
cp ~/rugsnipe/deploy/bin/rugsnipe-check ~/check.sh && bash ~/check.sh start && bash ~/check.sh
```
What it should print: `TRADING: yes`, the wallet line, `buys: copies of his buys only (entry.rule_buys = false)`,
and the copy line `copy on (this process): his launch buys N  not copied: tip under 2M ..., operator not listed ...,
operator he bought < 2 times in 24 h ...` (the `< 2` must read 2). Paste the first `bash ~/check.sh` back.

### 6.9 The first day's rules

- Read `bash ~/check.sh` every few hours and `bash ~/check.sh him` once a day; paste them.
- The TIP TEST decides the bid: keep 1.5M only if it lands no farther behind him (d_avg) and nets more per copy than
  3.0M. [PENDING: the backtest's cost-per-bid table]
- The daily stop (1 SOL) now stops his copies alone, since nothing else trades. If it latches on a day he loses, that
  is the stop doing its job: unkill the next day (06-infrastructure §4), do not raise it.
- Any `CRITICAL` in the journal, or the new check.sh WARNING line (SOL leaving the wallet outside trades): stop and paste.

## 7. Open questions

[PENDING]

## 8. Sources

- [`05-live/check-sh-2026-10-27.txt`](../05-live/check-sh-2026-10-27.txt), parsed by `analysis/research/2026-10-28/live_decomp/live_decomp.py` (§2).
- [`03-strategies/S6-copy-him.md`](../03-strategies/S6-copy-him.md), [`02-his-rules/README.md`](../02-his-rules/README.md), docs/17 §9-§10, docs/19 §9-§10.
- `docs/08-runbook.md` §9 (the probe steps this runbook follows), `docs/07-deploy.md` §5-§6.
- [PENDING: the four reviews of this session, in `analysis/research/2026-10-28/`]
