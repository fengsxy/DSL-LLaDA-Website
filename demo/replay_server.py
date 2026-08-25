"""Serve the DSL-LLaDA paper homepage and frozen replay traces."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


ROOT_DIR = Path(__file__).resolve().parents[1]
ROUTES = {
    "/": (ROOT_DIR / "index.html", "text/html; charset=utf-8"),
    "/index.html": (ROOT_DIR / "index.html", "text/html; charset=utf-8"),
    "/about.html": (ROOT_DIR / "about.html", "text/html; charset=utf-8"),
    "/assets/figure1final.png": (
        ROOT_DIR / "assets" / "figure1final.png",
        "image/png",
    ),
    "/assets/nfe_efficiency_web.png": (
        ROOT_DIR / "assets" / "nfe_efficiency_web.png",
        "image/png",
    ),
    "/assets/nfe_efficiency_web_mobile.png": (
        ROOT_DIR / "assets" / "nfe_efficiency_web_mobile.png",
        "image/png",
    ),
    "/demo/traces/showcase.json": (
        ROOT_DIR / "demo" / "traces" / "showcase.json",
        "application/json; charset=utf-8",
    ),
    "/demo/traces/ocr_impresso_case_39.json": (
        ROOT_DIR / "demo" / "traces" / "ocr_impresso_case_39.json",
        "application/json; charset=utf-8",
    ),
}


class ReplayHandler(BaseHTTPRequestHandler):
    server_version = "DSL-LLaDA-Replay/1.0"

    def do_GET(self) -> None:
        self._serve(include_body=True)

    def do_HEAD(self) -> None:
        self._serve(include_body=False)

    def _serve(self, include_body: bool) -> None:
        path = urlsplit(self.path).path
        if path == "/healthz":
            payload = json.dumps(
                {"status": "ok", "mode": "replay", "gpu_required": False}
            ).encode("utf-8")
            self._write_response(
                payload,
                "application/json; charset=utf-8",
                include_body,
            )
            return

        route = ROUTES.get(path)
        if route is None:
            self.send_error(404, "Not found")
            return

        file_path, content_type = route
        if not file_path.is_file():
            self.send_error(404, "Artifact not found")
            return

        self._write_response(file_path.read_bytes(), content_type, include_body)

    def _write_response(
        self,
        payload: bytes,
        content_type: str,
        include_body: bool,
    ) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        if include_body:
            self.wfile.write(payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=7860)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), ReplayHandler)
    print(
        f"DSL-LLaDA replay site: http://{args.host}:{args.port}",
        flush=True,
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
