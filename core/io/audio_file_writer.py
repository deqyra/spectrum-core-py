class AudioFileWriter:
    def __init__(self, filename):
        raise NotImplementedError('AudioFileWriter.__init__: abstract method was called. Do all inherited file readers override __init__ properly?')

    def write(self, sample):
        raise NotImplementedError('AudioFileWriter.writ: abstract method was called. Do all inherited file writers override write properly?')
