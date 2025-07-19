"""Test configuration and fixtures for calculator tests."""

import pytest
import sys
import os

# Add the parent directory to the path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def app_context():
    """Create an application context for testing."""
    with app.app_context():
        yield app
