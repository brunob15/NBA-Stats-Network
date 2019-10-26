import preprocessing as prep
import datasets_prediction as ds
import knn_prediction as knn
import svm_prediction as svm

[seasons_by_player, team_seasons, team_season_by_id] = prep.preprocess()
[teams, dataset, dataset_network, labels] = ds.build_datasets(team_seasons, team_season_by_id)

K = 1
seasons_predicted = 3
n_predict = seasons_predicted * 30

training = dataset[:-n_predict]
to_predict = dataset[-n_predict:]

training_net = dataset_network[:-n_predict]
to_predict_net = dataset_network[-n_predict:]

training_labels = labels[:-n_predict]
validation = labels[-n_predict:]

print('Predicting with simple dataset')
print('Seasons to be predicted: ', seasons_predicted)

knn.predict(K, training, training_labels, to_predict, validation)
svm.predict(training, training_labels, to_predict, validation)

print()
print('Predicting using dataset with additional network data')
print('Seasons to be predicted: ', seasons_predicted)

knn.predict(K, training_net, training_labels, to_predict_net, validation)
svm.predict(training_net, training_labels, to_predict_net, validation)
