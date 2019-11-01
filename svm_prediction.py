from sklearn import svm

def predict(training, training_labels, to_predict, validation):
    print('USING SVM')
    clf = svm.SVC(gamma='scale')
    clf.fit(training, training_labels)
    predictions = clf.predict(to_predict)

    accurate = 0
    for i in range(len(to_predict)):
        if predictions[i] == validation[i]:
            accurate += 1

    accuracy = accurate / len(to_predict) * 100
    print('Accuracy: ', accuracy)
    return accuracy
