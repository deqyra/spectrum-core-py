import numpy as np

class Window:
    """
    An abstract representation of windows to put samples through before FFT-related operations.
    """

    def __init__(self):
        self.name = None
        self.coherent_gain = None
        self.noise_pow_bw = None
        self.max_amp_error = None
        self.max_lobe_level = None
        self.rolloff_rate = None
        self.dB3_width = None
        self.dB6_width = None

    def __str__(self):
        return '{} window'.format(self.name)

    def __repr__(self):
        """
        String representation of the abstract window.

        Returns:
            (str): the string representation of the abstract window
        """

        res =  '{}\n'.format(self.__class__.__name__)
        res += 'Characteristics:\n'
        res += 'Name: {}.\n'.format(self.name)
        res += 'Coherent gain: {}.\n'.format(self.coherent_gain)
        res += 'Noise power bandwidth: {}.\n'.format(self.noise_pow_bw)
        res += 'Worst-case amplitude error: {} dB.\n'.format(self.max_amp_error)
        res += 'Maximum side lobe level: {} dB.\n'.format(self.max_lobe_level)
        res += 'Side lobe rolloff rate: {} dB/decade.\n'.format(self.rolloff_rate)
        res += 'Main lobe width at -3dB: {} bins.\n'.format(self.dB3_width)
        res += 'Main lobe width at -6dB: {} bins\n.'.format(self.dB6_width)

        return res

    def _generate_scaling_factors(self, length):
        """
        Generate the scaling factors corresponding to the window type, given a certain length.

        Args:
            length (int): number of scaling factors to generate.

        Returns:
            (np.ndarray): the sequence of scaling factors.
        """

        raise NotImplementedError('Base Window.__generate_scaling_factors was called. A concrete window class might not be properly implemented.')

    def process(self, samples):
        """
        Effectively windows the input sample and returns it.

        Args:
            sample (np.ndarray): input samples to window.

        Returns:
            (nd.array): windowed samples
        """

        # The following is the basic template that basically implements the windowing.
        # It should not need to be overriden.
        factors = self._generate_scaling_factors(len(samples))

        return factors * samples
