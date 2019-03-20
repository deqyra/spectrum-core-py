from core.windows.hann import HannWindow
from core.io.wav_reader import WavReader
from core.dsp_toolbox import DSPToolbox as DSP
from plot.audio_plotter import AudioPlotter as AP

from examples.example import Example

filename = '../assets/exode.wav'
folder = 'output/spectrogram_generation'

sizes = [128, 256, 512, 1024, 2048, 4096, 8192]

class SpectrogramToImageExample(Example):
    @staticmethod
    def run():
        reader = WavReader(filename)
        sample = reader.get_sample()
        window = HannWindow()
        for size in sizes:
            spectro = DSP.spectrogram_from_sample(sample, window, size=size, overlap=(size // 2))
            im = DSP.image_from_spectrogram(spectro)
            im.save('{}/exode_spectrogram_fft{}.png'.format(folder, size))
        # AP.plot_spectrogram(spectro)

if __name__ == '__main__':
    SpectrogramToImageExample.run()