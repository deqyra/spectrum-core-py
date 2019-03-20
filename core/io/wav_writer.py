import wave

from core.io import AudioFileWriter
from util.byte_tools import ByteTools as b

class WavWriter(AudioFileWriter):
    def __init__(self, filename):
        super(WavWriter, self).__init__()

        if not filename:
            raise ValueError('WavReader.__init__: filename is needed.')
        self.filename = filename

    def write(self, sample):
        f = wave.open(self.filename, 'wb')
        f.setnchannels(1)
        f.setsampwidth(sample.sample_width)
        f.setframerate(sample.sample_rate)
        f.setnframes(len(sample.wave))
        f.setcomptype('NONE', 'not compressed')

        data = b.to_bytes(sample.wave, sample.sample_width, little_endian=True)
        f.writeframes(data)
        f.close()
