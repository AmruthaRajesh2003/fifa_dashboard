import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_match_data():
    matches = pd.DataFrame({
        'Match_ID': range(1, 49),
        'Group': ['A','A','A','A','A','A',
                  'B','B','B','B','B','B',
                  'C','C','C','C','C','C',
                  'D','D','D','D','D','D',
                  'E','E','E','E','E','E',
                  'F','F','F','F','F','F',
                  'G','G','G','G','G','G',
                  'H','H','H','H','H','H'],
        'Team1': ['Brazil','France','Germany','Argentina','Spain','Portugal',
                  'England','Netherlands','Belgium','Croatia','Denmark','Serbia',
                  'USA','Mexico','Canada','Ecuador','Uruguay','Colombia',
                  'Japan','South Korea','Australia','Morocco','Senegal','Ghana',
                  'Brazil','France','Germany','Argentina','Spain','Portugal',
                  'England','Netherlands','Belgium','Croatia','Denmark','Serbia',
                  'USA','Mexico','Canada','Ecuador','Uruguay','Colombia',
                  'Japan','South Korea','Australia','Morocco','Senegal','Ghana'],
        'Team2': ['Germany','Argentina','Spain','Portugal','Brazil','France',
                  'Belgium','Denmark','England','Serbia','Netherlands','Croatia',
                  'Ecuador','Canada','USA','Colombia','Mexico','Uruguay',
                  'Morocco','Ghana','Senegal','South Korea','Japan','Australia',
                  'Germany','Argentina','Spain','Portugal','Brazil','France',
                  'Belgium','Denmark','England','Serbia','Netherlands','Croatia',
                  'Ecuador','Canada','USA','Colombia','Mexico','Uruguay',
                  'Morocco','Ghana','Senegal','South Korea','Japan','Australia'],
        'Team1_Goals': np.random.randint(0, 5, 48),
        'Team2_Goals': np.random.randint(0, 5, 48),
        'Stage': ['Group']*48,
        'Venue': ['New York','Los Angeles','Dallas','Houston','Miami','Seattle',
                  'New York','Los Angeles','Dallas','Houston','Miami','Seattle',
                  'New York','Los Angeles','Dallas','Houston','Miami','Seattle',
                  'New York','Los Angeles','Dallas','Houston','Miami','Seattle',
                  'New York','Los Angeles','Dallas','Houston','Miami','Seattle',
                  'New York','Los Angeles','Dallas','Houston','Miami','Seattle',
                  'New York','Los Angeles','Dallas','Houston','Miami','Seattle',
                  'New York','Los Angeles','Dallas','Houston','Miami','Seattle'],
        'Date': pd.date_range(start='2026-06-11', periods=48, freq='D')
    })

    matches['Result'] = matches.apply(
        lambda x: x['Team1'] if x['Team1_Goals'] > x['Team2_Goals']
        else (x['Team2'] if x['Team2_Goals'] > x['Team1_Goals'] else 'Draw'), axis=1)
    matches['Total_Goals'] = matches['Team1_Goals'] + matches['Team2_Goals']
    return matches

def get_upcoming_matches():
    upcoming = pd.DataFrame({
        'Date': [
            '2026-06-19', '2026-06-19', '2026-06-20',
            '2026-06-20', '2026-06-21', '2026-06-21',
            '2026-06-22', '2026-06-22', '2026-06-23',
            '2026-06-23'
        ],
        'Time': [
            '15:00', '18:00', '15:00',
            '18:00', '15:00', '18:00',
            '15:00', '18:00', '15:00',
            '18:00'
        ],
        'Team1': [
            'Brazil', 'France', 'Germany',
            'Argentina', 'Spain', 'England',
            'Portugal', 'Netherlands', 'Japan',
            'Morocco'
        ],
        'Team2': [
            'Colombia', 'Denmark', 'USA',
            'Croatia', 'Serbia', 'Belgium',
            'Uruguay', 'Mexico', 'South Korea',
            'Senegal'
        ],
        'Group': ['E','B','C','D','F','B','E','C','G','H'],
        'Venue': [
            'Miami', 'New York', 'Dallas',
            'Houston', 'Seattle', 'Los Angeles',
            'New York', 'Dallas', 'Miami',
            'Houston'
        ],
        'Status': ['Upcoming']*10
    })
    return upcoming

