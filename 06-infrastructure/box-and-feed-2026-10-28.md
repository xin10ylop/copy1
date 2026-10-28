# Where to run rugsnipe-hot (the copy of him): box and feed, 2026-10-28

**Labels.** **VERIFIED** = repo data (file named) or measured by me today (TeraSwitch looking glass, Cherry public API,
DNS/ipinfo; raw files under `scratchpad/raw/`). **SOURCED** = a web page (URL, and the date fetched or published).
**UNVERIFIED** = an inference, an estimate or a vendor claim nobody has checked. Times are UTC; Beirut is UTC+2 on these
dates (my measurements ran 15:00-15:20 UTC = 17:00-17:20 Beirut).

---

## 0. The answer

1. **Is there something better than Frankfurt? No.** One box: Frankfurt, bare metal, inside or next to the TeraSwitch
   FRA2 building. Amsterdam (AMS3) ties on reach but has fewer leaders in its building. Nothing else comes close, and
   Ohio is out.
2. **Can Cherry Servers give the same? Almost.** Cherry FRA sits in Equinix FR13, 360 m from TeraSwitch FRA2, on a
   private link. Today it is **0.25-0.33 ms slower per round trip** than inside the TeraSwitch building. On Oct 14 it
   was not slower at all. For this bot that is about **1-2 block positions out of the ~90** it lands behind him.
   In stock right now: **EPYC 9355 at €599/mo (€1.026/h)**. The repo's €989 EPYC 9375F is sold out in Frankfurt.
3. **The box is not what puts us 90 positions behind him. The feed is.** Any box in the Frankfurt metro changes our
   distance by 0-8 positions. The feed choice moves it by about 30-80. Under the Triton plan: point gRPC at
   **Riptide** (free on a shared plan) and keep **Deshred** on. If the copy is ever restarted, test **Triton Preconfs**
   for one day. That is the "new angle" open item 3 asks for.
4. **Ohio never runs the hot path.** It has 0% of leaders in its metro and is 104-108 ms from Frankfurt.
5. **No second site.** Amsterdam or Šiauliai would add at most a few tenths of a SOL a month, and the code to run two
   boxes is not built.

---

## 1. What fra1 actually was

| Fact | Label |
|---|---|
| "Frankfurt bare metal, user `ops`". It ran the hot role: `rugsnipe-hot`, `rugsnipe-guard`, `shredstream-proxy` and the operator, discover and pnl-tg timers. Stopped about 12:45 UTC Oct 27, terminated Oct 28 (`06-infrastructure/README.md`) | VERIFIED |
| **The provider, plan, CPU, IP and datacenter are not recorded anywhere in the repo.** No invoice, no `lscpu`, no `latency-fra-candidate.txt` (the probe output the checklist asks you to keep). The docs/07 diagram says "Frankfurt bare metal (TeraSwitch)", but it was drawn while fra1 was still "to rent". docs/06 §12 says "TeraSwitch FRA bare metal (Latitude/Cherry; AWS eu-central-1 fallback)" | VERIFIED (that it is missing) |
| It was **not the AWS fallback**. `deploy/aws-create-fra1.sh` builds an Ubuntu EC2 box (user `ubuntu`). fra1 used `ops` with `ssh root@FRA1_IP` (docs/08 §1), which is the bare-metal path. The README says bare metal | VERIFIED (docs), inference UNVERIFIED |
| The owner asks whether Cherry "can give the same", which suggests fra1 was not Cherry. So it was most likely **TeraSwitch FRA2**, the plan's first choice | UNVERIFIED |
| Feeds on fra1: Triton Dragon's Mouth gRPC (`*.rpcpool.com`), Triton `SubscribeDeshred` (source label `shreds`) and a shredstream-proxy entry feed. Senders: Helius `fra-sender`, Nozomi `fra2`, Astralane `fr`, BlockRazor Frankfurt, and Jito Frankfurt and Amsterdam through a local TLS relay (`config/probe-a.example.toml`, docs/08 §9 rows `feeds.deshred` and `feeds.entries`, `crates/rugsnipe-feed/src/grpc/mod.rs`) | VERIFIED (config and docs; the box's real `/etc/rugsnipe/rugsnipe.toml` is not in the repo) |

**Ask the owner** for the invoice or provider email to settle it. Then send that box's `lscpu` and a `latency_probe.sh`
output from the backup, if one is there.

---

## 2. What decides this bot's speed

- **Our copy lands a median ~90 block positions after his buy. That gap is the pipeline:** his buy executes, reaches
  our feed, and our buy reaches the leader. Under EU leaders our at-create fires landed a median 90 positions after
  the create (66% in the create slot); his landed a median 103 after it (63%). Under NA leaders it is 28% vs 25% in
  the slot, under Asian leaders 7% vs 10% (docs/17 §10). VERIFIED.
