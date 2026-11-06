# Submission — Squeekchain builder badge ("Buildooooor")

## Satu kalimat

**SqueekScope** — dashboard live buat Squeekchain yang baca API publik (`api.squeekchain.com/v1`) dan nampilin state hamster, Squeek blocks, supply $SQK, staking, settlement, plus feed event — real-time, read-only, nol dependency.

## Yang dibutuhin buat submit

| Field | Isi |
|---|---|
| **Judul** | SqueekScope |
| **Repo** | https://github.com/0xhrtzzc/squeekscope |
| **Live URL** | https://0xhrtzzc.github.io/squeekscope/ |
| **Kategori** | Tool / Dashboard / Explorer |
| **Attribution** | wallet Genesis yang mau dikasih badge |

## Deskripsi (buat form, ~90 kata)

SqueekScope is a live dashboard for Squeekchain built entirely on the public read API documented at docs.squeekchain.com/developers/api. It surfaces the hamster's live measurement (freshness, provenance, wheel speed, rpm), Squeek block height with progress toward the next block, cumulative work and difficulty, the $SQK supply schedule with burned totals, staking totals, the settlement history table with per-round SQK minted, the next round state, and a live event feed of settlements, NFT deposits and merges.

The whole thing is two files and zero dependencies: a stdlib Python proxy and one HTML page. The proxy exists because the API does not answer third-party browser fetches, so it re-serves the allow-listed paths under `/api/` with a 3-second memo. Read-only — no wallet, no keys, nothing to sign.

## Attribution (kalau ditanya "kenapa ini buat Squeekchain")

- 100% datanya dari API resmi mereka ✓ — nggak ada scraping, nggak ada endpoint gelap
- Pakai vocabulary asli API (`settledThroughRound`, work units, Squeek block) biar nggak salah skala
- Nutupin celah yang mereka belum punya: satu halaman yang nampilin hamster + ekonomi + settlement sekaligus

## Catatan buat gue (bukan buat dikirim)

- Kalau badge-nya ditolak karena "live URL cuma sandbox", opsi berikutnya: GitHub Pages (static) —
  tapi `index.html` butuh proxy buat API, jadi harus pakai Cloudflare Worker kecil
  (`/api/*` → `api.squeekchain.com/v1/*` + header browser). Atau Vercel/Netlify function.
- Screenshot ada di `docs/screenshot.png` (59 KB, dashboard penuh angka).
