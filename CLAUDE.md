# CLAUDE.md: guide for agents working in copy1 (operator 1, "him")

## What this repo is

The "him" half of the rugsnipe project. Him = operator 1 = `AHwJSnFNUiAU9FfT5ewW2osqMo938WtL7KhfsJyfpaN2`. The strategies
built on him are S0-S7. S6, the direct copy, traded real money. The hot copy bot is `crates/rugsnipe` (`rugsnipe-hot`),
configured by `config/rugsnipe.example.toml`. It is **stopped**, and its server fra1 was terminated on Oct 28.

Read `README.md` (status, A-Z index), then `01-who-he-is/` and `02-his-rules/`, then `03-strategies/README.md`. The
original project docs are in `docs/`: 09-19 cover him and the copies, 00-08 the background. The sister repo **copy2**
holds wallet 4 (H9kuqGKN), its long copy (paper, running on the Ohio box) and its launch copy. The code is identical in
both repos.

**Upstream:** the live code is developed in `xin10ylop/rugsnipe`, branch `claude/eloquent-mayer-264bxk`. This repo is a
snapshot at `7184554` (Oct 28). Code meant for a box goes upstream (or the box gets pointed here); say which you did.

## The owner and how to work with them

- The owner runs every command on the boxes and pastes the output back. You can't reach the boxes. Give one copy-paste
  block, say what each line should print, and say which machine it runs on. Begin with `cd ~/rugsnipe` when you use repo
  paths.
- **Answer the question asked, directly**, yes or no first, then the evidence. Plain words, short sentences, tables.
  Times: the owner reads Beirut time (UTC+2 on these dates); say which zone.
- **Never invent numbers.** Every figure in these docs has a source (a doc §, a research script, a pasted output).
  When sources disagree, say so; the chain decides. The strategy pages flag every known disagreement.
- Be honest about losses and your own bugs. The copy bot lost −5.13 SOL live. The stuck coin was a code bug.

## Security (hard rules)

- **This repo is public.** Never commit private keys, API keys, RPC URLs with keys, a box's `/etc/rugsnipe/*.toml`,
  `*.tok` files, or the fra1 backup. Enable the hook: `git config core.hooksPath .githooks`.
- Never print or ask for the contents of a key file. The SSH key is the owner's; never ask for it or display it.
- fra1's backup (`/root/backups/fra1-backup.tgz` on Ohio, wallet and API keys inside) stays private: not in git, not
  shared, not in cloud sync.
- Don't publish the owner's IP, local username or server addresses in new files.

## Build and test

```
cargo build --release                      # toolchain pinned in rust-toolchain.toml
cargo test -p rugsnipe                     # the hot bot (copy, copy_more, follow, graduation, sell lifetime ...)
cargo test -p rugsnipe-exit -p rugsnipe-tx -p pump-codec
```
On a box: `sudo bash deploy/install.sh --role hot` (dry-run first; docs/07 §5). check.sh = `deploy/bin/rugsnipe-check`
(`cp deploy/bin/rugsnipe-check ~/check.sh`); history from saved files = `deploy/bin/rugsnipe-history`. Python analysis:
`analysis/` (`pyproject.toml`); run scripts with `python3 -I`.

## Datasets

The research scripts (`analysis/research/<date>/<topic>/*.py`) were run in the session scratchpad, and they still
hard-code it: `SP = "/tmp/claude-0/-home-user-rugsnipe/972c43cf-f494-5af4-b87a-fe32117a83be/scratchpad"`. The fetched
data is in `data/datasets/` as `.tar.xz` archives, split into parts under 95 MB. `data/datasets/MANIFEST.md` lists each
archive, what it backs and its checksum.
```
bash data/datasets/unpack.sh            # unpacks every archive into the SP path above, so the scripts run unchanged
bash data/datasets/unpack.sh dec        # one archive
```
- Each archive is a scratchpad folder as it was on Oct 28: the data plus the scripts and helper modules kept beside it
  (several studies import `SP/month/*.py` and `SP/rivalpnl/*.py`, or `chdir` into `SP/dec/copy`). Logs, `*.tok`,
  `*.toml`, `.triton_url` and `live/` are left out. `analysis/research/_helpers/` has the two helper libraries
  (`month/tri.py`, `rivalpnl/*.py`) as plain files for reading.
- Many scripts also put `/home/user/rugsnipe/analysis` on `sys.path` (the upstream checkout). To run them from this repo:
  `[ -e /home/user/rugsnipe ] || ln -s "$PWD" /home/user/rugsnipe`.
- **Keys are not included.** `month/tri.py` reads a Triton URL from `month/.triton_url`, and `rivalpnl/common.py` a
  Helius key from `live/rivals2.py`. To fetch anew, supply your own. Cached responses (`month/tricache/` ...) let many
  scripts rerun offline. The Oct 28 fetchers (copy2 `analysis/research/2026-10-28/fetch/`) use the public RPC.

## Conventions

- Research: one folder per study with a README (run order, results). Pick on one period, score on the next, and report
  without the best 2 trades as well. Count every cost: tips, fees, refused buys' fees, the model's bias against real fills.
- Code: match the surrounding Rust. A behaviour change gets a test (`crates/rugsnipe/tests/`) and a line in the doc that
  owns it (docs/17 for `entry.copy`, docs/19 for `copy_more` ...).
- Docs here: update the curated page (`03-strategies/Sx-*.md`), add sources, keep the README status current.

## Open items (Oct 28)

1. Nothing runs. If the copy of him is ever restarted: deploy the graduation fix `af681ad` first, run him alone (wallets 3
   and 5 lost; the daily stop counts every wallet), and make check.sh count open positions and failed-sell fees.
2. Check the operator-count rule on the box's config ("operator he bought < 0 times" in check.sh suggests
   `copy_signer_min_buys = 0`).
3. The copy's gap: we fill his weaker coins and his better ones get refused (+4.63 of his +8.92). Every refusal fix
   tested negative (docs/19 §9-§10). Landing closer would roughly double the backtest, but a tip doesn't buy it
   (docs/17 §9). A new angle is needed, or let it go.
4. Task #45 and #68 from the original session (his exact selection logic; a new copy-target search) were never finished.
