import pandas as pd

data = pd.read_csv('data/aggregate_data.csv')
X = data[[x for x in data if x != 'result']]
for x in X:
    X[x] = (X[x] - min(X[x]))/(max(X[x] - min(X[x])))

y = data[['result']]

netGenerator = NetworkGenerator()
networks = [None] * 10
for i in range(0, 10):
    networks[i] = netGenerator.generate()

genetic = Genetic(networks)

endNetworks = genetic.begin(X, y)