def get_team_history():
    history = {
        'Brazil': {'WC_Titles': 5, 'Finals': 7, 'Best': 'Champions', 'Last_WC': '2022 QF'},
        'France': {'WC_Titles': 2, 'Finals': 3, 'Best': 'Champions', 'Last_WC': '2022 Final'},
        'Germany': {'WC_Titles': 4, 'Finals': 8, 'Best': 'Champions', 'Last_WC': '2022 Groups'},
        'Argentina': {'WC_Titles': 3, 'Finals': 6, 'Best': 'Champions', 'Last_WC': '2022 Champions'},
        'Spain': {'WC_Titles': 1, 'Finals': 1, 'Best': 'Champions', 'Last_WC': '2022 R16'},
        'Portugal': {'WC_Titles': 0, 'Finals': 0, 'Best': '3rd Place', 'Last_WC': '2022 QF'},
        'England': {'WC_Titles': 1, 'Finals': 1, 'Best': 'Champions', 'Last_WC': '2022 QF'},
        'Netherlands': {'WC_Titles': 0, 'Finals': 3, 'Best': 'Runners-up', 'Last_WC': '2022 QF'},
        'Belgium': {'WC_Titles': 0, 'Finals': 0, 'Best': '3rd Place', 'Last_WC': '2022 Groups'},
        'Croatia': {'WC_Titles': 0, 'Finals': 1, 'Best': 'Runners-up', 'Last_WC': '2022 3rd Place'},
        'Japan': {'WC_Titles': 0, 'Finals': 0, 'Best': 'Round of 16', 'Last_WC': '2022 R16'},
        'Morocco': {'WC_Titles': 0, 'Finals': 0, 'Best': '4th Place', 'Last_WC': '2022 SF'},
        'USA': {'WC_Titles': 0, 'Finals': 0, 'Best': '3rd Place', 'Last_WC': '2022 R16'},
        'Mexico': {'WC_Titles': 0, 'Finals': 0, 'Best': 'Quarter Final','Last_WC': '2022 Groups'},
        'South Korea': {'WC_Titles': 0, 'Finals': 0, 'Best': '4th Place', 'Last_WC': '2022 R16'},
        'Senegal': {'WC_Titles': 0, 'Finals': 0, 'Best': 'Quarter Final','Last_WC': '2022 R16'},
    }
    return history

def get_venue_map_data():
    venues = pd.DataFrame({
        'City': ['New York', 'Los Angeles', 'Dallas', 'Houston',
                 'Miami', 'Seattle', 'San Francisco', 'Boston'],
        'Stadium': [
            'MetLife Stadium', 'SoFi Stadium', 'AT&T Stadium',
            'NRG Stadium', 'Hard Rock Stadium', 'Lumen Field',
            'Levi\'s Stadium', 'Gillette Stadium'
        ],
        'Lat': [40.8135, 33.9534, 32.7473, 29.6847,
                25.9580, 47.5952, 37.4032, 42.0909],
        'Lon': [-74.0745, -118.3392, -97.0945, -95.4107,
                -80.2389, -122.3316, -121.9698, -71.2643],
        'Capacity': [82500, 70240, 80000, 72220,
                     65326, 69000, 68500, 65878],
        'Matches': [8, 7, 6, 6, 7, 5, 5, 4]
    })
    return venues

def get_top_scorers():
    scorers = pd.DataFrame({
        'Player': ['Kylian Mbappé','Erling Haaland','Vinicius Jr',
                   'Harry Kane','Pedri','Lautaro Martinez',
                   'Bukayo Saka','Gavi','Rodri','Leroy Sane'],
        'Country': ['France','Norway','Brazil',
                    'England','Spain','Argentina',
                    'England','Spain','Spain','Germany'],
        'Goals': [8, 7, 6, 6, 5, 5, 4, 4, 3, 3],
        'Assists': [3, 2, 4, 1, 3, 2, 5, 2, 4, 1]
    })
    return scorers

