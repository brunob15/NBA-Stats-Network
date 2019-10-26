import itertools
import csv
import constants as const

ts = None

# Calculate edges in team-seasons graph
def build_graph(team_seasons):
    global ts
    ts = team_seasons

    print('Building TeamSeasons Graph')

    nodes = list(team_seasons.keys()) # Nodes are team-seasons
    edges = list(map(list, itertools.combinations(nodes, 2)))
    nodes = list(map(to_node, nodes))

    print('Creating edges...')

    i = 1
    edges_count = len(edges)
    for edge in edges:
        team_season_a = team_seasons[edge[0]]
        team_season_b = team_seasons[edge[1]]

        players_ts_a = map(player_name, team_season_a['player-stats'])
        players_ts_b = map(player_name, team_season_b['player-stats'])

        players_shared = list(set(players_ts_a) & set(players_ts_b)) # Intersection
        count_players_shared = len(players_shared)

        print(i, '/', edges_count, end='\r')
        i += 1

        if count_players_shared > 0:
            edge[0] = team_season_a['id']
            edge[1] = team_season_b['id']
            edge.append(count_players_shared)
        else:
            edges.remove(edge)

    print('Finished building TeamSeasons graph')

    return [nodes, edges]


def filter_edges(edges):
    for edge in edges:
        year_a = int(edge[0].split('-')[1])
        year_b = int(edge[1].split('-')[1])

        if abs(year_a - year_b) > const.MAX_YEAR_INTERVAL:
            edges.remove(edge)

    return edges

def to_node(team_season):
    return [ts_id(team_season), team_season, ts[team_season]['playoffs']]

def ts_id(team_season):
    return ts[team_season]['id']

def player_name(ts):
    return ts[const.PLAYER_NAME]

def export_csv(nodes, edges):
    nodes.insert(0, ['id', 'label', 'playoffs']) # csv file header

    with open('exported_csv/team_seasons/vertexes.csv', 'w', newline='') as ts_vtx:
        writer = csv.writer(ts_vtx)
        writer.writerows(nodes)
    ts_vtx.close()

    edges.insert(0, ['Source', 'Target', 'PlayersShared']) # csv file header

    with open('exported_csv/team_seasons/edges.csv', 'w', newline='') as ts_edges:
        writer = csv.writer(ts_edges)
        writer.writerows(edges)
    ts_edges.close()
