import pytest

from src.app import activities, signup_for_activity, unregister_from_activity


pytestmark = pytest.mark.backend


def test_signup_for_activity_adds_email_to_participants():
    # Arrange
    activity_name = "Gym Class"
    email = "unit.test.student@mergington.edu"

    # Act
    result = signup_for_activity(activity_name=activity_name, email=email)

    # Assert
    assert result == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_unregister_from_activity_removes_email_from_participants():
    # Arrange
    activity_name = "Programming Class"
    email = "unit.remove@mergington.edu"
    activities[activity_name]["participants"].append(email)

    # Act
    result = unregister_from_activity(activity_name=activity_name, email=email)

    # Assert
    assert result == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]
