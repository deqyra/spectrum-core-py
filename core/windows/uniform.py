import numpy as np

from core.window import Window

class UniformWindow(Window):
    def __init__(self, scale=1.):
        super(UniformWindow, self).__init__()

        self.name = 'uniform'
        self.coherent_gain = 1.
        self.noise_pow_bw = 1.
        self.max_amp_error = 3.92
        self.max_lobe_level = -13
        self.rolloff_rate = 20
        self.dB3_width = 0.89
        self.dB6_width = 1.21
        self.scale = scale

    def _generate_scaling_factors(self, length):
        """
        Generate the scaling factors corresponding to the window type, given a certain length.

        Args:
            length (int): number of scaling factors to generate.

        Returns:
            (np.ndarray): the sequence of scaling factors.
        """
        return np.asarray(length * [self.scale])

    def __repr__(self):
        """
        String representation of the uniform window.

        Returns:
            (str): the string representation of the uniform window
        """
        res = super(UniformWindow, self).__repr__()
        res += 'Parameters:\n'
        res += 'Scale: {}.\n'.format(self.scale)
        return res

    # def process(self, samples):
    #     """
    #     Effectively windows the input sample and returns it.
    #
    #     Args:
    #         sample (np.ndarray): input samples to window.
    #
    #     Returns:
    #         (nd.array): windowed samples
    #     """
    #
    #     factors = self.__generate_scaling_factors(len(samples))
    #     new_samples = factors * samples
    #
    #     return new_samples
