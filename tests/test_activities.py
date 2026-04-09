"""
Tests for the GET /activities endpoint.
Uses the AAA (Arrange-Act-Assert) testing pattern.
"""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""

    def test_get_activities_returns_all_activities(self, client):
        """
        ARRANGE: Client is ready
        ACT: Send GET request to /activities
        ASSERT: Response contains all activities
        """
        # Arrange
        expected_activity_count = 9  # Based on app.py
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == expected_activity_count
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities

    def test_get_activities_returns_correct_structure(self, client):
        """
        ARRANGE: Client is ready
        ACT: Send GET request to /activities
        ASSERT: Each activity has required fields
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert activity_name  # Not empty
            assert required_fields.issubset(activity_data.keys())
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_participants_are_emails(self, client):
        """
        ARRANGE: Client is ready
        ACT: Send GET request to /activities
        ASSERT: Participants are valid email strings
        """
        # Arrange
        # (no setup needed)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_data in activities.values():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant  # Basic email validation
