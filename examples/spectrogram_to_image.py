from core.windows.hann import HannWindow
from core.io.wav_reader import WavReader
from core.dsp_toolbox import DSPToolbox as DSP
from plot.audio_plotter import AudioPlotter as AP

from examples.example import Example

filename = '../assets/exode.wav'
folder = 'output/spectrogram_generation'

class SpectrogramToImageExample(Example):
    @staticmethod
    def run():
        reader = WavReader(filename)
        sample = reader.get_sample()
        window = HannWindow()
        spectro = DSP.spectrogram_from_sample(sample, window, size=1024, overlap=768)
        im = DSP.image_from_spectrogram(spectro)
        im.save('{}/exode_spectrogram.png'.format(folder))
        # AP.plot_spectrogram(spectro)

if __name__ == '__main__':
    SpectrogramToImageExample.run()