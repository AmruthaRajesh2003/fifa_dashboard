import requests
import pandas as pd
from config import API_KEY, BASE_URL

HEADERS = {"X-Auth-Token": API_KEY}

def get_wc_matches():
    try:
        url = f"{BASE_URL}/competitions/WC/matches"
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        
        matches = []
        for m in data.get('matches', []):
            matches.append({
                'Date': m['utcDate'][:10],
                'Status': m['status'],
                'Stage': m['stage'],
                'Group': m.get('group', 'Knockout'),
                'Team1': m['homeTeam']['name'],
                'Team2': m['awayTeam']['name'],
                'Team1_Goals': m['score']['fullTime']['home'],
                'Team2_Goals': m['score']['fullTime']['away'],
                'Venue': m.get('venue', 'TBD')
            })
        return pd.DataFrame(matches)
    except Exception as e:
        return None

def get_wc_standings():
    try:
        url = f"{BASE_URL}/competitions/WC/standings"
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        
        standings = []
        for group in data.get('standings', []):
            group_name = group['group']
            for team in group['table']:
                standings.append({
                    'Group': group_name,
                    'Position': team['position'],
                    'Team': team['team']['name'],
                    'Played': team['playedGames'],
                    'Wins': team['won'],
                    'Draws': team['draw'],
                    'Losses': team['lost'],
                    'GF': team['goalsFor'],
                    'GA': team['goalsAgainst'],
                    'GD': team['goalDifference'],
                    'Points': team['points']
                })
        return pd.DataFrame(standings)
    except Exception as e:
        return None

def get_wc_scorers():
    try:
        url = f"{BASE_URL}/competitions/WC/scorers"
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        
        scorers = []
        for s in data.get('scorers', []):
            scorers.append({
                'Player': s['player']['name'],
                'Country': s['team']['name'],
                'Goals': s['goals'],
                'Assists': s.get('assists', 0)
            })
        return pd.DataFrame(scorers)
    except Exception as e:
        return None
