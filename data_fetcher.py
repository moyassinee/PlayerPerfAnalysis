import soccerdata as sd

fbref = sd.FBref("ENG-Premier League", "2024-25")
player_stats = fbref.read_player_season_stats(stat_type="standard")
csv_path = "data/players_data.csv"
player_stats.to_csv(csv_path, index=False)