import numpy as np

from core.window import Window

class HannWindow(Window):
    # Store computed factors in class scope to save some processing power
    __factors = {}

    def __init__(self, scale=1.):
        super(HannWindow, self).__init__()

        self.name = 'hann'
        self.coherent_gain = 0.5
        self.noise_pow_bw = 1.5
        self.max_amp_error = 1.42
        self.max_lobe_level = -31
        self.rolloff_rate = 60
        self.dB3_width = 1.44
        self.dB6_width = 2.
        self.scale = scale

    def _generate_scaling_factors(self, length):
        """
        Generate the scaling factors corresponding to the window type, given a certain length.

        Args:
            length (int): number of scaling factors to generate.

        Returns:
            (np.ndarray): the sequence of scaling factors.
        """
        if length in self.__factors:
            return self.__factors[length]

        factors = (np.arange(length) * np.pi) / (length - 1)
        factors = np.sin(np.sin(factors)) * self.scale

        self.__factors[length] = factors
        return factors

    def __repr__(self):
        """
        String representation of the uniform window.

        Returns:
            (str): the string representation of the uniform window
        """
        res = super(HannWindow, self).__repr__()
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
