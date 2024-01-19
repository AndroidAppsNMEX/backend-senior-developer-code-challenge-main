import mock
import pandas as pd
from helpers.helpers import load_mock_data
from app import api_flask
from pathlib import Path


@mock.patch('app.api_flask.call_remote_url')
def test_get_scoreboard_data(mocked_call_remote_url):
    mocked_call_remote_url.return_value = pd.json_normalize(load_mock_data(Path('data/scoreboard_mock_data.json')))
    df_scoreboard = api_flask.get_scoreboard_data('2023-01-01', '2023-02-01', 'NFL')
    assert df_scoreboard.to_dict('records') == pd.json_normalize(load_mock_data(Path('data/processed_scoreboard_mock_data.json'))).to_dict('records')


@mock.patch('app.api_flask.call_remote_url')
def test_get_team_rankings_data(mocked_call_remote_url):
    mocked_call_remote_url.return_value = pd.json_normalize(load_mock_data(Path('data/team_rankings_mock_data.json')))
    df_team_rankings = api_flask.get_team_rankings_data('NFL')
    assert df_team_rankings.to_dict('records') == pd.json_normalize(load_mock_data(Path('data/team_rankings_mock_data.json'))).to_dict('records')


def test_return_data():
    df_scoreboard = pd.json_normalize(load_mock_data(Path('data/processed_scoreboard_mock_data.json')))
    df_team_rankings = pd.json_normalize(load_mock_data(Path('data/team_rankings_mock_data.json')))
    response = api_flask.return_data(df_scoreboard, df_team_rankings)
    assert response == pd.json_normalize(load_mock_data(Path('data/challenge_mock_data.json'))).to_dict('records')