- **Converting positions to time:** about **0.19 ms per position**. The first independent slot-0 winner lands a median
  149 transactions (~28 ms) after the create (gap-2, docs/03 §6). So 90 positions ≈ 17 ms and 45 ≈ 8.5 ms. This is
  an average; the density changes from block to block. UNVERIFIED (derived).
- **What a position is worth:** docs/17 §9 ("A bigger tip", the live copy's rule set) gives +5.64 SOL over 5 days at
  the measured distance and +5.97 at 45 positions. That is about **0.007 SOL per position per 5 days, ~0.044 SOL per
  position per month**. The table for his ≥0.7 SOL buys is far steeper: +2.31 at D = 60 and +0.90 at D = 90, i.e.
  0.047 SOL per position per 5 days. **The two tables disagree by about 6×.** Treat the live-copy table as the main
  figure and the other as an upper bound. VERIFIED (repo figures); the linear slope is UNVERIFIED.
- **Box location enters the pipeline twice, one way each time:** feed node to box, then box to sender. That adds up
  to about one round trip between the box and the TeraSwitch building. The feed's own delay (shred propagation,
  replay, Geyser) is the big part, and it is the same for every box in the metro.
- **Context:** the copy bot lost **−5.13 SOL live** (CLAUDE.md). The box is not the reason. Item 3 of the open items
  (we fill his weaker coins, his better ones get refused) still stands whatever box is chosen.

### Where the leaders are (repo data)

