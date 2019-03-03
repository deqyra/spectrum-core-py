from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
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

    @staticmethod
    def plot_spectrogram(spectrogram):
        im = DSP.spectrogram_to_image(spectrogram)
        matrix = np.asarray(im)

        max_freq = spectrogram.fft_slices[0].max_frequency
        sampling_freq = spectrogram.fft_slices[0].metadata['sampling_frequency']
        sample_duration = 1 / sampling_freq
        spectrogram_duration = sample_duration * spectrogram.sample_span

        xticks, xlabels, yticks, ylabels = AudioPlotter._get_spectrogram_axis_info(spectrogram_duration, im.width, max_freq, im.height)

        plt.imshow(matrix, cmap='gray', vmin=0, vmax=255)
        plt.xticks(xticks, xlabels)
        plt.yticks(yticks, ylabels)
        plt.show()

    @staticmethod
    def plot_image(im):
        matrix = np.asarray(im)
        plt.imshow(matrix, cmap='gray', vmin=0, vmax=255)
        plt.show()

    @staticmethod
    def _get_spectrogram_axis_info(duration, width, max_freq, height):
        N_XTICKS = 6
        N_YTICKS = 6

        xtick_period = width / (N_XTICKS - 1)
        xticks = [int(i * xtick_period) for i in range(N_XTICKS)]
        xlabels = [int(i * (duration / (N_XTICKS - 1))) for i in range(N_XTICKS)]

        ytick_period = height / (N_YTICKS - 1)
        yticks = [int(i * ytick_period) for i in range(N_YTICKS)]
        ylabels = [int(i * (max_freq / (N_YTICKS - 1))) for i in reversed(range(N_YTICKS))]

        return xticks, xlabels, yticks, ylabels