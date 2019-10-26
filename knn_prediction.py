from sklearn.neighbors import KNeighborsClassifier

def distance(a, b):
    sum_a = sum(a[1:])
    sum_b = sum(b[1:])

    return abs(sum_a - sum_b)

def predict(K, training, training_labels, to_predict, validation):
    print('USING KNN')
    knn = KNeighborsClassifier(n_neighbors=K, metric=distance)
    knn.fit(training, training_labels)
    predictions = knn.predict(to_predict)

    accurate = 0
    for i in range(len(to_predict)):
        if predictions[i] == validation[i]:
            accurate += 1
    print('Accuracy: ', accurate / len(to_predict) * 100)
