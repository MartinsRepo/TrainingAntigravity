"""Unit tests for mock server endpoints adhering to coding standards."""

import http.client
from pathlib import Path
import sys
import threading
import time
import unittest

# Ensure module directory is in sys.path
LAB_DIR = Path(__file__).resolve().parent
if str(LAB_DIR) not in sys.path:
    sys.path.insert(0, str(LAB_DIR))

from server import HTTPServer, HealthHandler


class TestServerEndpoints(unittest.TestCase):
    """Test suite for HTTP health and metrics endpoints."""

    @classmethod
    def setUpClass(cls) -> None:
        """Start HTTP server on an ephemeral test port in a background thread."""
        cls.port = 8899
        cls.server = HTTPServer(("127.0.0.1", cls.port), HealthHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls) -> None:
        """Shut down HTTP server cleanly."""
        cls.server.shutdown()
        cls.server.server_close()

    def test_health_endpoint(self) -> None:
        """Verify GET /health returns 200 OK and valid JSON status."""
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        conn.request("GET", "/health")
        res = conn.getresponse()
        self.assertEqual(res.status, 200)
        self.assertEqual(res.getheader("Content-Type"), "application/json")
        body = res.read().decode("utf-8")
        self.assertIn('"status": "healthy"', body)
        conn.close()

    def test_metrics_endpoint(self) -> None:
        """Verify GET /metrics returns 200 OK and metrics payload."""
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        conn.request("GET", "/metrics")
        res = conn.getresponse()
        self.assertEqual(res.status, 200)
        body = res.read().decode("utf-8")
        self.assertIn('"events_processed": 128', body)
        conn.close()

    def test_not_found(self) -> None:
        """Verify unknown path returns 404 Not Found."""
        conn = http.client.HTTPConnection("127.0.0.1", self.port)
        conn.request("GET", "/unknown")
        res = conn.getresponse()
        self.assertEqual(res.status, 404)
        conn.close()


if __name__ == "__main__":
    unittest.main()
