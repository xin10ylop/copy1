#!/bin/bash
# run_all.sh REPO OUT: Part A (the published scripts), then Part B and C in order. Logs and the small JSON hand-offs go
# in OUT. Run setup.sh first.
set -euo pipefail
REPO=${1:-/home/user/copy1}; OUT=${2:-$(pwd)/out}; H=$(cd "$(dirname "$0")" && pwd)
SP=/tmp/claude-0/-home-user-rugsnipe/972c43cf-f494-5af4-b87a-fe32117a83be/scratchpad
R=$REPO/analysis/research; mkdir -p "$OUT/logs"; cd "$OUT"
py() { python3 -I "$@"; }
# Part A: reproduce (ablate.py rewrites SP/dec/copy/live_copies.json with the same content)
py "$R/2026-10-25/five/copy/ablate.py"     > logs/A_ablate.txt
py "$R/2026-10-25/five/copy/ablate2.py"    > logs/A_ablate2.txt
py "$R/2026-10-25/five/copy/scratch.py"    > logs/A_scratch.txt
py "$R/2026-10-25/five/copy/react_pos.py"  > logs/A_react_pos.txt
py "$R/2026-10-25/five/copy/tipworth.py"   > logs/A_tipworth.txt
(cd "$SP/dec/copy" && py "$SP/dec/copy/prem5.py") > logs/A_prem5.txt      # opens scratch.py beside itself (fails/README)
(cd "$SP/dec/copy" && py "$R/2026-10-26/fails/prem5b.py") > logs/A_prem5b.txt   # opens ./scratch.py
py "$R/2026-10-26/oprule/options.py"       > logs/A_options.txt
py "$R/2026-10-26/oprule/arrival.py"       > logs/A_arrival.txt
# Part B and C
(cd "$REPO" && py "$H/live_parse.py" 05-live/check-sh-2026-10-27.txt "$OUT/live_rows.json") > logs/B_live_parse.txt
py "$H/check_base.py"                      > logs/B_check_base.txt
py "$H/recon.py" "$OUT"                    > logs/B_recon.txt
py "$H/calib_live.py" "$OUT/live_rows.json" > logs/B_calib_live.txt
py "$H/c1_stake_ladder.py"                 > logs/C1_stake_ladder.txt
py "$H/c2_exit_bucket.py"                  > logs/C2_exit_bucket.txt
py "$H/c3_sell_late.py" "$OUT/calib_live.json" > logs/C3_sell_late.txt
py "$H/c4_breakers.py" "$OUT/live_rows.json" > logs/C4_breakers.txt
py "$H/c5_refused_lowtip.py" "$OUT/live_landing.json" > logs/C5_refused_lowtip.txt
py "$H/c6_oprule.py"                       > logs/C6_oprule.txt
py "$H/c7_buckets.py" "$OUT/live_rows.json" > logs/C7_buckets.txt
py "$H/c8_bid.py" "$OUT/live_rows.json" "$OUT/live_landing.json" > logs/C8_bid.txt
py "$H/c9_bidkey.py" /tmp/claude-0/-home-user-copy1/289c45cb-b6c5-5bb3-9b48-165765ddce53/scratchpad/agents/onchain/data/rows.jsonl > logs/C9_bidkey.txt   # the rows.jsonl check is optional
echo "done: $OUT/logs"
