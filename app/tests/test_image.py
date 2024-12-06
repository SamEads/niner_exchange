import pytest
from app.routes.user import allowed_file
from unittest.mock import MagicMock
from io import BytesIO

def test_image_type(client):
    file = MagicMock()
    response = client.get('/user/<username>')

    file.filename = "image.jpg"
    file.mimetype = "image/jpeg"
    assert allowed_file(file) == True

    file.filename = "image.exe"
    file.mimetype = "text/html"
    assert allowed_file(file) == False

