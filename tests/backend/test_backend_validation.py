import pytest


pytestmark = [pytest.mark.integration, pytest.mark.backend]


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


def test_signup_returns_400_for_empty_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "   "
    path = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Email is required"}


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


def test_signup_returns_404_for_activity_name_with_special_characters(client):
    # Arrange
    activity_name = "Chess+Club@2026"
    email = "student@mergington.edu"
    path = f"/activities/{activity_name}/signup"

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


def test_unregister_returns_400_on_second_attempt_for_same_email(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{activity_name}/unregister"

    # Act
    first_response = client.post(path, params={"email": email})
    second_response = client.post(path, params={"email": email})

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json() == {"detail": "Student is not signed up for this activity"}
