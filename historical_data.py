import requests
import pandas as pd

def get_away_id(game):
    if 'away' in game:
        return game['away']['teamId']
    else:
        return 'BYE'

def get_away_points(game):
    if 'away' in game:
        return game['away']['totalPoints']
    else:
        return 'BYE'

def get_team_name_by_id(id):
    if id == 1:
        return "Crusaders"
    elif id == 2:
        return "Crackers"
    elif id == 3:
        return "Afternoon Delights"
    elif id == 4:
        return "Monstars"
    elif id == 5:
        return "Bubba"
    elif id == 6:
        return "Uncle Bill"
    elif id == 7:
        return "Street Fighters"
    elif id == 8:
        return "Fuzzman"
    elif id == 9:
        return "Waiver Wire"
    elif id == 10:
        return "Hall"
    elif id == 11:
        return "Tommy"
    elif id == 12:
        return "Ram Rod"
    elif id == 13:
        return "Afternoon Delights"
    elif id == 14:
        return "Hulkamaniacs"
    elif id == 15:
        return "Farmer Fran"
    elif id == 16:
        return "Ed Horne Football Team"
    elif id == 'BYE':
        return id

def append_data_for_year(data, df):
    curr_year_df = [[
            game['matchupPeriodId'],
            get_team_name_by_id(game['home']['teamId']), game['home']['totalPoints'],
            get_team_name_by_id(get_away_id(game)), get_away_points(game), year
        ] for game in d['schedule']]
    curr_year_df = pd.DataFrame(curr_year_df, columns=columns)
    curr_year_df['Type'] = ['Regular' if w<=14 else 'Playoff' for w in curr_year_df['Week']]
    curr_year_df.head()
    df = df.append(curr_year_df)
    return df

league_id = 69673
starting_year = 2005
ending_year = 2020
url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + \
      str(league_id)

columns = ['Week', 'Team1', 'Score1', 'Team2', 'Score2', 'Year']
df = pd.DataFrame(columns=columns)

for year in range(starting_year, ending_year):
    r = requests.get(url, params={"seasonId":str(year), "view": "mMatchup"})
    d = r.json()[0]
    df = append_data_for_year(d, df)

# TODO: This isn't working:
url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2020/segments/0/leagues/" + \
      str(league_id)
r = requests.get(url, params={"view": "mMatchup"})
d = r.json()
df = append_data_for_year(d, df)

print(df)
df.to_csv("history.csv")


