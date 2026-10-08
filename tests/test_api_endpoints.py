import pytest

from app import create_app
from database.db import db


@pytest.fixture
def client():
    db.reset()

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

    db.reset()


def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json["status"] == "UP"


def test_list_books(client):
    response = client.get("/api/books")

    assert response.status_code == 200
    assert len(response.json) >= 2


def test_borrow_endpoint(client):
    response = client.post(
        "/api/borrow",
        json={
            "user_id": "U101",
            "book_id": "B001",
        },
    )

    assert response.status_code == 201
    assert response.json["status"] == "ACTIVE"