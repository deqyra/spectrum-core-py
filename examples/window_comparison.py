from examples.example import Example

from core.io.wav_reader import WavReader
from core.dsp_toolbox import DSPToolbox as DSP

from core.windows.uniform import UniformWindow
from core.windows.hann import HannWindow
from core.windows.hamming import HammingWindow
from core.windows.exact_blackman import ExactBlackmanWindow
from core.windows.blackman_harris import BlackmanHarrisWindow
from core.windows.flat_top import FlatTopWindow

from plot.audio_plotter import AudioPlotter as AP

folder = 'examples/output/window_comparison'
filename = 'assets/sine220.wav'

class WindowComparisonExample(Example):
    @staticmethod
    def run():
        reader = WavReader(filename)
        s = reader.get_sample()

        s = DSP.normalise(s)
        AP.plot_wave(s, title='220Hz sine wave', save_image=True, filename='{}/sine220_wave.png'.format(folder))

        window_classes = [
            UniformWindow,
            HannWindow,
            HammingWindow,
            ExactBlackmanWindow,
            BlackmanHarrisWindow,
            FlatTopWindow
        ]

        for window_class in window_classes:
            win = window_class()
            fft = DSP.fft(s, win)
            AP.plot_spectrum(fft, show_constant=-80, save_image=True,
                             title='220Hz sine spectrum ({} window)'.format(win.name),
                             filename='{}/sine220_{}_spectrum.png'.format(folder, win.name))

if __name__ == '__main__':
    WindowComparisonExample.run()