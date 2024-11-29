import pytest

def test_home_route():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert response.data ==
    print(response)

test_home_route()