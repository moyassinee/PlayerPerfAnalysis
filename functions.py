import soccerdata as sd
import pandas as pd

#data_type can be "standard", "shooting", "passing", "passing_types", "goal_shot_creation", "defense", "possession", 
# "playing_time", "misc", "keeper","keeper_adv"

# available leagues : ['ENG-Premier League', 'ESP-La Liga', 'FRA-Ligue 1', 'GER-Bundesliga', 'ITA-Serie A']

def read_players_data(data_type: str, league: str) -> pd.DataFrame:
    fbref = sd.FBref("Big 5 European Leagues Combined", "2024-25")
    player_stats = fbref.read_player_season_stats(stat_type=data_type)
    player_stats = player_stats.reset_index()
    filtered_df = player_stats[player_stats['league'] == league]
    return filtered_df

#read team data
def read_teams_data(data_type: str, league: str) -> pd.DataFrame:
    fbref = sd.FBref("Big 5 European Leagues Combined", "2024-25")
    team_stats = fbref.read_team_season_stats(stat_type=data_type)
    team_stats = team_stats.reset_index()
    filtered_df = team_stats[team_stats['league'] == league]
    return filtered_df