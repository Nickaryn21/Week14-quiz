# test.py
import pytest
from main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    # Use a separate secret key for tests if you want
    app.config["SECRET_KEY"] = "test-secret"
    with app.test_client() as client:
        yield client


def test_read_main(client):
    """
    Test the root endpoint returns 200 and correct structure.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "version": "1.0.0"}


def test_addition_logic(client):
    """
    Test the math endpoint to ensure logic holds.
    """
    response = client.get("/add/5/10")
    assert response.status_code == 200
    assert response.get_json() == {"result": 15}


def test_invalid_input(client):
    """
    Test that sending text instead of integers results in 404 (Flask behavior).
    """
    response = client.get("/add/five/ten")
    # Flask returns 404 if the route type <int:> doesn't match
    assert response.status_code == 404


# ---------- NEW TESTS FOR LOGIN & SUBTRACT ----------

def test_login_valid_credentials(client):
    """
    Login should succeed with a valid username & password.
    """
    payload = {"username": "alice", "password": "password123"}
    response = client.post("/login", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Login successful"
    assert data["user"] == "alice"


def test_login_invalid_credentials(client):
    """
    Login should fail with wrong password.
    """
    payload = {"username": "alice", "password": "wrongpassword"}
    response = client.post("/login", json=payload)

    assert response.status_code == 401
    assert response.get_json()["detail"] == "Invalid credentials"


def test_subtract_requires_login(client):
    """
    Subtract endpoint should NOT work without login.
    """
    response = client.get("/subtract/10/3")
    assert response.status_code == 401
    assert response.get_json()["detail"] == "Authentication required"


def test_subtract_after_login(client):
    """
    After a successful login, subtract should work.
    """
    # First login
    login_payload = {"username": "alice", "password": "password123"}
    login_response = client.post("/login", json=login_payload)
    assert login_response.status_code == 200

    # Then call subtract in the same client (session keeps cookies)
    response = client.get("/subtract/10/3")
    assert response.status_code == 200
    assert response.get_json() == {"result": 7}
