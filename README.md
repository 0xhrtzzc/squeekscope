# SqueekScope

A live, read-only dashboard for [Squeekchain](https://squeekchain.com) — the
hamster-powered proof-of-work toychain on Ethereum Sepolia.

Built against the project's public read API
(`https://api.squeekchain.com/v1/...`, no API key required) and documented in
[docs.squeekchain.com/developers/api](https://docs.squeekchain.com/developers/api/).

![SqueekScope dashboard](docs/screenshot.png)

**Live demo:** https://8842-agqx5wjv3jtakqlnabor425bxu.instabox.tech

## What it shows

| Panel | Source | Meaning |
|---|---|---|
| Hamster | `/v1/status` → `measurement` | live/offline, provenance, wheel speed (mm/s), rpm |
| Squeek blocks | `/v1/core` → `core` | block height, progress to next block, cumulative work, difficulty |
| SQK supply | `/v1/economy/state` → `supply` | live supply, total burned |
| Staking | `/v1/economy/state` → `staking` | total staked SQK, total NFT power |
| Settlements | `/v1/settlements` | settlement count, last settle time, next round |
| Recent settlements | `/v1/settlements` → `recentSettlements` | per-round blocks, work added, SQK minted |
| Event feed | `/v1/events` | live chain/nft/staking/system events |

Units follow the API convention: `…BaseUnits` are 18-decimal $SQK, `blockHeight`
and similar are **Squeek blocks** (1,000,000,000 block units each), not Ethereum
blocks. Large integers arrive as decimal strings and are parsed as numbers here
(the values stay far below 2^53).

## Why it proxies instead of calling the API from the page

`api.squeekchain.com` sits behind Cloudflare and does not answer browser
`fetch()` from a third-party origin — the request fails at CORS/preflight even
though the docs advertise `Access-Control-Allow-Origin: *`. `server.py`
(standard library only) does the call server-side with a browser `User-Agent`
and exposes it as `/api/<path>`, memoised for 3s so a 5s-polling page never
hammers upstream.

## Run

```bash
python3 server.py 8842     # http://localhost:8842
```

Endpoints:

- `GET /` — dashboard
- `GET /api/status` · `/api/core` · `/api/economy/state` · `/api/settlements`
  · `/api/events` · `/api/measurement/blocks` · `/api/measurement/runs`
- `GET /healthz` — liveness

## Notes

- Read-only: no wallet, no keys, no transactions. Nothing to sign.
- `"status": "unavailable"` with HTTP 200 means *unknown*, not zero — the
  dashboard shows the last good value rather than inventing one.
- The Sepolia deployment is `core-sepolia-20261103`, revision 7, chain
  `11155111`; contract IDs come from
  [the deployment record](https://docs.squeekchain.com/developers/#deployments),
  never from an API response.
