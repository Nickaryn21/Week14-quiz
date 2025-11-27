**Week 14 – CI/CD Pipeline, Flask API, Authentication, and Unit Testing**

This project implements a simple Flask-based API with mathematical operations, a login system using a temporary in-memory database, and protected endpoints that require authentication. The repository also includes a complete CI/CD pipeline using GitHub Actions to perform linting, automated testing, and a simulated deployment using Docker.
This assignment demonstrates the ability to build backend API functions, secure endpoints, write automated tests, and integrate continuous integration and delivery in a modern development workflow.

**Project Structure**
main.py
test.py
requirements.txt
Dockerfile
.github/workflows/main.yml

**API Endpoints**
1. Root Endpoint
Route: /
Method: GET
Description: Health check endpoint to verify the API is functioning correctly.

Response:

{
  "status": "ok",
  "version": "1.0.0"
}

2. Addition Endpoint
Route: /add/<int:a>/<int:b>
Method: GET
Description: Performs an addition operation using two integer path parameters.

Example Request:
/add/5/10

Response:

{
  "result": 15
}


If non-integer parameters are provided, Flask automatically returns status code 404 because of the <int:> type converter.

3. Login Endpoint

Route: /login
Method: POST
Description: Authenticates a user using a temporary in-memory dictionary that simulates a database.
If the credentials are valid, the logged-in username is stored in the Flask session.

Temporary User Database:

USERS = {
    "alice": "password123",
    "admin": "admin456"
}


Valid Request Body:

{
  "username": "alice",
  "password": "password123"
}


Successful Response:

{
  "message": "Login successful",
  "user": "alice"
}


Invalid Credentials Response:

{
  "detail": "Invalid credentials"
}

4. Protected Subtraction Endpoint

Route: /subtract/<int:a>/<int:b>
Method: GET
Description: Performs subtraction, but only if the user is authenticated.
The endpoint checks for an active session created by the login endpoint.

Unauthenticated Response:

{
  "detail": "Authentication required"
}


Authenticated Response Example:

{
  "result": 7
}

Unit Testing (test.py)

The test.py file contains a complete set of tests written using pytest.
All tests are automatically executed during the CI pipeline.

The tests cover:

Root endpoint validation

Addition endpoint (valid and invalid input)

Login endpoint

Valid login

Invalid login

Subtract endpoint

Fails without login

Succeeds after login

Example: Valid Login Test
def test_login_valid_credentials(client):
    payload = {"username": "alice", "password": "password123"}
    response = client.post("/login", json=payload)
    assert response.status_code == 200
    assert response.get_json()["user"] == "alice"

Example: Subtraction After Login Test
def test_subtract_after_login(client):
    login_payload = {"username": "alice", "password": "password123"}
    client.post("/login", json=login_payload)

    response = client.get("/subtract/10/3")
    assert response.status_code == 200
    assert response.get_json() == {"result": 7}


All tests must pass before deployment simulation proceeds.

CI/CD Pipeline Overview

The CI/CD pipeline is implemented in .github/workflows/main.yml.
The pipeline includes two stages: Integration (CI) and Delivery (CD).

Integration Stage (CI)

Triggered on every push or pull request to the main branch.

The CI stage performs:

Code checkout

Python setup

Dependency installation

Linting using Flake8

Automated testing using PyTest

The workflow stops immediately if any step fails.

Delivery Stage (CD)

This stage only runs when:

The CI stage succeeds

The event is a push to the main branch

The CD stage performs:

Docker setup and build

Simulated deployment steps (container build confirmation, registry push simulation, and orchestration update message)

This stage does not deploy to a real environment; it demonstrates understanding of the deployment workflow.

**Dockerfile**
The Dockerfile uses the python:3.9-slim base image and performs the following steps:

1. Sets the working directory
2. Installs dependencies from requirements.txt
3. Copies the application code
4. Exposes port 8000
5. Starts the Flask application

Build Command
  docker build -t week14-app .

Run Command
  docker run -p 8000:8080 week14-app

**How to Run Locally**

Install dependencies:
  pip install -r requirements.txt

Run the Flask application:
  python main.py

Execute unit tests:
  pytest test.py

**Summary**
- This project demonstrates:
- Creation of a multi-endpoint Flask API
- Implementation of a login system
- Protection of certain endpoints using session authentication
- Writing comprehensive unit tests with pytest
- Building a complete CI/CD pipeline using GitHub Actions
- Using Docker to simulate deployment
This fulfills all requirements for the Week 14 assignment.
