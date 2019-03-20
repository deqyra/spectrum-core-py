class AudioFileWriter:
    def write(self, filename):
        raise NotImplementedError('AudioFileWriter.write: abstract method was called. Do all inherited file writers override write() properly?')
