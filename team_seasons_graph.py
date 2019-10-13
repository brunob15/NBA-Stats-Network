# Calculate edges in team-seasons graph

def build_graph(seasons_by_player):
    team_seasons_sharing_players = {}

    for player in list(seasons_by_player.keys()):
        seasons = seasons_by_player[player]['seasons']
        seasons_mapped = [season[TEAM_INDEX] + '-' + str(int(season[YEAR_INDEX])) for season in seasons]

        team_seasons_pairs = list(itertools.combinations(seasons_mapped, 2))

        #for pair in team_seasons_pairs:
