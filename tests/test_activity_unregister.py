from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_existing_participant_removes_email():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # ensure the student is not already registered
    client.delete(f"/activities/{activity_name}/unregister?email={email}")

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
