import pytest


pytestmark = [pytest.mark.integration, pytest.mark.backend]


def test_root_redirects_to_static_index(client):
    # Arrange
    path = "/"

    # Act
    response = client.get(path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_dictionary(client):
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)

    # Assert
    payload = response.json()
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
