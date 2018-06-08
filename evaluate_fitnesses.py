from network.network import evaluate_fitness
import pickle
import pandas as pd
import sys
data = pd.read_csv('./data/aggregate_data.csv')
X = data[[x for x in data if x != 'result']]
for x in X:
    X[x] = (X[x] - min(X[x]))/(max(X[x] - min(X[x])))
if len(sys.argv) == 1:
    y = data[['result']]
    for i in range(10):
        with open('network{}.pickle'.format(int(sys.argv[0]) + i), 'rb') as handle:
            n = pickle.load(handle)

        print(evaluate_fitness(n, X, y))
