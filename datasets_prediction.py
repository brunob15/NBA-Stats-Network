import pandas
import re

import constants as const
import team_seasons_graph as ts

tsn = None

def build_datasets(team_seasons, team_season_by_id):
    neighbors = build_network_dataset(team_seasons, team_season_by_id)

    teams = []
    dataset = []
    dataset_network = []
    labels = []

    for (ts, ts_data) in team_seasons.items():
        teams.append(ts)
        dataset.append(dataset_example(ts, ts_data))
        dataset_network.append(dataset_network_example(ts, ts_data, neighbors))
        labels.append(ts_data['playoffs'])

    return [teams, dataset, dataset_network, labels]

# An example contains the Win Share stats for the 12 most relevant players
# in descendant order
def dataset_example(ts, ts_data):
    example = []
    for player_stats in ts_data['player-stats']:
        example.append(player_stats[const.WIN_SHARE])

    example.sort(reverse=True)
    example = example[:12]

    # Complete with 0 WS if less than 12 players
    fields_missing = 12 - len(example)
    if fields_missing > 0:
        for i in range(fields_missing):
            example.append(0)

    return example

def get_last_stat():


# An example contains the Win Share stats for the 12 most
# relevant players in descendant order plus the label of the
# N team-seasons that share more players. This is extended with network information
def dataset_network_example(ts, ts_data, neighbors):
    return dataset_example(ts, ts_data) + neighbors[ts]

def second(tuple):
    return tuple[1]

def build_network_dataset(team_seasons, team_season_by_id):
    ts_edges = pandas.read_csv('exported_csv/team_seasons/edges.csv', delimiter=',').to_numpy()
    ts_nodes = pandas.read_csv('exported_csv/team_seasons/vertexes.csv', delimiter=',').to_numpy()
    ts_nodes = list(map(list, ts_nodes))

    global tsn
    tsn = ts_nodes

    neighbors = build_neighbors(ts_edges, team_season_by_id)
    neighbors

    return neighbors
    

def build_neighbors(ts_edges, team_season_by_id):
    neighbors = {}

    for edge in ts_edges:
        neighbor_a = team_season_by_id[edge[0]]
        neighbor_b = team_season_by_id[edge[1]]
        players_shared = edge[2]

        if neighbor_a in neighbors:
            neighbors[neighbor_a].append([neighbor_b, players_shared])
        else:
            neighbors[neighbor_a] = [[neighbor_b, players_shared]]

        if neighbor_b in neighbors:
            neighbors[neighbor_b].append([neighbor_a, players_shared])
        else:
            neighbors[neighbor_b] = [[neighbor_a, players_shared]]
        
    for neigh in list(neighbors.values()):
        neigh.sort(reverse=True, key=second)

    neighbors = label_neighbors(neighbors)

    return neighbors

def to_label(neigh):
    result = None

    for node in tsn:
        if neigh[0] == node[1]:
            result = node[2]
            break

    return result

def label_neighbors(neighbors):
    for ts in list(neighbors.keys()):
        neighbors[ts] = list(map(to_label, neighbors[ts]))[:5]

    return neighbors

##################################################################
##################################################################

def partition_dataset(teams, dataset, labels, season_to_predict):
    training = []
    to_predict = []
    training_labels = []
    validation_labels = []

    for index, row in enumerate(dataset):
        if re.search(season_to_predict, teams[index]):
            to_predict.append(row)
            validation_labels.append(labels[index])
        else:
            training.append(row)
            training_labels.append(labels[index])

    return [training, to_predict, training_labels, validation_labels]
