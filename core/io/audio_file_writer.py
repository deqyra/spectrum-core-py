class AudioFileWriter:
    def __init__(self):
        pass

    def write(self, sample):
        raise NotImplementedError('AudioFileWriter.writ: abstract method was called. Do all inherited file writers override write properly?')
