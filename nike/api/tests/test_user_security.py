"""
Regression tests for the public-registration privilege-escalation fix and the
missing authorization on /user/all and /user/{user_id}/{status}.

Each test fails against the pre-fix code and passes against the fix:
- UserService.create() used to trust a client-supplied "role" field verbatim.
- GET /user/all and POST /user/{user_id}/{status} had no auth dependency at all.
"""

from fastapi.testclient import TestClient

from user import UserService
from utils.kbn import ROLE
from helpers.const import CODE


class FakeUserRepository:
    """Stub for the external boundary (persistence) — not the unit under test."""

    def __init__(self):
        self.received = None

    def create(self, data):
        self.received = data
        return {**data, "token": "fake-token"}


def test_create_forces_user_role_even_when_client_requests_admin():
    repo = FakeUserRepository()
    service = UserService(user_repository=repo)

    service.create({
        "username": "attacker",
        "email": "attacker@example.com",
        "fullname": "Attacker",
        "password": "Test123@",
        "role": ROLE.ADMIN.value,
    })

    assert repo.received["role"] == ROLE.USER.value


def test_user_all_rejects_anonymous_requests():
    from main import app

    client = TestClient(app)
    response = client.get("/user/all")

    body = response.json()
    assert body["code"] == CODE.API.INVALID_REQUEST
    assert body["payload"] is None


def test_user_status_change_rejects_anonymous_requests():
    from main import app

    client = TestClient(app)
    response = client.post("/user/some-id/1")

    body = response.json()
    assert body["code"] == CODE.API.INVALID_REQUEST
    assert body["payload"] is None
