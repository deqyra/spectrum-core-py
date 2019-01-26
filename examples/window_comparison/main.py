from core.sample import Sample
from core.wave_tools import WaveTools as WT

from core.windows.uniform import UniformWindow
from core.windows.hann import HannWindow
from core.windows.hamming import HammingWindow
from core.windows.exact_blackman import ExactBlackmanWindow
from core.windows.blackman_harris import BlackmanHarrisWindow
from core.windows.flat_top import FlatTopWindow

filename = 'assets/sine220.wav'

if __name__ == '__main__':
    s = Sample(filename)
    s.wave = WT.normalise(s.wave, 1 << (s.bit_depth - 1))
    WT.plot_wave(s, title='220Hz sine wave', save_image=False,filename='sine220_wave.png')

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
        fft = WT.fft(s, win)
        WT.plot_spectrum(fft, title='220Hz sine spectrum ({} window)'.format(win.name), show_constant=-80,
                         save_image=False, filename='sine220_{}_spectrum.png'.format(win.name))
