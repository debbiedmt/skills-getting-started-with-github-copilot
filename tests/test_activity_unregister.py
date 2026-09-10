from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_success_and_participant_is_added():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    client.delete(f"/activities/{activity_name}/unregister?email={email}")

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_rejects_duplicate_registration():
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_existing_participant_removes_email():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    client.post(f"/activities/{activity_name}/signup?email={email}")

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_400():
    activity_name = "Gym Class"
    email = "missingstudent@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"
