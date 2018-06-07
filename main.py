import pandas as pd
from genetic.genetic import Genetic
from network.networkgenerator import NetworkGenerator
import pickle
from datetime import datetime
data = pd.read_csv('data/aggregate_data.csv')
X = data[[x for x in data if x != 'result']]
for x in X:
    X[x] = (X[x] - min(X[x]))/(max(X[x] - min(X[x])))

y = data[['result']]

netGenerator = NetworkGenerator(num_layers=4, num_inputs=11, num_neurons=5)
networks = [netGenerator.generate() for _ in range(10)]
progress_file = open('progress.txt', 'w')
progress_file.write('Start at {}').format(datetime.now())
progress_file.close()
for gen in range(10):
    genetic = Genetic(networks, X, numgens=500)
    networks = genetic.begin(X, y).items
    for i in range(10):

        with open('network{}.pickle', 'wb') as handle:
            pickle.dump(networks[i], handle, protocol=pickle.HIGHEST_PROTOCOL)
    progress_file = open('progress.txt', 'a')
    progress_file.write('Saved HOF for gen {}'.format((gen+1) * 500))
    progress_file.close()

