# Pasang frostvo1d.my.id ke SqueekScope — 4 langkah

Hasil akhir: **https://frostvo1d.my.id** nampilin dashboard SqueekScope ✓,
dan itu **domain sendiri** ✓ → lolos syarat form IMD ✓.

---

## Langkah 1 — Cari tahu di mana DNS-nya diatur

Domain `.my.id` biasanya dikelola di registrar tempat lu beli. Buka panel
DNS-nya (biasanya menu **DNS Management** / **Kelola DNS** / **Nameserver**).

Cek cepat dari terminal:

```bash
dig +short NS frostvo1d.my.id
```

- Kalau keluar `ns1.rumahweb.com` / `dns1.registrar...` → pakai panel **registrar** itu
- Kalau keluar `*.ns.cloudflare.com` → domain udah dipindah ke Cloudflare, edit di sana
- Kalau **kosong** → domain belum punya NS aktif, harus diset dulu di registrar

---

## Langkah 2 — Tambah 5 record DNS ini

| Type | Name / Host | Value / Target | TTL |
|---|---|---|---|
| A | `@` | `185.199.108.153` | 3600 |
| A | `@` | `185.199.109.153` | 3600 |
| A | `@` | `185.199.110.153` | 3600 |
| A | `@` | `185.199.111.153` | 3600 |
| CNAME | `www` | `0xhrtzzc.github.io` | 3600 |

Catatan:
- Kalau panelnya nolak `@`, isi nama domain lengkap: `frostvo1d.my.id`
- Kalau CNAME nolak tanpa titik di akhir, coba `0xhrtzzc.github.io.`
- **Jangan** pakai `A` ke IP lain — 4 IP di atas punya GitHub Pages

---

## Langkah 3 — Kasih tau gue

Bilang **"udah"** → gue cek propagasi DNS (biasanya 5–30 menit, kadang 1–2 jam),
lalu gue nyalain **HTTPS enforced** di GitHub Pages begitu sertifikatnya terbit.

---

## Langkah 4 — Submit

Setelah `https://frostvo1d.my.id` kebuka ✓, balik ke form IMD:

| Field | Isi |
|---|---|
| Project name | `SqueekScope` |
| Site address | `https://frostvo1d.my.id` |
| What does it do | teks di bawah |
| Source repo | `https://github.com/0xhrtzzc/squeekscope` |
| Headline image | `squeekscope-banner.png` (udah gue bikinin) |

### Teks buat field "What does it do"

```
SqueekScope is a live, read-only dashboard for Squeekchain built entirely on the public read API at api.squeekchain.com/v1. It surfaces the wheel's live measurement (freshness, provenance, rpm), Squeek Core block height with progress toward the next block, cumulative work and difficulty, the SQK supply schedule including burned totals, staking totals and NFT power, the settlement history table with per-round SQK minted, the next round state, and a live feed of settlement, NFT deposit and merge events.

It reads six documented endpoints (status, core, economy/state, settlements, events, measurement) straight from the browser, uses the API's own units and field names, and is one static HTML file with zero dependencies. Read-only: no wallet, no keys, no transactions. Source and endpoint-to-panel mapping are in the repository.
```
