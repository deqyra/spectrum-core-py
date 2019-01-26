import math
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, fftfreq

from core.window import Window
from plot.audio_hz_scale import AudioHzScale

class WaveTools:
    """
    Class to wrap an audio signal, providing a collection of tools to perform different operations on it.
    """
    def __spectrum_to_grey(self, slice):
        pass

    @staticmethod
    def spectrogram(sample, window_size):
        i = 0

        spectrum_slices = []
        while i < len(sample.wave):
            lower = i
            upper = i + window_size
            if upper > len(sample.wave):
                upper = len(sample.wave)

            slice = sample.slice(lower, upper)
            slice_fft = WaveTools.fft(slice)

            spectrum_slices.append(...)
            i += upper

        gray_slices = [sample.__slice_to_gray(slice) for slice in spectrum_slices]
        # TODO: generate pixel shades depending on amps along bins

    @staticmethod
    def amplitude_axes(sample):
        wave_x = np.arange(len(sample.wave)) / sample.sample_rate
        wave_y = np.asarray(sample.wave) / (1 << (sample.bit_depth - 1))

        return wave_x, wave_y

    @staticmethod
    def fft(sample, window, phase=False, rms=False, pow=False):
        # This is to cut the second half of the spectrum (aliases above the Nyquist freq or negative freqs)
        # This is half the length of the input wave since the length of numpy's fft happens to be exactly that.
        max_index = int(math.ceil(len(sample.wave) / 2))
        max_value = 1 << (sample.bit_depth - 1)

        # Compute frequency bins with spacing according to the sampling rate (in most cases 44.1kHz)
        fft_bins = fftfreq(len(sample.wave), 1.0 / sample.sample_rate)
        fft_bins = fft_bins[:max_index]
        # Shortcuts for later
        nyquist = sample.sample_rate / 2
        bin_spac = sample.sample_rate / len(sample.wave)
        max_freq = nyquist - bin_spac

        if not isinstance(window, Window):
            raise TypeError('WaveTools.fft_axes: passed window is not a valid window.')

        # Window the sample
        wave = window.process(sample.wave) / window.coherent_gain

        # Compute frequency coefficients
        fft_y = fft(wave)
        # Cut off half of the spectrum
        fft_y = fft_y[:max_index]

        # Separate amp and phase info, scale amp values
        fft_amp = np.abs(fft_y)

        fft_phase = None
        if phase:
            fft_phase = np.angle(fft_y)

        # First, scale the FFT output (relative to the sample count in the input wave)
        fft_amp /= len(wave)
        # Multiply freq amps by 2: we cut off half of the spectrum and we want to preserve the overall energy
        # We multiply by 2 everywhere because the spectrum is symmetrical around 0
        fft_amp = 2 * fft_amp
        # The 0-frequency however does not appear twice in the original spectrum so we restore it to half its new value
        # The DC offset should be 0 so there would theoretically be no need for that, but we do it just to make sure
        fft_amp[0] /= 2

        fft_rms = None
        fft_pow = None
        # The RMS amplitude spectrum can be useful for certain computations
        if rms or pow:
            fft_rms = fft_amp * np.sqrt(2)
            fft_rms[0] /= np.sqrt(2)
            # The power spectrum too
            if pow:
                fft_pow = np.square(fft_rms)

        return {
            'bins': fft_bins,
            'bin_spacing': bin_spac,
            'nyquist': nyquist,
            'max_freq': max_freq,
            'amp': fft_amp,
            'phase': fft_phase,
            'rms':fft_rms,
            'pow': fft_pow,
            'ref': max_value,
            'window': window.name
        }

    @staticmethod
    def to_db(levels, reference, square=True):
        factor = 20
        if not square:
            factor = 10

        if isinstance(levels, list):
            return list(map(lambda x: factor * np.log10(x / reference), levels))

        return factor * np.log10(levels / reference)

    @staticmethod
    def to_level(dbs, reference, unsquare=True):
        divisor = 20
        if not unsquare:
            divisor = 10

        if isinstance(dbs, list):
            return list(map(lambda x: (10 ** (x / divisor)) / reference, dbs))

        return (10 ** (dbs / divisor)) / reference

    @staticmethod
    def to_deg(radians):
        if isinstance(radians, list):
            return list(map(lambda x: x * 180 / np.pi, radians))

        return radians * 180 / np.pi

    @staticmethod
    def to_rad(degrees):
        if isinstance(degrees, list):
            return list(map(lambda x: x * np.pi / 180, degrees))

        return degrees * np.pi / 180

    @staticmethod
    def plot_wave(sample, title='', save_image=False, filename=''):
        x, y = WaveTools.amplitude_axes(sample)
        plt.plot(x, y)

        axes = plt.gca()
        axes.set_xlim([0, x[-1]])
        axes.set_ylim([-1, 1])

        plt.title(title)
        plt.show()

        if save_image:
            file = filename or 'wave_{}.png'.format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
            plt.savefig(file)

    @staticmethod
    def plot_spectrum(fft_values, title='', fill=True, show_constant=None, save_image=False, filename=''):
        # TODO: logarithmic x scale
        # TODO: add title

        dbs = WaveTools.to_db(fft_values['amp'], fft_values['ref'])
        plt.plot(fft_values['bins'], dbs, lw=0.25)
        min_value = dbs.min()

        if fill:
            dbs[0] = min_value
            dbs[-1] = min_value
            plt.fill(fft_values['bins'], dbs)

        if show_constant is not None:
            plt.plot(fft_values['bins'], np.full(fft_values['bins'].shape[0], show_constant))

        axes = plt.gca()
        axes.set_xscale('audio_hz')
        axes.set_xlim([20, 20000])
        axes.set_ylim([min_value, 0])

        plt.title(title)
        plt.show()

        if save_image:
            file = filename or 'spectrum_{}.png'.format(datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
            plt.savefig(file)

    @staticmethod
    def normalise(wave, max_value):
        wave_min = min(wave)
        wave_max = max(wave)
        max_amp = max(abs(wave_min), abs(wave_max))
        factor = max_value / max_amp
        if factor != 1.:
            return list(map(lambda x: int(round(x * factor)), wave))
