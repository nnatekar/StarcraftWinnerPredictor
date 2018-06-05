import pandas as pd

data = pd.read_csv('aggregate_data.csv')
X = data[[x for x in data if x != 'result']]
for x in X:
    X[x] = (X[x] - min(X[x]))/(max(X[x] - min(X[x])))

y = data[['result']]



