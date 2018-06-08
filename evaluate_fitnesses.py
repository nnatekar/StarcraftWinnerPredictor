from network.network import evaluate_fitness
import pickle
import pandas as pd
import sys
from random import randint

data = pd.read_csv('./data/aggregate_data.csv')
X = data[[x for x in data if x != 'result']]
for x in X:
    X[x] = (X[x] - min(X[x])) / (max(X[x] - min(X[x])))
y = data[['result']]

# Argument is starting number (network620, network70, etc.)
if len(sys.argv) == 2 or len(sys.argv) == 3:
    for i in range(10):
        with open('network{}.pickle'.format(int(sys.argv[1]) + i), 'rb') as handle:
            n = pickle.load(handle)
        if len(sys.argv) == 3 and i == 0:
            vals = n.predict(X)
            for j in range(30):
                print('Prediction: {} | Actual: {}'.format(vals[j][0],
                                                           y['result'][j]))

        print(evaluate_fitness(n, X, y))

# argv[1] = start, argv[2] = end, argv[3] = interval in between
elif len(sys.argv) == 4:
    for i in range(int((int(sys.argv[2])-int(sys.argv[1]))/int(sys.argv[3]))):
        print(int(sys.argv[1]) + i * int(sys.argv[3]))
        num = randint(0,9)
        with open('network{}.pickle'.format(int(sys.argv[1]) + num * int(sys.argv[3])), 'rb') as handle:
            n = pickle.load(handle)

        print('--Gen {}--'.format(i + 1))
        print(evaluate_fitness(n, X, y))
        print('++++')
        vals = n.predict(X)
        for j in range(10):
            print('Prediction: {} | Actual: {}'.format(vals[j][0],
                                                       y['result'][j]))

