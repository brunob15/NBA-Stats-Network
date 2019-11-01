import sys

import preprocessing as prep
import datasets_prediction as ds
import knn_prediction as knn
import svm_prediction as svm

def main(arg):
    [seasons_by_player, team_seasons, team_season_by_id] = prep.preprocess()
    [teams, dataset, dataset_network, labels] = ds.build_datasets(team_seasons, team_season_by_id)

    K = 1

    season_to_predict = arg

    training, to_predict, training_labels, validation_labels = ds.partition_dataset(teams, dataset, labels, season_to_predict)
    training_net, to_predict_net, _, _ = ds.partition_dataset(teams, dataset_network, labels, season_to_predict)

    print()
    print('Predicting season', season_to_predict, 'with simple dataset')
    print()

    knn.predict(K, training, training_labels, to_predict, validation_labels)
    svm.predict(training, training_labels, to_predict, validation_labels)

    print()
    print('Predicting season', season_to_predict ,'using dataset with additional network data')
    print()

    #knn.predict(K, training_net, training_labels, to_predict_net, validation_labels)
    svm.predict(training_net, training_labels, to_predict_net, validation_labels)

if __name__ == "__main__":
   main(sys.argv[1])