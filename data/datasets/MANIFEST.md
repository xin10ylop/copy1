# Datasets

The scratchpad folders behind `analysis/research/`, as they were on Oct 28, compressed: the fetched data (raw RPC
transactions, signature lists, account reads, tapes, caches) and the scripts and helper modules kept beside it, which
several studies import or `chdir` into. Logs, `*.tok`, `*.toml`, `*.sh`, `.triton_url` and `live/` are left out. Every
file was scanned for API keys, tokens and keypairs before packing; none are included. Each archive unpacks to
`<SP>/<name>/`, where `SP` is the scratchpad path the scripts hard-code (see CLAUDE.md "Datasets").

```
bash data/datasets/unpack.sh                 # check SHA256SUMS, unpack everything into SP
bash data/datasets/unpack.sh dec ext         # some
SP=/elsewhere bash data/datasets/unpack.sh   # another place (then change SP in the scripts you run)
```
Archives over 95 MB are split into `.part-NN` files (GitHub's 100 MB limit); `unpack.sh` joins them. Study folders are
under `analysis/research/`.

| archive | parts | compressed | unpacked | files | what uses it |
|---|---|---|---|---|---|
| `dec` | 1 | 65.4M | 465.2M | 30,303 | used by 2026-10-25/five (copy, exact), follow; 2026-10-26/fails, flush, h9, holders, oprule, speed, wallets; 2026-10-27/refused |
| `ext` | 2 | 97.6M | 3.3G | 22,821 | used by 2026-10-25/five; 2026-10-26/speed, wallets |
| `fails` | 1 | 106.7K | 430.6K | 7 | used by 2026-10-26/fails |
| `flush` | 1 | 985.4K | 3.8M | 1,436 | used by 2026-10-26/flush |
| `fp` | 1 | 3.9M | 21.0M | 4,190 | used by 2026-10-25/five, follow |
| `full` | 1 | 1.2M | 8.8M | 2,260 | used by 2026-10-24/corrected, rugs; 2026-10-25/five, follow |
| `full30` | 1 | 502.7K | 3.2M | 377 | used by 2026-10-24/corrected |
| `helpers` | 1 | 12.9K | 39.6K | 15 | the helper libraries `month/tri.py` (Triton client: its URL file `month/.triton_url` is not included) and `rivalpnl/*.py` (pump parsers, Helius client: its key file `live/rivals2.py` is not included); also plain in `analysis/research/_helpers/` |
| `hold` | 1 | 10.2M | 59.4M | 105 | used by 2026-10-26/holders, w3 |
| `month` | 1 | 15.5M | 86.5M | 1,779 | used by 2026-10-24 (+corrected, tweets); 2026-10-25/five, follow; 2026-10-26/fails, flush, h9, holders, oprule, six, w3, wallets; 2026-10-27/h9long, own_ledger, refused. His and 6anjqMe's month of transactions, `pull_month.py`, the Triton cache |
| `oos` | 1 | 9.4M | 49.2M | 5,608 | used by 2026-10-26/flush, holders, wallets, wallets2; 2026-10-27/refused |
| `pm` | 1 | 6.1M | 60.2M | 47 | used by 2026-10-24/corrected, rugs; 2026-10-25/follow |
| `refused` | 1 | 4.6M | 24.4M | 2,049 | used by 2026-10-27/refused |
| `rivalpnl` | 1 | 7.2M | 77.2M | 43 | most studies from 2026-10-24 to 2026-10-26 (the pump parsers and their data) |
| `six` | 1 | 1.3M | 5.8M | 10 | used by 2026-10-26/six |
| `today` | 1 | 26.5M | 129.5M | 20 | used by 2026-10-24 (+corrected, tweets) |
| `univ` | 1 | 24.6M | 136.6M | 21,823 | used by 2026-10-24 (+corrected, rugs, tweets); 2026-10-25/five, follow; 2026-10-26/holders, speed |
| `wide` | 1 | 7.4M | 36.8M | 9,143 | used by 2026-10-26/flush, holders, wallets |
