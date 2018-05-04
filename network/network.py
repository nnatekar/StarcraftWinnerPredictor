from keras import Sequential
from keras.layers import Dense
import numpy as np
import pandas as pd

def load_network(filename):
    """Loads a neural network from the specified file name

    :param filename: name of file to read
    :return: New neural network with weights and structure specifiedi in file
    """
    file = open(filename, 'r')
    nid = int(filename.split('_')[1])
    structure = [int(i) for i in str(file.readline()).split(' ')[:-1]]
    activations = str(file.readline()).split(' ')[:-1]

    n = Network(structure[0], structure[1], structure[2], structure[3],
                activations, nid)
    weights = []
    layers = []
    for layer in range(structure[0]):
        layers.append(layer)
        weights.append([[float(num) for num in sl.split(' ')[:-1]]
                        for sl in str(file.readline()).split(';')[:-1]])
    n.set_weights(layers, weights)
    return n


class Network:
    """Wrapper class for keras neural networks

    """

    def __init__(self, num_layers, num_inputs, num_neurons, num_outputs,
                 activations, nid):
        """Initialize network.

        :param num_layers: number of layers
        :param num_inputs: number of inputs
        :param num_neurons: (list) number of neurons in each layer
        :param num_outputs: number of outputs
        :param activations: (list) activation functions for each layer
        """

        if num_layers < 2:
            raise ValueError('Invalid number of layers (must be ≥ 2')
        self.num_layers = num_layers
        self.num_inputs = num_inputs
        self.num_neurons = num_neurons
        self.num_outputs = num_outputs
        self.activations = activations

        self.model = Sequential()
        self.model.add(Dense(num_neurons, input_dim=num_inputs,
                       activation=activations[0]))

        [self.model.add(Dense(num_neurons, activation=activations[i + 1]))
         for i in range(self.num_layers - 2)]

        self.model.add(Dense(num_outputs, activation=activations[-1]))
        self.id = nid

    def set_weights(self, layer_numbers, weights):
        """Sets the weights for the specified layers to the specified weights.

        :param layer_numbers: list of layers you want to set weights for
        :param weights: list of
        :return: None
        """
        current_weight_number = 0
        for layer in layer_numbers:
            if layer < 0 or layer > self.num_layers:
                raise IndexError('Invalid layer number')
            if weights[current_weight_number][0].__class__ == \
                    self.get_weights(layer)[0].__class__:
                if len(weights[current_weight_number]) != len(self.get_weights(layer)) or len(
                        weights[current_weight_number][0]) != len(self.get_weights(layer)[0]) or \
                        len(weights[current_weight_number][0][0]) \
                        != len(self.get_weights(layer)[0][0]):
                    raise ValueError(
                        'Number of weights does not match number of nodes')
                else:
                    self.model.layers[layer].set_weights(weights[current_weight_number])
            else:
                weight = self.get_weights(layer)
                if len(weight[0]) != len(weights[current_weight_number]) or len(weight[0][0]) \
                        != len(weights[current_weight_number][0]):
                    raise ValueError(
                        'Number of weights does not match number of nodes')
                else:
                    for inp in range(len(weights[current_weight_number])):
                        for w in range(len(weights[current_weight_number][inp])):
                            weight[0][inp][w] = weights[current_weight_number][inp][w]
                    self.model.layers[layer].set_weights(weight)
            current_weight_number += 1

    def get_weights(self, layer):
        """Returns the weights for a given layer

        :param layer: layer to get weights for
        :return: numpy array of weights of the specified layer
        """
        if layer < 0 or layer > self.num_layers:
            raise IndexError('Invalid layer number')

        return self.model.layers[layer].get_weights()

    def write_to_file(self):
        """
        Writes all of the data from the network into a file
        :return: none
        """
        file = open('network_{}'.format(self.id), 'w')
        file.write('{} {} {} {} \n'.format(self.num_layers, self.num_inputs,
                                          self.num_neurons, self.num_outputs))
        acts = ''
        for act in self.activations:
            acts += act + ' '

        file.write(acts + '\n')
        for layer in range(self.num_layers):
            current_weights = self.get_weights(layer)[0]
            for neuron in current_weights:
                row = ''
                for item in neuron:
                    row += str(item) + ' '
                file.write(row + ';')
            file.write('\n')
        file.close()

    def predict(self, x):
        """Returns prediction values for each of the inputs

        :param x: list or numpy array of lists with size = num_inputs
        :return: list of size = len(x) of lists with size = num_outputs
        """
        if isinstance(x, type(pd.DataFrame())):
            if x.shape[1] != self.num_inputs:
                raise ValueError('Invalid number of inputs.')
        else:
            try:
                if len(x[0]) != self.num_inputs:
                    raise ValueError('Invalid number of inputs.')
            except TypeError:
                raise ValueError('Expected input with shape [n, num_inputs]')
            if not isinstance(x, type(np.array([1]))):
                x = np.array(x)
        return self.model.predict(x)

    def evaluate_fitness(self, x, y):
        """Runs the model on the samples, and then checks how many it predicted
         correctly.

        :param x: list or numpy array of lists with size = num_inputs
        :param y: list of the same size as x with the 0 or 1
        :return: float for percentage of results the model predicted correctly
        """

        if isinstance(x, type(pd.DataFrame())):
            if x.shape[1] != self.num_inputs:
                raise ValueError('Invalid number of inputs.')

            if isinstance(y, type(pd.DataFrame())) or isinstance(
                    y, type(pd.Series())):
                if x.shape[0] != y.shape[0]:
                    raise ValueError('Length of x and y differ.')
                if y.shape[1] != self.num_outputs:
                    raise ValueError('Invalid number of outputs.')
            else:
                if x.shape[0] != len(y):
                    raise ValueError('Length of x and y differ.')
                if len(y[0]) != self.num_outputs:
                    raise ValueError('Invalid number of outputs.')
        else:
            try:
                if len(x) != len(y):
                    raise ValueError('Length of x and y differ.')
                elif len(x[0]) != self.num_inputs:
                    raise ValueError('Invalid number of inputs.')
                elif len(y[0]) != self.num_outputs:
                    raise ValueError('Invalid number of outputs.')
            except TypeError:
                raise ValueError('Expected input with shape [n, num_inputs]')

            if not isinstance(x, type(np.array([1]))):
                x = np.array(x)

        if self.num_outputs == 1:
            predictions = [int(res[0]+.5) for res in self.model.predict(x)]
            return sum([1 if predictions[i] == y[i][0] else 0
                        for i in range(len(y))]) / len(y)
