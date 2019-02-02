import math
from copy import deepcopy
import numpy as np
from numpy.fft import fft, fftfreq

from core.sample import Sample
from core.window import Window

class DSPToolbox:
    """
    Class to wrap an audio signal, providing a collection of tools to perform different operations on it.
    """
    @staticmethod
    def normalise(sample):
        wave_min = min(sample.wave)
        wave_max = max(sample.wave)
        max_value = 1 << (sample.sample_width * 8) - 1

        max_amp = max(abs(wave_min), abs(wave_max))
        factor = max_value / max_amp

        new_wave = deepcopy(sample.wave)
        new_wave = new_wave * factor

        return Sample(new_wave, sample.sample_rate, sample.sample_width)

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
            raise TypeError('DSPToolbox.fft: passed window is not a valid window.')

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