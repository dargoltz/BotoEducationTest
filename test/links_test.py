import uuid
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_create_link_ok(client):
    fake_id = uuid.uuid4()

    with patch("main.add_link_to_db", return_value=fake_id):
        response = client.post("/shorten", params={"link": "https://google.com"})

    assert response.status_code == 200
    assert response.json() == str(fake_id)


def test_create_link_invalid_url(client):
    response = client.post("/shorten", params={"link": "hello"})
    assert response.status_code == 422


def test_create_link_empty(client):
    response = client.post("/shorten", params={"link": ""})
    assert response.status_code == 422


def test_create_link_missing_param(client):
    response = client.post("/shorten")
    assert response.status_code == 422


def test_get_link_ok(client):
    link_id = uuid.uuid4()
    link = "https://google.com"

    with patch("main.get_link_by_id", return_value=link):
        response = client.get(f"/{link_id}", follow_redirects=False)

    assert response.status_code == 301
    assert response.headers["location"] == link


def test_get_link_not_found(client):
    link_id = uuid.uuid4()

    with patch("main.get_link_by_id", return_value=None):
        response = client.get(f"/{link_id}")

    assert response.status_code == 404
