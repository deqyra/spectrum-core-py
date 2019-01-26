from core.sample import Sample
from core.wave_tools import WaveTools as WT

filename = 'assets/sine220.wav'

if __name__ == '__main__':
    s = Sample(filename)
    s.wave = WT.normalise(s.wave, 1 << (s.bit_depth - 1))
    WT.plot_wave(s, title='220Hz sine wave', save_image=False,filename='sine220_wave.png')
