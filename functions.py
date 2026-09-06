import soccerdata as sd
import pandas as pd
import numpy as np
from mplsoccer import Radar, FontManager, grid
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

#data_type can be "standard", "shooting", "passing", "passing_types", "goal_shot_creation", "defense", "possession", 
# "playing_time", "misc", "keeper","keeper_adv"

# available leagues : ['ENG-Premier League', 'ESP-La Liga', 'FRA-Ligue 1', 'GER-Bundesliga', 'ITA-Serie A']

#season format: "2023-24"

def read_players_data(fbref,data_type: str, league = None) -> pd.DataFrame:
    player_stats = fbref.read_player_season_stats(stat_type=data_type)
    player_stats = player_stats.reset_index()
    if league == None:
        pass
    else:
        player_stats = player_stats[player_stats['league'] == league]
    player_stats.columns = player_stats.columns.map('_'.join)
    return player_stats

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
    


def plot_radar_chart_to_compare(df_player1, df_player2,min_scale=0, max_scale=3):
    # Parameters
    URL4 = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf'
    robotto_thin = FontManager(URL4)
    URL5 = ('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
        'RobotoSlab%5Bwght%5D.ttf')
    robotto_bold = FontManager(URL5)
    params = df_player1.columns.tolist()


    min_range = df_player2[params].min().tolist()
    max_range = df_player2[params].max().tolist()

    padding = 0.05  # 5%

    min_range = [
        m - padding * (M - m) for m, M in zip(min_range, max_range)
    ]
    max_range = [
        M + padding * (M - m) for m, M in zip(min_range, max_range)
    ]

    player1_values = df_player1.loc[0].values.tolist()
    player2_values = df_player2.loc[0].values.tolist()
    
    radar = Radar(params, min_range, max_range)
    fig, axs = grid(figheight=10, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                    title_space=0, endnote_space=0, grid_key='radar', axis=False)

    # plot the radar
    radar.setup_axis(ax=axs['radar'], facecolor='None')

    rings_inner = radar.draw_circles(ax=axs['radar'],facecolor='#28252c', edgecolor='#39353f', lw=1.5)  # draw circles
    radar_output = radar.draw_radar_compare(player1_values, player2_values, ax=axs['radar'],
                                            kwargs_radar={'facecolor': "#098023", 'alpha': 0.6},
                                            kwargs_compare={'facecolor': "#257ecc", 'alpha': 0.6})
    radar_poly, radar_poly2, vertices1, vertices2 = radar_output
    range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=15, color='#fcfcfc',
                                       fontproperties=robotto_thin.prop)
    param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=15, color='#fcfcfc',
                                       fontproperties=robotto_thin.prop)

    endnote_text = axs['endnote'].text(0.99, 0.5, 'Data From: FBref', fontsize=8,
                                    fontproperties=robotto_thin.prop, ha='right', va='center')
    title1_text = axs['title'].text(0.01, 0.65, 'Ayman Berkok', fontsize=15,
                                    fontproperties=robotto_bold.prop, ha='left', va='center', color= "#098023")
    title2_text = axs['title'].text(0.01, 0.25, 'Bundesliga shooting perf', fontsize=10,
                                    fontproperties=robotto_thin.prop,
                                    ha='left', va='center', color='#B6282F')
    title3_text = axs['title'].text(0.99, 0.65, 'All players', fontsize=15,
                                    fontproperties=robotto_bold.prop, ha='right', va='center', color= "#257ecc")
    title4_text = axs['title'].text(0.99, 0.25, 'Bundesliga shooting perf', fontsize=10,
                                    fontproperties=robotto_thin.prop,
                                    ha='right', va='center', color='#B6282F')
    
    fig.set_facecolor('#121212')


def parse_age(age_str) -> float:
    """'24-013' -> 24 + 13/365 ; '24' -> 24.0 ; NaN-safe."""
    if pd.isna(age_str):
        return np.nan
    s = str(age_str)
    if "-" in s:
        years, days = s.split("-")
        try:
            return float(years) + float(days) / 365
        except ValueError:
            return np.nan
    try:
        return float(s)
    except ValueError:
        return np.nan

    
def map_position(pos_str) -> str | None:
    if pd.isna(pos_str):
        return None
    s = str(pos_str)
    if "GK" in s:
        return "GK"
    if "DF" in s:
        return "DF"
    if "MF" in s:
        return "MF"
    if "FW" in s:
        return "FW"
    return None


def get_similar_players(player_name: str, df: pd.DataFrame, features: list, top_n: int = 10,
                         min_90s: float = 10) -> pd.DataFrame:
    
    row = df[df["player_"] == player_name]
    if row.empty:
        raise ValueError(f"'{player_name}' not found. Use search_players() to check spelling.")
    pos_group = row["pos_group"].iloc[0]
    if pos_group not in features or not features[pos_group]:
        raise ValueError(f"No feature set defined yet for position group '{pos_group}'.")
 
    features = [f for f in features[pos_group] if f in df.columns]
    pool = df[(df["pos_group"] == pos_group) & (df["90s_"] >= min_90s)].copy()
    if player_name not in pool["player_"].values:
        pool = pd.concat([pool, row])  # keep target even if below min_90s
 
    X = pool[features].fillna(pool[features].median())
    X_scaled = StandardScaler().fit_transform(X)
 
    idx = pool.index.get_loc(pool[pool["player_"] == player_name].index[0])
    target_vec = X_scaled[idx].reshape(1, -1)
    pool["similarity_score"] = cosine_similarity(target_vec, X_scaled)[0]
 
    return (
        pool[pool["player_"] != player_name]
        .sort_values("similarity_score", ascending=False)
        [["player_", "team_", "age_", "pos_", "similarity_score"]]
        .head(top_n)
        .reset_index(drop=True)
    )

def search_players(query: str, df: pd.DataFrame) -> pd.DataFrame:
    """Case-insensitive substring search, e.g. search_players('salah', df_agg)."""
    return df[df["player_"].str.contains(query, case=False, na=False)][["player_", "team_", "pos_", "age_"]]

def interactive_similarity(df: pd.DataFrame,features, top_n: int = 10):
    query = input("Search player name: ").strip()
    matches = search_players(query, df)
    if matches.empty:
        print("No matches found.")
        return
    matches = matches.reset_index(drop=True)
    print(matches)
    choice = int(input(f"Pick a row number (0-{len(matches) - 1}): "))
    player_name = matches.loc[choice, "player_"]
    result = get_similar_players(player_name, df,features, top_n=top_n)
    print(f"\nMost similar players to {player_name} ({matches.loc[choice, 'pos_']}):\n")
    print(result.to_string(index=False))
    return result