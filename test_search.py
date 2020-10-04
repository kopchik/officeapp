import pytest
from fastapi.testclient import TestClient

from search import app

# TODO: mock http requests
# TODO: make negative cases
# TODO: test integrations separately
# TODO: test documentation


def test_search(client):
    result = client.get("/search-repos", params={"q": "test", "engines": "github"})
    assert result.status_code == 200
    json = result.json()
    assert len(json["repos"]) > 0
    assert len(json["errors"]) == 0


def test_search_validation(client):
        result = client.get("/search-repos", params={"q": ""})
        assert_result(result, 422, "value has at least 2 characters")

        result = client.get("/search-repos", params={"engines": "bitbucket"})
        assert_result(result, 400, "unknown engine bitbucket")



def assert_result(result, expected_code, expected_substring):
        assert result.status_code == expected_code
        assert expected_substring in str(result.json())


def test_search(client):
    result = client.get("/available-engines")
    assert result.status_code == 200
    assert result.json() == ['gitea', 'github']


@pytest.fixture(scope='session')
def client():
    return TestClient(app)
