import pandas as pd
from genetic.genetic import Genetic
from network.network import Network
from network.networkgenerator import NetworkGenerator
data = pd.read_csv('aggregate_data.csv')
X = data[[x for x in data if x != 'result']]
for x in X:
    X[x] = (X[x] - min(X[x]))/(max(X[x] - min(X[x])))

y = data[['result']]

netGenerator = NetworkGenerator(num_layers=4, num_inputs=11, num_neurons=5)
networks = [netGenerator.generate() for _ in range(10)]

genetic = Genetic(networks, X)
endNetworks = genetic.begin(X, y)
