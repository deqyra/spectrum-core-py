import wave
from copy import deepcopy

from core.io import AudioFileWriter
from core.sample import Sample
from util.byte_tools import ByteTools as b

import numpy as np


class WavWriter(AudioFileWriter):
    def __init__(self, filename):
        super(WavWriter, self).__init__()

        if not filename:
            raise ValueError('WavReader.__init__: filename is needed.')
        self.filename = filename

    def write(self, sample):
        try:
            f = wave.open(self.filename, 'wb')
            f.setnchannels(1)
            f.setsampwidth(sample.sample_width)
            f.setframerate(sample.sample_rate)
            f.setnframes(len(sample.wave))
            f.setcomptype('NONE', 'NONE')

            data = b.to_bytes(sample.wave, sample.sample_width, little_endian=True)
            f.writeframes(data)
            f.close()

        except:
            raise ValueError(
                'WavReader.__init__: File {} could not be read properly as a Wave file.'.format(self.filename))

    def get_sample(self):
        if not hasattr(self, 'wave'):
            self.read()
        return Sample(deepcopy(self.wave), self.sample_rate, self.sample_width)
