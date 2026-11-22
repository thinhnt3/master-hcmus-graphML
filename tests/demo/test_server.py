import json
import threading
from http.client import HTTPConnection

import pytest

from src.demo.server import make_server


@pytest.fixture
def server(demo):
    server = make_server(demo, port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield server
    server.shutdown()
    server.server_close()
    thread.join(timeout=2)


def request(server, method, path, body=None, headers=None):
    client = HTTPConnection("127.0.0.1", server.server_port, timeout=10)
    payload = json.dumps(body) if body is not None else None
    client.request(method, path, body=payload, headers=headers or {})
    response = client.getresponse()
    data = response.read()
    status, kind = response.status, response.getheader("Content-Type")
    client.close()
    return status, kind, data


def test_serves_offline_ui_status_image_and_actual_search(server):
    assert request(server, "GET", "/")[0] == 200
    assert request(server, "GET", "/app.js")[0] == 200
    status, _, data = request(server, "GET", "/api/status")
    assert status == 200 and json.loads(data)["protocol"]["gallery_images"] == 3
    status, kind, data = request(server, "GET", "/api/image/101")
    assert status == 200 and kind == "image/jpeg" and data.startswith(b"\xff\xd8")
    status, _, data = request(server, "POST", "/api/search", {"query": "A new sentence", "results": 2, "alpha": 0})
    result = json.loads(data)
    assert status == 200 and len(result["results"]) == 2
    assert result["protocol"]["alpha"] == 0.7  # Request parameters never retune the model.


def test_bad_request_and_image_path_do_not_expose_files(server):
    assert request(server, "POST", "/api/search", {"query": ""})[0] == 400
    assert request(server, "GET", "/api/image/../../README.md")[0] == 404
    assert request(server, "GET", "/api/image/999")[0] == 404
    assert request(server, "GET", "/../../README.md")[0] == 404


def test_rejects_another_web_origin_or_host(server):
    assert request(server, "POST", "/api/search", {"query": "x"}, {"Origin": "https://example.com"})[0] == 403
    assert request(server, "GET", "/api/status", headers={"Host": "example.com"})[0] == 403
