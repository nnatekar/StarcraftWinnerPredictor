from keras import Sequential
from keras.layers import Dense

class Network:
    '''Wrapper class for keras neural networks

    '''

    def __init__(self, num_layers, num_inputs, num_neurons, num_outputs,
                 activations):
        '''Initialize network.

        :param num_layers: number of layers
        :param num_inputs: number of inputs
        :param num_neurons: (list) number of neurons in each layer
        :param num_outputs: number of outputs
        :param activations: (list) activation functions for each layer
        '''

        if num_layers < 2:
            raise ValueError('Invalid number of layers (must be ≥ 2')
        self.num_layers = num_layers

        self.model = Sequential()
        self.model.add(Dense(num_neurons, input_dim=num_inputs,
                       activation=activations[0]))

        [self.model.add(Dense(num_neurons, activation=activations[i + 1]))
         for i in range(self.num_layers - 2)]

        self.model.add(Dense(num_outputs, activation=activations[-1]))

    def set_weights(self, layer_numbers, weights):
        """

        :param layer_numbers: list of layers you want to set weights for
        :param weights: list of
        :return: None
        """

        # Switch to check weights at layer using get layer or something
        for layer in layer_numbers:
            if layer < 0 or layer > self.num_layers:
                raise IndexError('Invalid layer number')
            elif layer == 0 and len(weights[layer]) != self.num_inputs:
                raise ValueError(
                    'Number of weights does not match number of nodes')
            elif layer == self.num_layers and (
                    len(weights[layer]) != self.num_outputs):
                raise ValueError(
                    'Number of weights does not match number of nodes')
            elif len(weights[layer]) != self.num_neurons:
                raise ValueError(
                    'Number of weights does not match number of nodes')
            else:
                old_weight[layer] = weights[layer]


