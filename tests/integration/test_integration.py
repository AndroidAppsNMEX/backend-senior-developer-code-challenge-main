import pytest
import mock
from helpers.helpers import load_mock_data
from app.api_flask import app
from pathlib import Path
from testcontainers.compose import DockerCompose

@pytest.fixture(scope='session')
def mock_service_data():

    with DockerCompose(
        "./",
        compose_file_name="docker-compose.yaml",
        pull=True
    ) as mock_service_data:
        # Wait for the container to be ready (you can add more checks here)
        # mock_service_data.wait_for_container_ready()
        mock_service_data.start()
        yield mock_service_data


@pytest.fixture(scope='session')
def client(mock_service_data):
    with app.test_client() as client:
        yield client


def test_error_400(client):
    response = client.post('/events')
    assert response.status_code == 400



def test_mock_return_correct_values(client):
    mocked_json_data = load_mock_data(Path('data/challenge_mock_data.json'))
    body = {
        "startDate": "2023-01-01",
        "endDate": "2023-02-01",
        "league": "NFL"
    }

    response = client.post('/events', json=body)

    assert response.status_code == 200
    assert response.json == mocked_json_data


def test_mock_return_incorrect_values(client):
    mocked_json_data = load_mock_data(Path('data/challenge_mock_data.json'))
    
    body = {
        "startDate": "2023-01-01",
        "endDate": "2023-01-01",
        "league": "NFL"
    }

    response = client.post('/events', json=body)

    value = response.json != mocked_json_data

    assert response.status_code == 200
    assert value is True