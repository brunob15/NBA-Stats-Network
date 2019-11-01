import csv
import matplotlib.pyplot as plt
import pandas as pd

import preprocessing as prep
import datasets_prediction as ds
import knn_prediction as knn
import svm_prediction as svm

def last_two_digits(num):
    return num[-2:]

[seasons_by_player, team_seasons, team_season_by_id] = prep.preprocess()
[teams, dataset, dataset_network, labels] = ds.build_datasets(team_seasons, team_season_by_id)

#K = 1

# Seasons from 1975 to 2017
seasons_to_predict = list(map(str, list(range(1975, 2018))))

data = [['season', 'accuracy', 'accuracy_net']]

accs = []
accs_net = []

for season in seasons_to_predict:
    training, to_predict, training_labels, validation_labels = ds.partition_dataset(teams, dataset, labels, season)
    training_net, to_predict_net, _, _ = ds.partition_dataset(teams, dataset_network, labels, season)

    #knn.predict(K, training, training_labels, to_predict, validation_labels)
    accuracy = svm.predict(training, training_labels, to_predict, validation_labels)
    accs.append(accuracy)

    #knn.predict(K, training_net, training_labels, to_predict_net, validation_labels)
    accuracy_net = svm.predict(training_net, training_labels, to_predict_net, validation_labels)
    accs_net.append(accuracy_net)

    data.append([season, accuracy, accuracy_net])

seasons = list(map(last_two_digits, seasons_to_predict))
df = pd.DataFrame({'seasons': seasons, 'accs': accs, 'accs_net': accs_net})

plt.style.use('ggplot')
plt.plot('seasons', 'accs', data=df, color='blue', linewidth=2, marker='D', label='Accuracy')
plt.plot('seasons', 'accs_net', data=df, color='red', linewidth=2, marker='o',label='Accuracy with network data')
plt.xlabel('Season')
plt.ylabel('Accuracy')
plt.legend(loc='upper left')
plt.show()

with open('exported_csv/predictions.csv', 'w', newline='') as pred:
    writer = csv.writer(pred)
    writer.writerows(data)
pred.close()
