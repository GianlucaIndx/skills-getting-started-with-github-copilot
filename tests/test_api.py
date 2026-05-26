import pytest

from src.app import activities


pytestmark = pytest.mark.integration


def test_root_redirects_to_static_index(client):
    # Arrange
    path = "/"

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)

    # Assert
    payload = response.json()
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_returns_success_for_new_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_for_existing_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_unregister_returns_success_for_registered_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{activity_name}/unregister"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    path = f"/activities/{activity_name}/unregister"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_returns_400_for_not_registered_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"
    path = f"/activities/{activity_name}/unregister"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is not signed up for this activity"}
