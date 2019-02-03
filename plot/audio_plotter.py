from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from core.sample import Sample
from core.dsp_toolbox import DSPToolbox as DSP
from core.fft_result import FFTResult

from plot.audio_hz_scale import AudioHzScale

class AudioPlotter:
    """
    Provides static methods to plot all kinds of audio-related stuff.
    """
    @staticmethod
    def plot_wave(sample, title='', save_image=False, filename=''):
        """
        Plots the waveform of a given sample.

        Args:
            sample (Sample): sample whose waveform is to plot
            title (str): title of the plot
            save_image (bool): whether to write the plot to the disk as an image
            filename (str): filename to save the plot image to if saving
        """
        x = np.arange(len(sample.wave)) / sample.sample_rate
        y = np.asarray(sample.wave) / (1 << (sample.bit_depth - 1))
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
        """
        Plots the spectrum corresponding to input FF data.
        Args:
            fft (FFTResult): the FFT data whose spectrum is to plot
            fill (bool): whether to fill with a color underneath the spectrum (looks awkward if False)
            show_constant (int): if not None, draws a red horizontal line at a certain level on the plot
            title (str): title of the plot
            save_image (bool): whether to write the plot to the disk as an image
            filename (str): filename to save the plot image to if saving
        """
        dbs = DSP.to_db(fft.amp_spectrum, fft.reference_level)
        plt.plot(fft.frequency_bins, dbs, lw=0.25)
        min_value = dbs.min()

        if fill:
            dbs[0] = min_value
            dbs[-1] = min_value
            plt.fill(fft.frequency_bins, dbs)

        if show_constant is not None:
            plt.plot(fft.frequency_bins, np.full(fft.frequency_bins.shape[0], show_constant))

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

