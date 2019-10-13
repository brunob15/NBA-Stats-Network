import constants as const
import csv

ts = None

# Returns [vertexes, edges]
def build_graph(team_seasons, seasons_by_player, team_season_by_id):
    global ts
    ts = team_seasons

    vertexes = []
    edges = []

    vertex_id_offset = 1

    team_season_subset = 1
    player_subset = 2

    for team_season in list(team_seasons.keys()):
        team_season_id = team_seasons[team_season]['id']
        vertexes.append([team_season_id, team_season, team_season_subset])
        vertex_id_offset = team_season_id

    for player in list(seasons_by_player.keys()):
        player_id = vertex_id_offset + seasons_by_player[player]['id']
        vertexes.append([player_id, player, player_subset])

        player_seasons = seasons_by_player[player]['seasons']

        player_seasons = [[player_id, ts_id] for ts_id in map(get_team_season_id, player_seasons)]
        edges += player_seasons

    return [vertexes, edges]

def build_edge(player_id, season):
    season_id = ts[season[const.TEAM]]['id']
    return [player_id, season_id]

def get_team_season_id(season):
    team_season = season[const.TEAM] + '-' + str(int(season[const.YEAR]))
    return ts[team_season]['id']

################################################################

def export_csv(vertexes, edges):
    vertexes.insert(0, ['id', 'label', 'subset']) # csv file header

    with open('bipartite/vertexes.csv', 'w', newline='') as bip_vtx:
        writer = csv.writer(bip_vtx)
        writer.writerows(vertexes)
    bip_vtx.close()

    edges.insert(0, ['Source', 'Target']) # csv file header

    with open('bipartite/edges.csv', 'w', newline='') as bip_edges:
        writer = csv.writer(bip_edges)
        writer.writerows(edges)
    bip_edges.close()
