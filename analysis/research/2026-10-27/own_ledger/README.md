# Our own wallet, every lamport (Oct 27)

`own_ledger.py WALLET [fetch]`: each transaction of the hot copy bot's wallet since T0 (landed and failed), classified by
what it did, and the sum against the wallet's balance change. Oct 26 13:22 to Oct 27 10:07 UTC, 1,326 transactions:
−1.4115 SOL = closed trades −0.809, 2RR6sfbi held −0.510, 405 failed sells of 2RR6sfbi −0.092, 83 failed buys −0.001.
See `05-live/stuck-coin-2RR6sfbi.md`. A copy of `analysis/research/2026-10-27/h9long/own_ledger.py` in the copy2 repo
(where the rest of `h9long/` lives); it reads its data from the session scratchpad (`SP`), see CLAUDE.md "Datasets".
