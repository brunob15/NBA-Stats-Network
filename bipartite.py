import constants as const
import csv

ts = None

# Returns [vertexes, edges]
def build_graph(team_seasons, seasons_by_player):
    print('Building Bipartite Graph')
    global ts
    ts = team_seasons

    vertexes = []
    edges = []

    vertex_id_offset = 1

    team_season_subset = 1
    player_subset = 2

    default_value = -1

    for team_season in list(team_seasons.keys()):
        team_season_id = team_seasons[team_season]['id']
        standing = team_seasons[team_season]['standing']
        playoffs = team_seasons[team_season]['playoffs']

        vertexes.append([team_season_id, team_season, team_season_subset, standing, playoffs])
        vertex_id_offset = team_season_id

    for player in list(seasons_by_player.keys()):
        player_id = vertex_id_offset + seasons_by_player[player]['id']
        vertexes.append([player_id, player, player_subset, default_value, default_value])

        player_seasons = seasons_by_player[player]['seasons']

        seasons = []
        for season in player_seasons:
            seasons.append(build_edge(player_id, season))
        
        edges += seasons

    return [vertexes, edges]

def build_edge(player_id, season):
    team_season = season[const.TEAM] + '-' + str(int(season[const.YEAR]))
    season_id = ts[team_season]['id']

    return [player_id, season_id, player_weight(season)]

def player_weight(season):
    win_share = season[const.WIN_SHARE]
    return win_share

################################################################

def export_csv(vertexes, edges):
    vertexes.insert(0, ['id', 'label', 'subset', 'standing', 'playoffs']) # csv file header

    with open('exported_csv/bipartite/vertexes.csv', 'w', newline='') as bip_vtx:
        writer = csv.writer(bip_vtx)
        writer.writerows(vertexes)
    bip_vtx.close()

    edges.insert(0, ['Source', 'Target', 'PlayerPerformance']) # csv file header

    with open('exported_csv/bipartite/edges.csv', 'w', newline='') as bip_edges:
        writer = csv.writer(bip_edges)
        writer.writerows(edges)
    bip_edges.close()
