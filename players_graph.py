import constants as const
import itertools
import csv

sbp = {}

# Calculate count of edges in players graph
def players_edges_count(team_seasons):
    count_players_edges = 0

    for players in list(team_seasons.values()):
        n = len(players['player-stats'])  # n = count players in team-season
        edges_in_complete_subgraph = int(n * (n-1) / 2)
        count_players_edges += edges_in_complete_subgraph

    print('Cantidad aristas en grafo de jugadores: ', count_players_edges)

def build_graph(team_seasons, seasons_by_player):
    global sbp
    sbp = seasons_by_player

    edges = []
    vertexes = []

    for player in list(seasons_by_player.keys()):
        vertexes.append([get_player_id(player), player])

    for ts in list(team_seasons.values()):
        player_relations = itertools.combinations(ts['player-stats'], 2)
        # Discard all edges with non-positive weight
        edges += list(filter(None, map(build_edge, player_relations)))

    return [vertexes, edges]

######################## HELPERS #########################

def get_player_id(player_name):
    return sbp[player_name]['id']

def to_tuple(player_stats):
    player_name = player_stats[const.PLAYER_NAME]
    return (get_player_id(player_name), player_name)

def player_val(player):
    return player[const.WIN_SHARE]

def player_relation_val(val_player_a, val_player_b):
    return val_player_a + val_player_b

def build_edge(relation):
    player_a = relation[0]
    player_b = relation[1]

    value_player_a = player_val(player_a)
    value_player_b = player_val(player_b)

    relation_value = player_relation_val(value_player_a, value_player_b)

    if relation_value > 0:  
        player_a_id = sbp[player_a[const.PLAYER_NAME]]['id']
        player_b_id = sbp[player_b[const.PLAYER_NAME]]['id']

        return [player_a_id, player_b_id, relation_value]
    else:
        return None


#################### EXPORT ######################

def export_csv(players_vtx, players_edges):
    players_vtx.insert(0, ['id', 'label']) # csv file header

    with open('exported_csv/players/vertexes.csv', 'w', newline='') as ply_vtx:
        writer = csv.writer(ply_vtx)
        writer.writerows(players_vtx)
    ply_vtx.close()

    players_edges.insert(0, ['Source', 'Target', 'Win_Share']) # csv file header

    with open('exported_csv/players/edges.csv', 'w', newline='') as ply_edges:
        writer = csv.writer(ply_edges)
        writer.writerows(players_edges)
    ply_edges.close()
