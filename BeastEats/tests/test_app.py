import pytest

from app import db
from app.models import Category, Product, User


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.json["application"] == "BeastEats"


def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200


def test_menu_api(client, app):
    with app.app_context():
        category = Category(name="Breakfast", description="Morning meals")
        db.session.add(category)
        db.session.flush()

        product = Product(
            name="Test Breakfast",
            description="CI test product",
            price=100,
            category_id=category.id,
            is_available=True,
        )
        db.session.add(product)
        db.session.commit()

    response = client.get("/api/menu")

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["name"] == "Test Breakfast"


def test_categories_api(client, app):
    with app.app_context():
        db.session.add(Category(name="Breakfast"))
        db.session.commit()

    response = client.get("/api/categories")

    assert response.status_code == 200
    assert response.json[0]["name"] == "Breakfast"


def test_user_registration(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "CI Test User",
            "email": "ci-test@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 201
    assert response.json["message"] == "Registration successful"


def test_duplicate_registration(client):
    payload = {
        "name": "CI Test User",
        "email": "duplicate@example.com",
        "password": "TestPassword123",
    }

    first = client.post("/auth/register", json=payload)
    second = client.post("/auth/register", json=payload)

    assert first.status_code == 201
    assert second.status_code == 409


@pytest.mark.parametrize(
    "payload",
    [
        {
            "name": "CI User",
            "email": "invalid-email",
            "password": "TestPassword123",
        },
        {
            "name": "CI User",
            "email": "valid@example.com",
            "password": "short",
        },
        {
            "name": "",
            "email": "valid@example.com",
            "password": "TestPassword123",
        },
    ],
)
def test_invalid_registration(client, payload):
    response = client.post("/auth/register", json=payload)

    assert response.status_code == 400


def test_invalid_login(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "WrongPassword123",
        },
    )

    assert response.status_code == 401


def test_valid_login(client, app):
    with app.app_context():
        user = User(name="CI Test User", email="login@example.com")
        user.set_password("TestPassword123")
        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200
    assert response.json["message"] == "Login successful"
