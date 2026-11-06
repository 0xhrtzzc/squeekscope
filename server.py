#!/usr/bin/env python3
"""
SqueekScope — a live dashboard for Squeekchain (Sepolia toychain).
Built on the public read API: https://api.squeekchain.com/v1/...

The API sits behind Cloudflare for browser clients (no CORS from a page),
so this tiny server proxies the reads server-side and serves the dashboard.
Stdlib only. No dependencies.

Run:  python3 server.py [port]
"""
import json
import os
import sys
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

API = "https://api.squeekchain.com/v1"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")
ALLOWED = {"status", "core", "economy/state", "settlements", "events",
           "measurement/blocks", "measurement/runs", "measurement/stats"}
CACHE_TTL = 3.0            # seconds — the upstream counter ticks continuously
_cache: dict[str, tuple[float, bytes]] = {}
HERE = os.path.dirname(os.path.abspath(__file__))


def upstream(path: str) -> tuple[int, bytes]:
    """Fetch one API path, memoised for CACHE_TTL seconds."""
    now = time.time()
    hit = _cache.get(path)
    if hit and now - hit[0] < CACHE_TTL:
        return 200, hit[1]
    req = urllib.request.Request(
        f"{API}/{path}",
        headers={"User-Agent": UA, "Accept": "application/json",
                 "Origin": "https://squeekchain.com",
                 "Referer": "https://squeekchain.com/"},
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            body = r.read()
            code = r.status
    except urllib.error.HTTPError as e:
        body, code = e.read()[:500], e.code
    except Exception as e:                      # network hiccup or CF challenge
        return 502, json.dumps({"error": "upstream_unreachable",
                                "detail": str(e)[:120]}).encode()
    if code == 200:
        _cache[path] = (now, body)
    return code, body


class Handler(BaseHTTPRequestHandler):
    server_version = "SqueekScope/1.0"

    def _send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?", 1)[0].strip("/")

        if path in ("", "index.html"):
            with open(os.path.join(HERE, "index.html"), "rb") as f:
                return self._send(200, f.read(), "text/html; charset=utf-8")

        if path == "healthz":
            return self._send(200, b'{"ok":true}', "application/json")

        if path.startswith("api/"):
            target = path[4:]
            if target not in ALLOWED:
                return self._send(404, b'{"error":"unknown_endpoint"}',
                                  "application/json")
            code, body = upstream(target)
            return self._send(code, body, "application/json")

        return self._send(404, b'{"error":"not_found"}', "application/json")

    def log_message(self, fmt, *args):          # keep stdout readable
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8842
    srv = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"SqueekScope on http://0.0.0.0:{port}", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
