#!/usr/bin/env python3
"""
A simple threaded HTTP API server to get and set a status value at /api/v1/status.
"""

import argparse
import json
import logging
import signal
import sys
from http.server import BaseHTTPRequestHandler
import socketserver


def parse_args():
    """
    Parse command-line arguments for port and initial status.
    """
    parser = argparse.ArgumentParser(
        description="Run a threaded HTTP server exposing /api/v1/status endpoint."
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=8000,
        help="Port number to listen on (default: 8000)"
    )
    parser.add_argument(
        "-s", "--status",
        default="OK",
        help="Initial status value (default: 'OK')"
    )
    return parser.parse_args()


class StatusAPIHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler that serves and updates a server-side status.
    """
    def _send_json(self, code: int, payload: dict) -> None:
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())

    def do_GET(self):
        if self.path == "/api/v1/status":
            current = getattr(self.server, 'status', 'OK')
            logging.info(f"GET /api/v1/status -> {current}")
            self._send_json(200, {"status": current})
        else:
            logging.warning(f"GET {self.path} -> 404 Not Found")
            self.send_error(404, "Not found")

    def do_POST(self):
        if self.path == "/api/v1/status":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length or 0)
            data = json.loads(raw) if raw else {}
            new_status = data.get("status")
            setattr(self.server, 'status', new_status)
            logging.info(f"POST /api/v1/status <- {new_status}")
            self._send_json(201, {"status": new_status})
        else:
            logging.warning(f"POST {self.path} -> 404 Not Found")
            self.send_error(404, "Not found")


class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    HTTP server with threading mix-in to handle requests concurrently.
    """
    daemon_threads = True
    allow_reuse_address = True


def run_server(port: int, initial_status: str) -> None:
    """
    Configure and start the HTTP server on the given port with the provided status.
    """
    server = ThreadedHTTPServer(("", port), StatusAPIHandler)
    setattr(server, 'status', initial_status)

    def handle_shutdown(signum, frame):
        logging.info("Shutdown signal received, stopping server...")
        server.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    logging.info(f"Serving on port {port} with initial status '{initial_status}'")
    try:
        server.serve_forever()
    except Exception as e:
        logging.error(f"Server error: {e}")
        raise


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    run_server(args.port, args.status)


if __name__ == "__main__":
    main()
