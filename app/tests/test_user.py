import pytest

def test_valid_user(client):
    username = "User123"

    response = client.get(f'/user/{username}')
    assert response.status_code == 302  # Route is Get/Post

def test_invalid_user(client):
    username = ""   # Invalid username

    response = client.get(f'/user/{username}')
    assert response.status_code == 404
