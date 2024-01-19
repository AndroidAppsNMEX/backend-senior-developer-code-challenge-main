from flask import Flask, request, jsonify
from pandasql import sqldf
import os
import logging
import traceback
import requests
import pandas as pd

app = Flask(__name__)

# Configure the logging
app.logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
app.logger.addHandler(stream_handler)

URL_HOST = os.environ.get('URL_HOST', 'http://localhost:9000')


# Auxiliary function to return the data and be used as helper for unittesting
def return_data(df_scoreboard, df_team_rankings):
    return sqldf("""
            SELECT 
                sb.id as eventId,
                date(sb.timestamp) as eventDate,
                time(sb.timestamp) as eventTime,
                sb.home_id as homeTeamId,
                sb.home_nickName as homeTeamNickName,
                sb.home_city as homeTeamCity,
                tr_home.rank as homeTeamRank,
                tr_home.rankPoints as homeTeamRankPoints,
                sb.away_id as awayTeamId,
                sb.away_nickName as awayTeamNickName,
                sb.away_city as awayTeamCity,
                tr_away.rank as awayTeamRank,
                tr_away.rankPoints as awayTeamRankPoints
            FROM df_scoreboard as sb
            JOIN df_team_rankings as tr_home
                ON sb.home_id = tr_home.teamId
            JOIN df_team_rankings as tr_away
                ON sb.away_id = tr_away.teamId        

            """).to_dict('records')


def call_remote_url(url, params):
    response = requests.request("GET", url=url, params=params)
    return pd.json_normalize(response.json())


def get_scoreboard_data(startDate, endDate, league):
    params_scoreboard = {
            "since": startDate,
            "until": endDate
        }

    url_scoreboard = f"{URL_HOST}/{league}/scoreboard"
    df_scoreboard = call_remote_url(url_scoreboard, params_scoreboard).query(f'"{startDate}" <= timestamp <= "{endDate}"')
    df_scoreboard.columns = df_scoreboard.columns.str.replace("[\s\-\[\]()?/;&'\.]+", '_', regex=True)
    print(df_scoreboard.to_dict('records'))
    return df_scoreboard


def get_team_rankings_data(league):
    url_team_rankings = f"{URL_HOST}/{league}/team-rankings"
    df_team_rankings = call_remote_url(url_team_rankings, {})

    return df_team_rankings


# Endpoint to retrieve events for ACME
@app.route('/events', methods=['POST'])
def get_events():
    api_key = request.headers.get('API-Key')
    # Check if API key is valid
    query_params = request.args.to_dict()

    try:

        league = request.json.get('league', 'NFL')
        startDate = request.json.get('startDate')
        endDate = request.json.get('endDate')

        df_scoreboard = get_scoreboard_data(startDate, endDate, league)
        df_team_rankings = get_team_rankings_data(league)

        return jsonify(return_data(df_scoreboard, df_team_rankings))

    except ValueError as e:
        return jsonify({'error': str(e)}), 401


if __name__ == '__main__':
    app.run()