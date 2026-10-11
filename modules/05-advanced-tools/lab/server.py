"""Lightweight background HTTP service for testing process management."""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import time
from typing import Tuple


START_TIME = time.time()


class HealthHandler(BaseHTTPRequestHandler):
    """HTTP Request handler for mock health and metrics endpoints."""

    def do_GET(self) -> None:
        """Handles incoming GET requests."""
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            payload = {
                "status": "healthy",
                "service": "event-pipeline-mock",
                "uptime_seconds": round(time.time() - START_TIME, 2),
            }
            self.wfile.write(json.dumps(payload).encode("utf-8"))
        elif self.path == "/metrics":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            payload = {
                "events_processed": 128,
                "active_workers": 4,
                "error_rate": 0.0,
            }
            self.wfile.write(json.dumps(payload).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def log_message(self, format: str, *args: Tuple[object, ...]) -> None:
        """Suppress default HTTP request logging to stderr."""
        return


def run_server(port: int = 8888) -> None:
    """Starts the HTTP server on the specified port.

    Args:
        port: The TCP port to listen on. Defaults to 8888.
    """
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, HealthHandler)
    print(f"Mock server listening on http://127.0.0.1:{port}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully.", flush=True)
    finally:
        httpd.server_close()


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else 8888
    run_server(port_arg)
