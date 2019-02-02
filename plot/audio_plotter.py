from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from core.dsp_toolbox import DSPToolbox as DSP
from plot.audio_hz_scale import AudioHzScale

class AudioPlotter:
    @staticmethod
    def __amplitude_axes(sample):
        wave_x = np.arange(len(sample.wave)) / sample.sample_rate
        wave_y = np.asarray(sample.wave) / (1 << (sample.bit_depth - 1))

        return wave_x, wave_y

    @staticmethod
    def plot_wave(sample, title='', save_image=False, filename=''):
        x, y = AudioPlotter.__amplitude_axes(sample)
        plt.plot(x, y)

        axes = plt.gca()
        axes.set_xlim([0, x[-1]])
        axes.set_ylim([-1, 1])

        plt.title(title)

        if matplotlib.get_backend() == 'agg':
            save_image = True
        else:
            plt.show()

        if save_image:
            file = filename or 'wave_{}.png'.format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
            plt.savefig(file)

    @staticmethod
    def plot_spectrum(fft, title='', fill=True, show_constant=None, save_image=False, filename=''):
        dbs = DSP.to_db(fft['amp'], fft['ref'])
        plt.plot(fft['bins'], dbs, lw=0.25)
        min_value = dbs.min()

        if fill:
            dbs[0] = min_value
            dbs[-1] = min_value
            plt.fill(fft['bins'], dbs)

        if show_constant is not None:
            plt.plot(fft['bins'], np.full(fft['bins'].shape[0], show_constant))

        axes = plt.gca()
        axes.set_xscale('audio_hz')
        axes.set_xlim([20, 20000])
        axes.set_ylim([min_value, 0])

        plt.title(title)

        if matplotlib.get_backend() == 'agg':
            save_image = True
        else:
            plt.show()

        if save_image:
            file = filename or 'spectrum_{}.png'.format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
            plt.savefig(file)

