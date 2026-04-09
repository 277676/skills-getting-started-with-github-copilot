"""
Tests for the POST /activities/{activity_name}/signup endpoint.
Uses the AAA (Arrange-Act-Assert) testing pattern.
"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up students for activities."""

    def test_signup_success(self, client, test_activity_name, test_emails):
        """
        ARRANGE: Prepare test data with a valid activity and new student email
        ACT: Send POST request to signup endpoint
        ASSERT: Student is successfully added to participants
        """
        # Arrange
        activity_name = test_activity_name
        email = test_emails["student1"]
        
        # Get initial participant count
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {email} for {activity_name}"
        
        # Verify participant was added
        verify_response = client.get("/activities")
        updated_count = len(verify_response.json()[activity_name]["participants"])
        assert updated_count == initial_count + 1
        assert email in verify_response.json()[activity_name]["participants"]

    def test_signup_duplicate_student_rejected(self, client, test_activity_name):
        """
        ARRANGE: Prepare a student already registered for an activity
        ACT: Try to signup the same student again
        ASSERT: Request is rejected with 400 status and appropriate error message
        """
        # Arrange
        activity_name = test_activity_name
        # Use an existing participant from the default data
        existing_participants = client.get("/activities").json()[activity_name]["participants"]
        email = existing_participants[0]  # Get first existing participant
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity(self, client, test_emails):
        """
        ARRANGE: Prepare test data with a non-existent activity name
        ACT: Send POST request to signup for non-existent activity
        ASSERT: Request is rejected with 404 status
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = test_emails["student1"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_response_format(self, client, test_activity_name, test_emails):
        """
        ARRANGE: Prepare valid signup request data
        ACT: Send POST request to signup endpoint
        ASSERT: Response has correct format and content
        """
        # Arrange
        activity_name = test_activity_name
        email = test_emails["student2"]
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert isinstance(data["message"], str)
        assert email in data["message"]
        assert activity_name in data["message"]
