#!/bin/bash
# run a script with the Triton URL in the environment (never echoed)
set -a; . "${TRITON_ENV:-$HOME/.rugsnipe/triton.env}"; set +a   # one line: TRITON_URL=https://<endpoint>.mainnet.rpcpool.com/<token>; never in the repo
exec python3 -I "$@"
