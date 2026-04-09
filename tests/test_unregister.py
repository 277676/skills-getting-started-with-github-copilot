"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.
Uses the AAA (Arrange-Act-Assert) testing pattern.
"""

import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering students from activities."""

    def test_unregister_success(self, client, test_activity_name, test_emails):
        """
        ARRANGE: Sign up a student first, then prepare unregister request
        ACT: Send DELETE request to unregister endpoint
        ASSERT: Student is successfully removed from participants
        """
        # Arrange
        activity_name = test_activity_name
        email = "new_student_unregister@mergington.edu"  # Use unique email to avoid conflicts
        
        # First, sign up the student
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Get participant count after signup
        verify_response = client.get("/activities")
        count_after_signup = len(verify_response.json()[activity_name]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        
        # Verify participant was removed
        verify_response = client.get("/activities")
        count_after_unregister = len(verify_response.json()[activity_name]["participants"])
        assert count_after_unregister == count_after_signup - 1
        assert email not in verify_response.json()[activity_name]["participants"]

    def test_unregister_nonexistent_participant(self, client, test_activity_name, test_emails):
        """
        ARRANGE: Prepare unregister request for a student not registered
        ACT: Send DELETE request to unregister endpoint
        ASSERT: Request is rejected with 400 status
        """
        # Arrange
        activity_name = test_activity_name
        email = "never_registered@mergington.edu"  # Use unique email guaranteed to not be registered
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]

    def test_unregister_from_nonexistent_activity(self, client, test_emails):
        """
        ARRANGE: Prepare unregister request for non-existent activity
        ACT: Send DELETE request to unregister from non-existent activity
        ASSERT: Request is rejected with 404 status
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = test_emails["student1"]
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_response_format(self, client, test_activity_name, test_emails):
        """
        ARRANGE: Sign up a student, then prepare unregister request
        ACT: Send DELETE request to unregister endpoint
        ASSERT: Response has correct format and content
        """
        # Arrange
        activity_name = test_activity_name
        email = test_emails["student2"]
        
        # Sign up first
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert isinstance(data["message"], str)
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_existing_participant(self, client, test_activity_name):
        """
        ARRANGE: Select an existing participant from the default data
        ACT: Send DELETE request to unregister the participant
        ASSERT: Existing participant is successfully removed
        """
        # Arrange
        activity_name = test_activity_name
        participants = client.get("/activities").json()[activity_name]["participants"]
        email = participants[0]  # Get first existing participant
        initial_count = len(participants)
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        
        # Verify participant was removed
        verify_response = client.get("/activities")
        updated_participants = verify_response.json()[activity_name]["participants"]
        assert len(updated_participants) == initial_count - 1
        assert email not in updated_participants
