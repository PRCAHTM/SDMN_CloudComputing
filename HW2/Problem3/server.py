#!/usr/bin/env python3
import http.server
import socketserver
import json

PORT = 8000
status = "OK"               # ← initial value must be "OK" (capital O‑K)

class MyHandler(http.server.BaseHTTPRequestHandler):
    def _send_json(self, code, body_dict):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body_dict).encode())

    def do_GET(self):
        if self.path == "/api/v1/status":
            self._send_json(200, {"status": status})
        else:
            self.send_error(404, "Not found")

    def do_POST(self):
        global status
        if self.path == "/api/v1/status":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length or 0))
            status = data.get("status")    # persist for future GETs
            self._send_json(201, {"status": status})
        else:
            self.send_error(404, "Not found")

# Threading mix‑in → concurrent requests (not required, but nicer)
with socketserver.ThreadingTCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
