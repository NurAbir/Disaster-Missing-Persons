"""Basic smoke tests to verify the app boots and public endpoints respond.

These tests require a reachable MongoDB instance (see MONGODB_URL env var).
They intentionally avoid touching auth-protected endpoints or mutating data,
so they're safe to run against a fresh/local database.
"""

import pytest
from httpx import AsyncClient, ASGITransport

from disaster_missing_persons.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def test_homepage_loads(client: AsyncClient) -> None:
    """The homepage should render without requiring authentication."""
    response = await client.get("/")
    assert response.status_code == 200


async def test_public_stats_endpoint(client: AsyncClient) -> None:
    """The public stats endpoint should be reachable without a token."""
    response = await client.get("/api/reports/stats")
    assert response.status_code == 200
    body = response.json()
    for key in ("active_reports", "found_persons", "total_tips", "urgent_reports"):
        assert key in body


async def test_list_reports_endpoint(client: AsyncClient) -> None:
    """Listing reports should not require authentication."""
    response = await client.get("/api/reports/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_register_requires_valid_payload(client: AsyncClient) -> None:
    """Registering with an incomplete payload should return a validation error."""
    response = await client.post("/api/auth/register", json={})
    assert response.status_code == 422


async def test_create_report_requires_auth(client: AsyncClient) -> None:
    """Creating a report without a token should be rejected."""
    response = await client.post("/api/reports/", json={})
    assert response.status_code in (401, 403)
