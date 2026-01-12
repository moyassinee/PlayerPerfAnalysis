import soccerdata as sd
import pandas as pd
from mplsoccer import Radar, FontManager, grid

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