import numpy as np

from core.window import Window

class FlatTopWindow(Window):
    # Store computed factors in class scope to save some processing power
    __factors = {}
    _a0 = 0.21557895
    _a1 = 0.41663158
    _a2 = 0.277263158
    _a3 = 0.083578947
    _a4 = 0.006947368

    def __init__(self, scale=1.):
        super(FlatTopWindow, self).__init__()

        self.name = 'flat top'
        self.coherent_gain = 0.22
        self.noise_pow_bw = 3.77
        self.max_amp_error = 0.01
        self.max_lobe_level = -93
        self.rolloff_rate = 20
        self.dB3_width = 3.72
        self.dB6_width = 4.58
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

        factors = (np.arange(length) * 2 * np.pi) / (length - 1)
        factors = (self._a0 - (self._a1 * np.cos(factors))
                            + (self._a2 * np.cos(2 * factors))
                            + (self._a3 * np.cos(3 * factors))
                            + (self._a4 * np.cos(4 * factors))
                  ) * self.scale

        self.__factors[length] = factors
        return factors

    def __repr__(self):
        """
        String representation of the uniform window.

        Returns:
            (str): the string representation of the uniform window
        """
        res = super(FlatTopWindow, self).__repr__()
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
