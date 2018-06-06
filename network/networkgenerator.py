from network.network import Network

"""All code written by Yoav Kaliblotzky"""

current_id = 0

class NetworkGenerator:
    """Class to generate neural networks of a specific layout.

    """
    def __init__(self, num_layers, num_inputs, num_neurons, num_outputs=1,
                 activations = None):
        """Initialize a generator.

        :param num_layers: number of layers
        :param num_inputs: number of inputs
        :param num_neurons: number of neurons in hidden layers
        :param num_outputs: number of outputs
        :param activations: (list) activation functions for each layer
        """
        self.num_neurons = num_neurons
        self.num_layers = num_layers
        if activations:
            self.activation = activations
        else:
            self.activation = ['sigmoid' for _ in range(num_layers - 1)]
            self.activation.append('sigmoid')
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        global current_id
        self.id = current_id
        current_id += 1
        self.networks_created = 0

    def __str__(self):
        return '{}: num_neurons = {}, num_layers = {}, activation = {}'.format(
            self.__class__,
            self.num_neurons,
            self.num_layers,
            self.activation)

    def generate(self):
        """Generates a neural network with the given structure specified.

        :return: New neural network with specfied structure and random weights
        """
        self.networks_created += 1
        return Network(self.num_layers, self.num_inputs, self.num_neurons,
                       self.num_outputs, self.activation,
                       self.networks_created - 1)
