from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_prevent_duplicate():
    activity = "Chess Club"
    email = "testuser@example.com"

    # ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert email in activities[activity]["participants"]

    # duplicate signup should fail
    r2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert r2.status_code == 400


def test_unregister_flow():
    activity = "Chess Club"
    email = "testuser@example.com"

    # ensure registered
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    r = client.post(f"/activities/{activity}/unregister?email={email}")
    assert r.status_code == 200
    assert email not in activities[activity]["participants"]

    # unregistering again should error
    r2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert r2.status_code == 400
