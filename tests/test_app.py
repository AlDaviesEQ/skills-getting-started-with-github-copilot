import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_and_unregister():
    # Sign up a new participant
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]

    # Unregister the participant
    unregister_resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    assert f"Removed {email}" in unregister_resp.json()["message"]

    # Unregister again should 404
    unregister_resp2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp2.status_code == 404

    # Sign up again, then try duplicate signup
    signup_resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp2.status_code == 200
    signup_resp3 = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp3.status_code == 400
    assert "already signed up" in signup_resp3.json()["detail"]
