import wave
from copy import deepcopy

from core.io import AudioFileReader
from core.sample import Sample
from util.byte_tools import ByteTools as b

import numpy as np

class WavReader(AudioFileReader):
    def __init__(self, filename):
        super(WavReader, self).__init__()
        
        if not filename:
            raise ValueError('WavReader.__init__: filename is needed.')
        self.filename = filename

    def read(self):
        try:
            f = wave.open(self.filename, 'rb')
            n_channels, self.sample_width, self.sample_rate, length, compression, _ = f.getparams()

            if compression is not 'NONE':
                raise ValueError('Compression {} is not supported.'.format(compression))

            data = f.readframes(length)
            if n_channels > 1:
                print('WavReader.__trim_channels: {} audio channels were found. First channel only will be kept; others will be discarded.'.format(n_channels))
                data = b.periodic_strip(data, self.sample_width, self.sample_width * n_channels)

            self.wave = np.asarray(b.to_int(data, self.sample_width, little_endian=True))

        except:
            raise ValueError('WavReader.__init__: File {} could not be read properly as a Wave file.'.format(self.filename))

    def get_sample(self):
        if not hasattr(self, 'wave'):
            self.read()
        return Sample(deepcopy(self.wave), self.sample_rate, self.sample_width)
