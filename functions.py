import soccerdata as sd
import pandas as pd

#data_type can be "standard", "shooting", "passing", "passing_types", "goal_shot_creation", "defense", "possession", 
# "playing_time", "misc", "keeper","keeper_adv"

# available leagues : ['ENG-Premier League', 'ESP-La Liga', 'FRA-Ligue 1', 'GER-Bundesliga', 'ITA-Serie A']

#season format: "2023-24"

def read_players_data(fbref,data_type: str, league: str) -> pd.DataFrame:
    player_stats = fbref.read_player_season_stats(stat_type=data_type)
    player_stats = player_stats.reset_index()
    filtered_df = player_stats[player_stats['league'] == league]
    filtered_df.columns = filtered_df.columns.map('_'.join)
    return filtered_df

def read_teams_data(fbref,data_type: str, league: str) -> pd.DataFrame:
    team_stats = fbref.read_team_season_stats(stat_type=data_type)
    team_stats = team_stats.reset_index()
    filtered_df = team_stats[team_stats['league'] == league]
    filtered_df.columns = filtered_df.columns.map('_'.join)
    return filtered_df


def read_player_match_data(fbref,data_type: str, league: str) -> pd.DataFrame:
    players_stats = fbref.read_player_match_stats(stat_type=data_type)
    players_stats = players_stats.reset_index()
    filtered_df = players_stats[players_stats['league'] == league]
    filtered_df.columns = filtered_df.columns.map('_'.join)
    return filtered_df

def get_match_info(fbref, home_team, away_team) -> pd.DataFrame:
    match_info = fbref.read_schedule()
    match_info = match_info.reset_index()
    filtered_df = match_info[(match_info['home_team'].str.contains(home_team)) & (match_info['away_team'].str.contains(away_team))]
    return filtered_df


def get_players_match_stats(fbref, data_type: str, match_id: str) -> pd.DataFrame:
    match_info = fbref.read_player_match_stats(stat_type=data_type, match_id=match_id)
    match_info = match_info.reset_index()
    return match_info