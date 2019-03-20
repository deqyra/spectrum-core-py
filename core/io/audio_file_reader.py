class AudioFileReader:
    def read(self):
        raise NotImplementedError('AudioFileReader.read: abstract method was called. Do all inherited file readers override read() properly?')

    def get_sample(self):
        raise NotImplementedError('AudioFileReader.get_sample: abstract method was called. Do all inherited file readers override get_sample() properly?')