| Cut | Shares | Source |
|---|---|---|
| Leader slots by ingress metro, epoch 1057 | FRA 35.6%, AMS 21.0%, LON 10.3%, NYC 6.3%, TYO 6.1%, **SQQ (Šiauliai) 4.9%**, WAS 4.3%, SIN 4.2%, LAX 2.2%, STO 1.5%, PDX 1.3%, DUB 0.8% | `data/stake_geo_v2.json` VERIFIED |
| By region, slot-weighted | EU 73.9%, APAC 10.9%, US-East 9.8%, US-West 4.1%, US-Central 1.3%, Ohio 0% | speed-geography §1 VERIFIED |
| `data/leader_regions.json` (the bot's leader filter), by validator **count**, not slots | 1,219 identities: eu 649 (53.2%), na 411 (33.7%), asia 131 (10.7%), other or unknown 28 (2.3%) | VERIFIED (counted today) |
| By building | TeraSwitch FRA 10.8%, Latitude FRA 7.8%, TeraSwitch AMS 7.5%, Allnodes FRA 6.7%, **Cherry Šiauliai 4.1%**, TeraSwitch TYO 3.5%, **Cherry FRA (AS213896) 2.9%**, AWS us-east-1 2.8% | speed-geography §1 VERIFIED |
| Leader class | BAM 37.6%, Jito-class 36.9%, Harmonic 25.5% of slots (Oct 14) | `stake_geo_v2.json` VERIFIED; today's mix UNVERIFIED |
| Cherry FRA today | 20 validators, 14.7M SOL, 2.67% of stake | SOURCED [validators.app AS213896 Frankfurt](https://www.validators.app/data-centers/213896-DE-Frankfurt%20am%20Main), fetched Oct 28 |

**Disagreements:** Šiauliai is 4.1% (by building), 4.5% (by metro, v1), 4.94% (by ingress, v2) or 4.4-4.5%
(the BAM `sqq-bam-2` node). Cherry's share of stake is ≈8.8% in speed-geography and 7.2% in speed-data-feed; the
two docs group ASNs differently (critique-speed C13).

**Reach model** (P that a create can be followed in block 0; direct sends, BAM 20 ms rounds, leader-slot weighted,
`stake_geo_v2.json`; VERIFIED as model output):

| Box | P(block 0) | Leader slots within 1 ms one way |
|---|---|---|
| FRA2 (TeraSwitch) | 0.742 | 0.343 |
| AMS3 (TeraSwitch) | 0.745 | 0.187 |
| SQQ (Cherry Šiauliai) | 0.624 | 0.045 |
| CMH (Ohio, AWS) | 0.446 | 0.000 |
| FRA2 + AMS3 | 0.755 | 0.530 |
| FRA2 + SQQ | 0.749 | 0.388 |

---

## 3. Candidate boxes, ranked for this bot

Round trips (RTT) are min/avg in ms from **TeraSwitch's own FRA2 router** (source 64.130.50.5), measured today
15:03-15:19 UTC (`raw/lg2_fra2.json`, `raw/lg2_repeat.json`). Oct 14 figures come from docs/research/speed-gap-6.md §3.
A rented server adds a top-of-rack hop and its own network stack: expect +0.05-0.1 ms (UNVERIFIED). "Extra
positions" = (RTT − 0.09 ms) ÷ 0.19 ms (UNVERIFIED estimate).

| # | Box | Building | Metal or VM | Price | Hourly | RTT to TSW FRA senders, Triton and the FRA ingress | RTT to the AMS leader mass | Extra positions | Label |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **TeraSwitch FRA2**, Ryzen 9 9950X 16C, 128 GB, 2×25G | Probably Equinix FR2, Kruppstraße 121-127. PeeringDB lists TeraSwitch at FR2 and FR5; the DZ link `fra2-tsw ↔ fr2-dzx-001` is 160 µs | metal | **~$425/mo** (catalogue estimate); 150 TB egress pool | yes, no minimum | **0.07-0.12** today and on Oct 14 (Jito 0.069-0.091, Helius fra-sender 0.074, Nozomi 0.075, BlockRazor 0.099, LaserStream 0.068, Harmonic FRA TPU 0.078, BAM fra 0.085, DZ fra2-tsw 0.093, Triton anycast 0.067-0.084) | 5.81-5.88 | 0 | RTT VERIFIED. Price and hourly SOURCED: [whtop listing, added Oct 3 2026](https://www.whtop.com/plans/teraswitch.com/158524). Stock and lead time UNVERIFIED (teraswitch.com, the docs and the portal return a Cloudflare 403 here). A self-serve console exists ("Create Services → Metal", [docs index](https://docs.teraswitch.com/llms.txt), fetched Oct 28) |
| 2 | **ERPC "Metal APP++"**, 9950X, 192 GB, 2×10G | ERPC's Frankfurt gRPC host is TeraSwitch AS20326, 0.110 ms from FRA2. Whether its metal sits there is not stated | metal | €398/mo | ? | ~0.11 if co-located | ~5.9 | ~0 | RTT of the gRPC host VERIFIED. Price SOURCED: [ERPC restock, Mar 25 2026](https://slv.dev/en/news/2026/03/25/erpc-9950x-restock-fra-ams-202603) ("only a handful of units"). Stock today and metal location UNVERIFIED |
| 3 | **Cherry Servers FRA**, in stock: **EPYC 9355** (32C, 3.55 GHz, 192 GB, 3 Gbps), 1 unit; **TR PRO 7965WX** (24C, 4.2 GHz, 512 GB, 3 Gbps), 1 unit | **Equinix FR13, Friesstraße 9**, 360 m from FR2, on Equinix's North-East campus. Private link (PNI) to TeraSwitch. Upstreams RETN, Arelion, NTT; exchange MEGA-IX | metal | **€599/mo** / **€979/mo** (quarterly €1,707 / €2,790) | **€1.026/h** / €1.676/h | **0.32-0.42 today** (Astralane fr 0.356-0.358, Shyft grpc.fra 0.318-0.387, speedtest 0.406-0.415; TTL 56). **0.089 on Oct 14** (TTL 60). Astralane `fr` and Shyft `grpc.fra` are inside Cherry FRA itself | 5.87-5.90 | **~1-2** | Stock and price VERIFIED ([api.cherryservers.com/v1/plans](https://api.cherryservers.com/v1/plans), 15:00 UTC). RTT VERIFIED. FR13 SOURCED ([Cherry Germany page](https://www.cherryservers.com/bare-metal-dedicated-servers/germany), [Cherry locations](https://www.cherryservers.com/network/locations), [Equinix FR13 press release](https://newsroom.equinix.com/2023-11-30-New-Equinix-Frankfurt-data-center-supports-companies-digital-infrastructure-needs-while-advancing-energy-efficiency-goals)). The 360 m is my geocode of both addresses (OSM) |
| 4 | Latitude.sh FRA, f4.metal.small (AMD 4484PX 12C 4.4 GHz, 96 GB, 2×10G) | A different building | metal | $398/mo | $0.55/h | 0.67-0.74 (Latitude TPU 0.715, constant-k prism 0.674); 0.69-0.74 on Oct 14 | 6.07-6.16 (Oct 14) | ~3 | RTT VERIFIED. Price SOURCED: [latitude.sh/pricing](https://www.latitude.sh/pricing), Oct 28 (Frankfurt availability not shown on the page) |
| 5 | Vultr Frankfurt | ? | metal or VM | not checked | yes | 0.656 / 0.698 (`fra-de-ping.vultr.com`) | ? | ~3 | RTT VERIFIED; price UNVERIFIED |
| 6 | **AWS eu-central-1**, c7i.2xlarge (the repo's `aws-create-fra1.sh`) | AWS's own Frankfurt AZ buildings, reached over TeraSwitch's backbone (fra2-bb → fra3-bb → AWS) | VM (Nitro, ENA, 1:1 NAT) | ~$297/mo + EBS, Elastic IP, egress $0.09/GB | $0.4074/h | **0.67-0.90 to AWS service endpoints** (S3 0.671-0.893, DynamoDB 0.823, Lambda 0.866). An EC2 instance itself was not measured: expect ≥ these | 6.03-6.21 | **~4-8** | Endpoint RTT VERIFIED; EC2 RTT UNVERIFIED. Price SOURCED: [DoiT c7i.2xlarge eu-central-1](https://www.doit.com/compute/spot/eu-central-1/c7i.2xlarge), Oct 28. DZ Edge will not run there (1:1 NAT; frankfurt-checklist §2). Not the same building: about 0.6-0.8 ms more per round trip |
| 7 | OVH Frankfurt (0slot `de1`) | OVH | metal | cheap, not checked | | 1.45 | ? | ~7 | RTT VERIFIED |
| 8 | Hetzner | **No Frankfurt site.** NBG1 3.68 ms, FSN1 5.04 ms | | | | 3.7-5.0 | | 19-26 | RTT VERIFIED. **Excluded:** its terms ban crypto nodes (2022-23 press: [Decrypt](https://decrypt.co/108346/ethereum-nodes-cloud-services-host-hetzner-banned), [The Block](https://www.theblock.co/post/165976/host-of-10-of-ethereum-nodes-prohibits-crypto-usage-discussing-consequences)); current terms UNVERIFIED |
| — | Equinix Metal | | | **closed June 30 2026** | | | | | SOURCED: [DCD](https://www.datacenterdynamics.com/en/news/equinix-to-kill-off-metal-by-june-2026/), [Equinix EOS FAQ](https://docs.equinix.com/metal/eos-faq) |
| — | **Ohio**, AWS us-east-2 (exists) | | VM | existing | | **104-108 to FRA**, 97 to AMS | | **≳500 on EU leaders** | VERIFIED (docs/03 §3) |
| — | 2nd site: TeraSwitch **AMS3** (64.130.42.0/24) | Science Park campus | metal | same catalogue (~$425) | yes | 5.8-5.9 from FRA | **0.07-0.09** to Helius ams-sender, Harmonic AMS, BAM ams-bam-2 (10.1% of slots); 0.17 to Jito AMS (Oct 14) | | VERIFIED (Oct 14) |
| — | 2nd site: **Cherry AMS** (Science Park 610) | Equinix AM3 area; PNI to TeraSwitch | metal | 7700X €159 (1 unit), TR 7975WX €1,249 (6), 2× EPYC 7443 €369 (1) | yes | 5.98 | 0.367 from AMS3 (Oct 14) | | VERIFIED |
| — | 2nd site: **Cherry Šiauliai** (Tilžės 74) | hosts BAM `sqq-bam-2` (4.4% of slots) and Astralane `lit` | metal | EPYC 9275F (24C 4.1 GHz, 10 Gbps) €879 (4 units, €1.505/h); EPYC 9355 €599 (2) | yes | **29.5-29.7 from FRA** (30.6 on Oct 14; DZ internet p50 31.5, DZ fiber 27.8) | 34.5 from AMS3 | | VERIFIED |

**Cherry 10 Gbps:** the Germany page says "up to 10 Gbps". Every 10 Gbps plan (9950X, 9900X, EPYC 4564P,
9254P, 9354P, 9554P, 9274F, 9575F) shows **0 in Frankfurt** today. The two FRA plans in stock are 3 Gbps. VERIFIED (API).
3 Gbps is far above what gRPC plus Deshred need: about 16-48 GB/day, i.e. a few Mbit/s on average. UNVERIFIED for a
raw shred feed.

**Is Cherry FRA in the TeraSwitch building? No.** Different building, same campus:
- TeraSwitch FRA2 is very probably Equinix FR2 (Kruppstraße); UNVERIFIED.
- Cherry is in Equinix FR13 (Friesstraße 9); SOURCED.
- 360 m of fibre costs about 0.01 ms, so today's extra 0.25-0.33 ms is the routing path, not distance.
- Today's traceroute from FRA2 goes `_gateway` → 100.117.x → Cherry routers (AS213896), with no exchange or transit
  in between. The Cherry hop answers at about 0.5 ms (`raw/lg2_trace.json`). VERIFIED.
- Cherry's own claim is "under 0.25 ms" to Jito Frankfurt ([Cherry PNI blog, updated Nov 7 2025](https://www.cherryservers.com/blog/pni-with-teraswitch)).
  **The Oct 14 reading (0.089) met that claim; today's (0.32-0.42) does not.** Only a box-side test settles it.

---

## 4. Recommendation

**Single best box: TeraSwitch FRA2 bare metal** (Ryzen 9950X class, ~$425/mo, hourly).
- It shares the building with everything the bot touches: the Triton anycast PoP (0.067-0.084 ms), Jito, Helius
  Sender and LaserStream, Nozomi, BlockRazor, the Harmonic and BAM Frankfurt ingress, and the DZ `fra2-tsw` device.
  VERIFIED.
- The 9950X's clock does not matter. The hot path costs tens of µs of CPU: sign 21.7-32 µs, a PDA 10-20 µs
  (arch-judge-1). VERIFIED.

**If TeraSwitch has no FRA2 stock today:**
- Take **Cherry FRA EPYC 9355, €599/mo or €1.026/h**. Rent it by the hour and run §6 before you commit.
- Against fra1:
  - If fra1 was a TeraSwitch FRA2 box (likely, UNVERIFIED), **Cherry is about 0.25-0.33 ms slower per round trip
    today.** It was not slower on Oct 14.
  - That is ~1-2 of the ~90 positions: about 0.07 SOL/month on the live-copy table, up to ~0.45 on the steep table.
    UNVERIFIED (estimate).
  - It sits 0 hops from Astralane `fr`, one of the five senders.
  - **It fails the checklist's "< 0.2 ms" rule.** Accept it at **< 0.5 ms average** if you agree that ~2 positions
    is worth having a box today. That is your call. Reject it at > 1 ms: the extra path is then something other than
    the PNI.
- Then ERPC FRA (€398, if in stock and in TeraSwitch), then Latitude FRA ($398, +3 positions).
- AWS eu-central-1 only if no bare metal is possible: +4-8 positions and no DZ Edge.

**Ohio: never the hot path.**
- 0% of leaders in its metro, +58 ms mean RTT to the leader and +90-107 ms on the 56% of slots led from FRA or AMS
  (speed-geography §6c). P(block 0) is 0.446 vs 0.742. VERIFIED.
- For the copy, ~100 ms is ≳500 positions on EU leaders. In docs/17 §9's table the ≥0.7 SOL copy is +0.90 SOL at
  D = 90 and +0.10 at D = 150, so Ohio would cost most of the edge. VERIFIED (table); the extrapolation is UNVERIFIED.
- Keep Ohio for analytics, the long copy in paper mode and the fra1 backup.

**A second site is not worth it now:**
- **Amsterdam (AMS3):** saves ~5.9 ms (~31 positions) on the ~21% of copies led from AMS, about 6-7 positions
  averaged over all copies. That is ≈0.3 SOL/month on the live-copy table, up to ~1.8 on the steep one, against
  ~$425/mo plus a second feed. UNVERIFIED (estimate).
- **Šiauliai:** a ~30 ms saving on ~5% of slots. docs/17 §10 measured all far leaders (NA plus Asia) at about 0.1
  SOL over 5 days. Šiauliai alone reaches only 0.624 of slots in block 0. VERIFIED (repo) and UNVERIFIED (Šiauliai gain).
- Two boxes need per-leader-window routing and a shared nonce pool. That is described in docs/06 §11 but **not
  built**. VERIFIED (docs).
- Revisit only after a single Frankfurt box shows the copy is profitable live.

---

## 5. Feeds under the Triton plan

**What the owner's plan includes:**
- **Dragon's Mouth (Yellowstone) gRPC** on the shared endpoint, billed from the prepaid balance at $0.08/GB. The
  pricing page says "Every Triton product is included on every plan, with flexible connection and rate limits and no
  tier gating" (SOURCED: [triton.one/pricing](https://triton.one/pricing), fetched Oct 28).
- **Riptide** (`https://riptide.rpcpool.com:443`), the lower-latency path to the same gRPC service, "available on
  shared Dragon's Mouth subscriptions, and usage is billed as part of the shared service". Same token, same filters
  (SOURCED: [docs.triton.one Riptide](https://docs.triton.one/project-yellowstone/riptide), fetched Oct 28).
- **SubscribeDeshred** (pre-execution transactions with lookup tables resolved): "paid beta", "now available on all
  plans" (SOURCED: [Triton Deshred blog, updated Oct 5 2026](https://blog.triton.one/deshred-transactions-the-fastest-path-to-solana-data/)).
  fra1 ran it, so it is very probably on the account already; UNVERIFIED, check the portal.
- **Shred Streaming** (raw UDP; FRA/AMS $1,500/mo or $0.59 per 15 min) and **Preconfs** (Harmonic and BAM): **on
  request**, through the portal or support (SOURCED: pricing page; [Triton Preconfs](https://triton.one/products/triton-preconfs)).
  **Shred prices changed:** the repo has "$0.18 per 15 min, or from $900/mo" (infra-shopping §0, Oct 15). Today's page
  says $1,500/mo or $0.59 per 15 min in FRA/AMS.

**Unconfirmed details:**
- The plan name "mainnet-shared" does not appear on Triton's public pages. The endpoint's form,
  `<name>.mainnet.rpcpool.com`, is the shared-plan form (Triton docs). UNVERIFIED that the two are the same thing.
- Pay-as-you-go needs a $125 minimum deposit (prepaid, non-refundable, 12 months). The $75 is presumably what is left
  of it; UNVERIFIED.
- The repo's volume estimates: about 16 GB/day for the whole pump program, 8 GB/day for successful transactions only
  (infra-shopping §0), and ~2 GB/hour with `bundle_run` (docs/08 §9). With gRPC plus Deshred both carrying every pump
  transaction, **$75 lasts roughly 10-30 days**. Watch the daily usage in the portal. UNVERIFIED (estimate).

**Where the endpoints land (VERIFIED today):**
- `tiny-breeze-ba60.mainnet.rpcpool.com` → 208.91.108.10, `riptide.rpcpool.com` → 208.91.108.100,
  `preconfs.rpcpool.com` → 208.91.108.24.
- All three are **anycast** (TeraSwitch AS20326; the DNS answers ignore the client subnet).
- From the FRA2 router they answer in 0.067-0.096 ms, and from AMS3 in 0.071-0.106 ms. **A Frankfurt box reaches
  Triton's Frankfurt PoP.**

**Who shows a transaction first:**

| Feed | What you get | Lead | Label |
|---|---|---|---|
| **Harmonic preconf** (Triton) | Executed by the builder before the leader runs it, **with the result** (success, fail, fees only). Only on slots led by Harmonic validators (~25%) | ~99% before Geyser; **~15 ms p50**, ~75 ms p95 | SOURCED (vendor) |
| **BAM preconf** (Triton; Helius has it too) | Committed by the leader, result when the node reports it. Only on BAM slots (~38%) | ~91% before Geyser; ~8 ms p50, ~34 ms p95 | SOURCED (vendor) |
| Raw leader shreds (DZ Edge FRA $1,500/mo; Triton Shred Streaming FRA $1,500/mo; Helius $800-1,000/IP) | Every shred, no result; needs our own decoder, which the hot binary **does not have** (docs/08 §0: "DoubleZero Edge or Helius shreds: not in the hot binary") | DZ: "~6 ms faster than other shred services" | SOURCED ([doublezero.xyz/edge](https://doublezero.xyz/edge), Oct 28) |
| **Deshred** (Triton, already in the code as `feeds.deshred`) | The transaction before replay, **no result**. "Uses the same shred sources as our raw shred streams", which include DZ Edge | **fra1 measured his tx a median 6 ms before the gRPC stream** (docs/17 §10). Vendor figure: p50 ~6.3 ms, p90 ~20 ms after shreds arrive | VERIFIED (repo) and SOURCED |
| Dragon's Mouth via **Riptide** | Post-execution, with the result | "delivers first 81.8% of the time" against the standard path | SOURCED ([Triton blog, updated Aug 4 2026](https://blog.triton.one/before-the-block-get-the-fastest-streams-on-solana/)) |
| Dragon's Mouth, standard endpoint, or Helius LaserStream FRA ($499 Business since Apr 7 2026, 10 connections) | Post-execution | baseline | SOURCED ([Helius, Apr 7 2026](https://www.helius.dev/blog/laserstream-websockets)) |

**The landed transaction earliest, with its result:** a Harmonic preconf on Harmonic slots, a BAM preconf on BAM
slots, otherwise Riptide gRPC. **Earliest without a result:** shreds, then Deshred.

**Recommendation:**
1. **Day one, free:** keep Dragon's Mouth. Fills, exits and the kill's health check depend on the post-execution
   stream. A/B it against Riptide for 2 hours (`grpc` = your endpoint, `grpc_b` = Riptide; §6 step B), then keep the
   one that is first on most creates. The repo's rule: a feed ≥10 ms ahead at p50 is worth paying for, one within
   2 ms is not; here both cost the same.
   - Riptide warns that failovers arrive as TCP resets. The bot reconnects, but a gap over `stale_ms = 4,000` latches
     the kill, so watch for that.
2. **Keep Deshred on:** 6 ms ≈ 30 positions.
   - Today a copy reacts to his *landed* buy from the post-execution stream (docs/17 §9). Firing on the Deshred copy
     would also copy the buys that fail his guard: −0.30 SOL over 5 days for his failed key attempts (docs/17 §10).
   - That is roughly a wash against the ~0.2 SOL the 30 positions are worth. **It pays only if the bot predicts his
     guard from the pre-execution curve**, which the Deshred adapter already quotes. That is code plus a backtest.
     UNVERIFIED.
3. **Do not buy** raw shreds, DZ Edge or LaserStream for this bot. The binary cannot read raw shreds, and Deshred
   gives the same sources decoded.
4. **The one feed that could move the result: Triton Preconfs**, if the copy is ever restarted.
   - Ask by ticket for `harmonic:fra`, `bam:fra` (and maybe the `ams` regions), with `signer_include` = his wallet.
     Harmonic preconfs carry the execution result, so no failed copies on those slots.
   - **Price:** "greater of $0.0015 / slot or $50 / million messages", and a stream pays for every slot its region
     produces (SOURCED: pricing page and [Triton preconfs docs](https://docs.triton.one/llms-full.txt)).
   - Using Oct 14 ingress shares (Harmonic FRA 10.4%, BAM FRA 5.3% of ~398,700 slots/day), `harmonic:fra` is about
     **$62/day** and `bam:fra` about **$32/day**, ≈ $2,800/month for both. UNVERIFIED (my arithmetic; check the
     per-slot price in the panel).
   - **Test 1 day (~$95)**: log his tx's lead over Deshred and gRPC.
   - Prerequisites: the repo has **no preconf adapter** (no `preconf` anywhere in `crates/`). VERIFIED. Access is not
     self-serve.
   - It would make sense only if the lead is ≳10 ms on his coins. From 90 to 10 positions is worth +1.53 SOL per 5
     days on the live-copy table (+5.64 → +7.17). UNVERIFIED as to whether preconfs deliver that.

---

## 6. Day-one checklist: verify the box before trading (run on the NEW Frankfurt box)

Prerequisite: the repo is cloned to `~/rugsnipe` on the box (frankfurt-checklist §3). Rent by the hour (Cherry
€1.026/h, TeraSwitch hourly), run this, and cancel if it fails.

**Step A: network and placement.** One copy-paste block, as user `ops`, on the new box:

```bash
cd ~/rugsnipe
sudo apt-get install -y mtr-tiny bc curl >/dev/null
lscpu | grep -E '^Model name|^CPU\(s\)|^Thread'
ip -4 -br addr show scope global | awk '{print $1, $3}'; curl -s https://checkip.amazonaws.com
bash deploy/latency_probe.sh 30 | tee ~/latency-day1.txt
for t in jito-fra:64.130.50.88 helius-fra:64.130.50.91 harmonic-fra:198.13.140.105 bam-fra:198.13.140.227 dz-fra2:198.13.140.16 nozomi-fra2:64.130.47.135 blockrazor:64.130.47.70 laserstream:64.130.32.214 triton-own:208.91.108.10 riptide:208.91.108.100 preconfs:208.91.108.24 astralane-fr:185.191.117.97 bam-ams:63.254.167.197 jito-ams:64.130.52.119; do printf "%-14s %-16s " "${t%%:*}" "${t#*:}"; ping -c 100 -i 0.2 -q -W 1 "${t#*:}" | tail -1; done | tee -a ~/latency-day1.txt
for h in tiny-breeze-ba60.mainnet.rpcpool.com riptide.rpcpool.com preconfs.rpcpool.com; do printf "%-40s %-16s " "$h" "$(getent hosts $h | awk '{print $1}')"; curl -s -o /dev/null -w "tcp %{time_connect}s\n" "https://$h/"; done | tee -a ~/latency-day1.txt
mtr -rwc 50 64.130.50.88 | tee -a ~/latency-day1.txt
```

What each line should print:

| Line | Expect | Fail if |
|---|---|---|
| `lscpu` | your CPU (9950X or EPYC 9355) and its core count | not the plan you paid for |
| `ip … ; checkip` | **the same public address on both lines**, ignoring the `/prefix` (a public IP on the NIC, no NAT; DZ Edge needs this). You do not need to paste the address | they differ (NAT: the AWS-style 172.31.x on the NIC) |
| `latency_probe.sh` (TCP connect, ms) | `jito-frankfurt`, `helius-fra`, `nozomi-fra2`, `astralane-fr`, `blockrazor-fra` median **< 1 ms**; `jito-amsterdam` / `helius-ams` ~6; `jito-ny` ~75-90; `jito-tokyo` ~210-235 | any Frankfurt sender above ~2 ms, or `0/30` |
| ICMP, the 5 core targets + nozomi, blockrazor, laserstream (`rtt min/avg/max/mdev`) | **TeraSwitch box: avg < 0.2 ms**, max < 2, 0% loss (frankfurt-checklist §2). **Cherry box: ~0.35-0.5 avg** (today's router reading was 0.32-0.42, plus the host) | Cherry > 0.5 avg: ask Cherry why the TeraSwitch PNI path is slow (it was 0.09 on Oct 14). > 1 ms: reject. AWS: accept < ~2.5 (checklist) |
| `triton-own`, `riptide`, `preconfs` | same class as Jito (< 0.2 on TeraSwitch, < 0.5 on Cherry): proves the anycast lands on Triton's Frankfurt PoP | > 3 ms: the anycast took you to another city (open a Triton ticket) |
| `astralane-fr` | **Cherry box: < 0.2** (it is in Cherry FRA). TeraSwitch box: ~0.35-0.45 | |
| `bam-ams`, `jito-ams` | 5.8-6.2 (sanity: Amsterdam is one metro away) | > 8 |
| `getent` / `tcp` | 208.91.108.10 / .100 / .24; `tcp` ≈ the ICMP RTT (0.000x s) | another address, or tcp > 0.005 s |
| `mtr` to Jito | TeraSwitch box: every hop inside the building, last hop 0% loss. Cherry box: Cherry hops (`*.cherryservers.net`), then TeraSwitch, **no exchange or transit hop** | a hop through an IX or a transit carrier |

Keep `~/latency-day1.txt` (the checklist asks for it, and fra1's copy was never saved).

**Step B: the feed race, in paper mode with no wallet.** Do this once Step A passes and `install.sh --role hot` is done.
- In `/etc/rugsnipe/rugsnipe.toml` `[feeds]` (edit with `sudoedit`):
  ```toml
  grpc    = { enabled = true, url = "https://tiny-breeze-ba60.mainnet.rpcpool.com", x_token = "GRPC_TOKEN", stale_ms = 4_000, bundle_run = true }
  grpc_b  = { enabled = true, url = "https://riptide.rpcpool.com", x_token = "GRPC_B_TOKEN", stale_ms = 4_000 }
  deshred = { enabled = true, url = "https://riptide.rpcpool.com", x_token = "DESHRED_TOKEN", stale_ms = 4_000, bundle_run = true }
  ```
- In `/etc/rugsnipe/keys/api-keys.toml`, add the lines `GRPC_B_TOKEN = "..."` and `DESHRED_TOKEN = "..."` holding the
  **same token** as `GRPC_TOKEN`. Never paste or print it.
- Run 2 hours, then (on the box):
  `sudo journalctl -u rugsnipe-hot --since -2h --no-pager | grep -A 12 '"first_seen"' | tail -14`
- **Expect:** `first_by` shows which of `grpc` / `grpc_b` wins most creates, and `lag."grpc_behind_shreds"` p50 near
  **6 ms**, as fra1 measured.
- **Keep Riptide** as `grpc` if it wins the majority. If `shreds` is not ahead, Deshred is not enabled on the account:
  open a ticket.

**Before any real money (CLAUDE.md, open item 1):**
- Deploy the graduation fix `af681ad` upstream first.
- Run him alone (wallets 3 and 5 out).
- Make check.sh count open positions and failed-sell fees.
- Then `chronyc tracking` < 1 ms against `ntp.frankfurt.jito.wtf` and `tune-hot.sh --check` with no DIFF
  (frankfurt-checklist §7).

---

## 7. Disagreements and open items

| Item | Values | Status |
|---|---|---|
| Cherry FRA ↔ TeraSwitch FRA2 | 0.089 ms (Oct 14, TTL 60) / **0.32-0.42 ms (Oct 28, TTL 56)** / "< 0.25 ms" (Cherry blog) | Only a box-side ping settles it (§6 A) |
| Position value | 0.007 SOL per position per 5 days (live-copy table) vs 0.047 (his ≥0.7 SOL buys table), docs/17 §9 | Two different copy sets; both are backtests; the copy lost live |
| Triton shred price | $0.18 per 15 min / from $900/mo (repo, Oct 15) vs FRA $1,500/mo / $0.59 per 15 min (pricing page, Oct 28) | Use today's page |
| DZ Edge FRA | $1,500/mo per seat ([doublezero.xyz/edge](https://doublezero.xyz/edge), Oct 28); a search snippet quotes the subscribe page at $100 USDC per epoch; the data API lists `dz100a-fra2-tsw` at $100 with 39 seats free | Not needed for this bot |
| Cherry has DZ devices | `cherlita` (sqq), `cherydam` (ams), and `frankry` (fra) looks like Cherry FRA by its name (`raw/dz_edge_devices.json`) | `frankry` = Cherry FRA is UNVERIFIED |
| fra1's provider | not recorded | ask the owner |
| Leader class mix after Alpenglow | Oct 14 figures used throughout | re-run `getClusterNodes` before relying on the preconf cost |

**What I did not change:** no code, no config, nothing pushed upstream.

**Raw files** (kept in the session scratchpad, not in the repo):
- `cherry_plans.json`: the Cherry API at 15:00 UTC.
- `lg2_fra2.json`, `lg2_repeat.json`, `lg2_triton.json`, `lg2_trace.json`: TeraSwitch looking-glass pings and
  traceroutes.
- `dz_edge_devices.json`, `dz_metro_lat.json`: DoubleZero.
- `triton_llms_full.txt`: the Triton docs.
- The pinger script is `scratchpad/scripts/lg2.py`. It uses the same method as `deploy/speed_gap6/lg.py`.
