def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data

    chess = data["Chess Club"]
    assert chess["description"].startswith("Learn strategies")
    assert "max_participants" in chess
    assert isinstance(chess["participants"], list)


def test_signup_for_activity(client):
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

    response = client.get("/activities")
    assert email in response.json()[activity]["participants"]


def test_duplicate_signup_returns_400(client):
    activity = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant(client):
    activity = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity}/participants?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"

    response = client.get("/activities")
    assert email not in response.json()[activity]["participants"]


def test_unregister_missing_participant_returns_404(client):
    activity = "Chess Club"
    email = "missing@mergington.edu"

    response = client.delete(f"/activities/{activity}/participants?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_signup_nonexistent_activity_returns_404(client):
    response = client.post("/activities/Unknown/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_nonexistent_activity_returns_404(client):
    response = client.delete("/activities/Unknown/participants?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
