import wave
from copy import deepcopy

import numpy as np

class Sample:
    """
    Encapsulates a raw wave, either read from a file or created from existing values.
    """

    def __init__(self, filename):
        if not filename:
            raise ValueError('Sample.__init__: filename is needed.')

        try:
            f = wave.open(filename, 'rb')
            self.n_channels, self.sample_width, self.sample_rate, self.length, self.compression, _ = f.getparams()
            self.bit_depth = 8 * self.sample_width

            if self.compression is not 'NONE':
                raise ValueError('Compression {} is not supported.'.format(self.compression))
            self.raw_data = f.readframes(self.length)

            self.__trim_channels()
            self.__compute_wave()
        except:
            raise ValueError('Sample.__init__: File {} could not be read properly as a Wave file.'.format(filename))

    def slice(self, start, end):
        if start < 0:
            raise ValueError('Sample.slice: `start` cannot be lower than 0.')
        if end > len(self.wave):
            raise ValueError('Sample.slice: `end` cannot be greater than wave data length.')
        if start >= end:
            raise ValueError('Sample.slice: `start` cannot be greater than or equal to `end`.')

        res = deepcopy(self)
        res.raw_data = self.raw_data[start:end]
        res.wave = self.wave[start:end]
        res.length = end - start
        return res

    def __compute_wave(self):
        # self.wave = np.asarray(b.to_int(self.raw_data, self.sample_width, little_endian=True))
        delattr(self, 'raw_data')

    def __trim_channels(self):
        if self.n_channels > 1:
            print('Sample.__trim_channels: {} audio channels were found. First channel only will be kept; others will be discarded.'.format(self.n_channels))
            # self.raw_data = b.periodic_strip(self.raw_data, self.sample_width, self.sample_width * self.n_channels)
            self.n_channels = 1
