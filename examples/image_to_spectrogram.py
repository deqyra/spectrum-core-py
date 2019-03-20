from PIL import Image

from core.windows.hann import HannWindow
from core.io.wav_writer import WavWriter
from core.dsp_toolbox import DSPToolbox as DSP
from plot.audio_plotter import AudioPlotter as AP
from core.spectrogram_image import SpectrogramImage

from examples.example import Example

filename = '../assets/exode_spectrogram_fft512.png'
folder = 'output/wave_restoration'

metadata = {
    'sampling_frequency': 44100,
    'window_type': HannWindow,
    'reference_level': 1 << 15
}

class SpectrogramToImageExample(Example):
    @staticmethod
    def run():
        i = Image.open(filename)
        im = SpectrogramImage(i, metadata)
        spectro = DSP.spectrogram_from_image(im)
        AP.plot_spectrogram(spectro, save_image=True, filename='{}/restored_spectrogram.png'.format(folder))

        sample = DSP.sample_from_spectrogram(spectro)
        writer = WavWriter('{}/exode_restored.wav'.format(folder))
        writer.write(sample)

if __name__ == '__main__':
    SpectrogramToImageExample.run()