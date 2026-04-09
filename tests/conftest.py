"""
Test configuration and fixtures for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient for the FastAPI application.
    """
    return TestClient(app)


@pytest.fixture
def test_emails():
    """
    Fixture that provides test email addresses.
    """
    return {
        "student1": "student1@mergington.edu",
        "student2": "student2@mergington.edu",
        "student3": "student3@mergington.edu",
    }


@pytest.fixture
def test_activity_name():
    """
    Fixture that provides a test activity name.
    """
    return "Chess Club"


@pytest.fixture
def fresh_client():
    """
    Fixture that provides a TestClient with a fresh activities database.
    This resets the activities state for tests that need isolation.
    """
    # Import here to get a fresh module state
    from importlib import reload
    import src.app as app_module
    
    # Reload the app module to reset activities
    reload(app_module)
    
    return TestClient(app_module.app)