def get_team_stats():
    teams = pd.DataFrame({
        'Team': ['Brazil','France','Germany','Argentina','Spain',
                 'England','Portugal','Netherlands','Belgium','Croatia'],
        'Wins': [4,4,3,3,4,3,3,2,2,2],
        'Draws': [1,1,2,1,0,1,1,2,1,2],
        'Losses': [1,1,1,2,2,2,2,2,3,2],
        'Goals_For': [12,11,9,8,10,8,7,6,7,5],
        'Goals_Against': [4,5,6,7,5,7,6,7,8,6],
        'Points': [13,13,11,10,12,10,10,8,7,8]
    })
    return teams

def get_player_history():
    players = {
        'Kylian Mbappé': {
            'Country': 'France',
            'Age': 27,
            'Club': 'Real Madrid',
            'Position': 'Forward',
            'WC_2018': 'Winner 🏆',
            'WC_2022': 'Runner-up (Final)',
            'Career_Goals': 320,
            'Career_Assists': 180,
            'Fun_Fact': 'Second teenager to score in WC Final after Pelé!'
        },
        'Erling Haaland': {
            'Country': 'Norway',
            'Age': 25,
            'Club': 'Manchester City',
            'Position': 'Striker',
            'WC_2018': 'Did not qualify',
            'WC_2022': 'Did not qualify',
            'Career_Goals': 280,
            'Career_Assists': 90,
            'Fun_Fact': 'First ever WC for Norway — qualified 2026!'
        },
        'Vinicius Jr': {
            'Country': 'Brazil',
            'Age': 24,
            'Club': 'Real Madrid',
            'Position': 'Forward',
            'WC_2018': 'Squad member',
            'WC_2022': 'Quarter Final',
            'Career_Goals': 180,
            'Career_Assists': 160,
            'Fun_Fact': 'Won Champions League & Ballon dOr 2024!'
        },
        'Harry Kane': {
            'Country': 'England',
            'Age': 31,
            'Club': 'Bayern Munich',
            'Position': 'Striker',
            'WC_2018': 'Golden Boot Winner',
            'WC_2022': 'Quarter Final',
            'Career_Goals': 350,
            'Career_Assists': 120,
            'Fun_Fact': 'England all-time top scorer!'
        },
        'Pedri': {
            'Country': 'Spain',
            'Age': 23,
            'Club': 'Barcelona',
            'Position': 'Midfielder',
            'WC_2018': 'Too young',
            'WC_2022': 'Round of 16',
            'Career_Goals': 80,
            'Career_Assists': 110,
            'Fun_Fact': 'Won Golden Boy award 2021!'
        },
        'Lautaro Martinez': {
            'Country': 'Argentina',
            'Age': 27,
            'Club': 'Inter Milan',
            'Position': 'Striker',
            'WC_2018': 'Not selected',
            'WC_2022': 'World Champion',
            'Career_Goals': 220,
            'Career_Assists': 85,
            'Fun_Fact': 'Scored in 2022 WC Final shootout!'
        },
        'Bukayo Saka': {
            'Country': 'England',
            'Age': 23,
            'Club': 'Arsenal',
            'Position': 'Winger',
            'WC_2018': 'Too young',
            'WC_2022': 'Quarter Final',
            'Career_Goals': 120,
            'Career_Assists': 140,
            'Fun_Fact': 'Arsenal youngest scorer in European competition!'
        },
        'Gavi': {
            'Country': 'Spain',
            'Age': 20,
            'Club': 'Barcelona',
            'Position': 'Midfielder',
            'WC_2018': 'Too young',
            'WC_2022': 'Round of 16',
            'Career_Goals': 45,
            'Career_Assists': 90,
            'Fun_Fact': 'Youngest Spain player to appear in WC!'
        },
        'Rodri': {
            'Country': 'Spain',
            'Age': 28,
            'Club': 'Manchester City',
            'Position': 'Midfielder',
            'WC_2018': 'Squad member',
            'WC_2022': 'Round of 16',
            'Career_Goals': 60,
            'Career_Assists': 95,
            'Fun_Fact': 'Won Ballon dOr 2024 & Champions League!'
        },
        'Leroy Sane': {
            'Country': 'Germany',
            'Age': 29,
            'Club': 'Bayern Munich',
            'Position': 'Winger',
            'WC_2018': 'Left out of squad',
            'WC_2022': 'Group Stage exit',
            'Career_Goals': 150,
            'Career_Assists': 180,
            'Fun_Fact': 'Controversially left out of 2018 WC winning squad!'
        },
    }
    return players

