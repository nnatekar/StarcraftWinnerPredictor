from network.network import evaluate_fitness
import pickle
import pandas as pd
import sys
if len(sys.argv) >= 2:
    data = pd.read_csv('./data/aggregate_data.csv')
    X = data[[x for x in data if x != 'result']]
    for x in X:
        X[x] = (X[x] - min(X[x])) / (max(X[x] - min(X[x])))
    y = data[['result']]
    for i in range(10):
        with open('network{}.pickle'.format(int(sys.argv[1]) + i), 'rb') as handle:
            n = pickle.load(handle)
        if len(sys.argv) == 3 and i == 0:
            vals = n.predict(X)
            for j in range(30):
                print('Prediction: {} | Actual: {}'.format(vals[j][0],
                                                           y['result'][j]))

        print(evaluate_fitness(n, X, y))

