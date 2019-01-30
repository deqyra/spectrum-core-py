from copy import deepcopy


class Sample:
    """
    Encapsulates a raw wave, either read from a file or created from existing values.
    """

    def __init__(self, wave, sample_rate, sample_width):
        self.wave = wave
        self.length = len(wave)

        self.sample_rate = sample_rate
        self.sample_width = sample_width
        self.bit_depth = 8 * sample_width

    def slice(self, start, end):
        if start < 0:
            raise ValueError('Sample.slice: `start` cannot be lower than 0.')
        if end > len(self.wave):
            raise ValueError('Sample.slice: `end` cannot be greater than wave data length.')
        if start > end:
            raise ValueError('Sample.slice: `start` cannot be greater than `end`.')

        return Sample(deepcopy(self.wave[start:end]), self.sample_rate, self.sample_width)
