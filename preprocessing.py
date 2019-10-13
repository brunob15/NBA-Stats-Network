import numpy as numpy
import pandas as pandas
import math
import itertools

YEAR_INDEX = 1
PLAYER_INDEX = 2
TEAM_INDEX = 5
MINUTES_PLAYED_INDEX = 8

dataset_path = 'C:/Users/bruno/Documents/FING/AR/proyecto/Seasons_Stats.csv'

dataset = pandas.read_csv(dataset_path, delimiter=',')
dataset_length = len(dataset)

np_dataset = dataset.to_numpy()

seasons_by_player = {}
player_name_by_id = {}
team_seasons = {}
team_season_by_id = {}

MIN_YEAR = 1975
MIN_MINUTES_PLAYED = 1000

# Returns [seasons_by_player, team_seasons]
def preprocess():
    player_id = 0

    for row in np_dataset:
        year = row[YEAR_INDEX]

        # Discard all data prior to 1975
        if year >= MIN_YEAR:
            player = row[PLAYER_INDEX]
            minutes_played = row[MINUTES_PLAYED_INDEX]
            team = row[TEAM_INDEX]

            if not (isinstance(player, float) and math.isnan(player)): # Discard rows with no player
                # When a player played for more than one team in one season
                # there is a row with TEAM = 'TOT' that sums the stats of that player
                # for all teams he played for in that season (redundant minutes played).
                # I discard that row.
                if team != 'TOT':
                    if player in seasons_by_player:
                        seasons_by_player[player]['seasons'].append(row)
                        seasons_by_player[player]['minutes'] += minutes_played
                    else:
                        seasons_by_player[player] = {}
                        seasons_by_player[player]['seasons'] = [row]
                        seasons_by_player[player]['minutes'] = minutes_played
                        seasons_by_player[player]['id'] = player_id

                        player_name_by_id[player_id] = player

                        player_id += 1

    # Discard all players that played less than 1000 minutes in their careers
    for player in list(seasons_by_player.keys()):
        if seasons_by_player[player]['minutes'] < MIN_MINUTES_PLAYED:
            del seasons_by_player[player]

    players_filtered = list(seasons_by_player.keys())

    team_season_id = 1
    for row in np_dataset:
        year = row[YEAR_INDEX]

        # Discard all data prior to 1975
        if year >= MIN_YEAR:
            player = row[PLAYER_INDEX]
            minutes_played = row[MINUTES_PLAYED_INDEX]
            team = row[TEAM_INDEX]

            if not (isinstance(player, float) and math.isnan(player)):
                if player in players_filtered:
                    # Discard rows with no player
                    # When a player played for more than one team in one season
                    # there is a row with TEAM = 'TOT' that sums the stats of that player
                    # for all teams he played for in that season (redundant minutes played).
                    # I discard that row.
                    if team != 'TOT':
                        year = str(int(year))
                        team_season = team + '-' + year

                        if team_season in team_seasons:
                            team_seasons[team_season]['player-stats'].append(row)
                        else:
                            team_seasons[team_season] = {}
                            team_seasons[team_season]['player-stats'] = [row]
                            team_seasons[team_season]['id'] = team_season_id

                            team_season_by_id[team_season_id] = team_season

                            team_season_id += 1

    return [seasons_by_player, team_seasons, player_name_by_id]
