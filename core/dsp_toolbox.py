import math
from copy import deepcopy
import numpy as np
from numpy.fft import fft, fftfreq, ifft
from PIL import Image

from core import default
from core.sample import Sample
from core.window import Window
from core.fft_result import FFTResult
from core.spectrogram import Spectrogram
from core.spectrogram_image import SpectrogramImage
from util.byte_tools import ByteTools as b

class DSPToolbox:
    """
    Class to wrap an audio signal, providing a collection of tools to perform different operations on it.
    """
    @staticmethod
    def normalise(sample):
        """
        Returns a normalised copy of the input sample.
        Args:
            sample (Sample): the sample to copy and normalise

        Returns:
            (Sample): a normalised copy of the input sample
        """
        wave_min = min(sample.wave)
        wave_max = max(sample.wave)
        max_value = 1 << (sample.bit_depth) - 1

        max_amp = max(abs(wave_min), abs(wave_max))
        factor = max_value / max_amp

        new_wave = deepcopy(sample.wave)
        new_wave = new_wave * factor

        return Sample(new_wave, sample.sample_rate, sample.sample_width)

    @staticmethod
    def spectrogram_from_sample(sample, window=None, size=default.SPECTROGRAM_SIZE):
        """
        Generates the spectrogram for the input sample.

        Args:
            sample (Sample): the input sample whose spectrogram to generate.
            window (Window): the window with which to process the sample.
            _size (int): the size of slices to extract from the sample.
            overlap (int): the number of samples by which slices should overlap.
            spp (int): samples per pixel - number of samples to consider for the value of one pixel.

        Returns:
            Generated spectrogram.
        """

        # Instantiate a default window if none provided
        if not window:
            window = default.WindowClass()

        overlap = size / 2

        length = len(sample.wave)
        _size = 2 * size

        slices = []
        i = 0
        while i < length:
            upper = min(i + _size, length)
            slices.append(sample.slice(i, upper))
            i += (_size - overlap)

        fft_slices = []
        for s in slices:
            fft_slices.append(DSPToolbox.fft(s, window))

        metadata = {
            'sampling_frequency': sample.sample_rate,
            'window_type': type(window)
        }

        return Spectrogram(fft_slices, size, metadata)

    @staticmethod
    def sample_from_spectrogram(spectrogram):
        """
        Restores a sample from the input spectrogram

        Args:
            spectrogram (Spectrogram): the input spectrogram

        Returns:
            Sample: the restored sample
        """

        overlap = spectrogram.overlap
        wave = []
        for i, slice in enumerate(spectrogram.fft_slices):
            # Restore spectrum info in the same format as it came out of numpy
            amp_array = slice.amp_spectrum / 2
            amp_array[0] *= 2

            sample_count = 2 * len(amp_array)
            amp_array *= sample_count

            # Append 0-axis symmetrical image of amp spectrum (frequency aliases)
            amp_array = amp_array.append(list(reversed(amp_array)))
            # Remove duplicate 0-frequency
            amp_array = amp_array[:-1]

            # Restore phase spectrum
            phase_array = slice.phase_spectrum
            # Get 0-axis symmetrical image of phase spectrum
            reversed_phase_array = list(reversed(phase_array))
            # Remove duplicate 0-phase
            reversed_phase_array = np.array(reversed_phase_array[:-1])
            # Multiply by -1 to get symmetry around 0
            reversed_phase_array = reversed_phase_array * (-1)
            # Append to phase spectrum
            phase_array = phase_array.append(reversed_phase_array)

            complex_array = 1j * phase_array
            complex_array += amp_array
            wave_slice = ifft(complex_array)
            wave = wave[:-overlap].append(np.abs(wave_slice).tolist())

        reference_level = spectrogram.fft_slices[0].reference_level
        sample_width = ((int(reference_level).bit_length() - 1) // 8) + 1
        return Sample(wave, spectrogram.metadata['sampling_rate'], sample_width)

    @staticmethod
    def image_from_spectrogram(spectrogram):
        w, h = len(spectrogram.fft_slices), spectrogram.fft_size
        im = Image.new('L', (w, h))
        for i, slice in enumerate(spectrogram.fft_slices):
            for j, amp in enumerate(slice.amp_spectrum):
                val = int((amp / slice.reference_level) * 255)
                im.putpixel((i, h - j - 1), val)

        metadata = spectrogram.metadata
        metadata['reference_level'] = spectrogram.fft_slices[0].reference_level
        return SpectrogramImage(im, metadata)

    @staticmethod
    def spectrogram_from_image(image):
        """
        Generates a spectrogram from an image.

        Args:
            image (SpectrogramImage): input image.
            reference_level (int): maximum sample value.

        Returns:
            Spectrogram: output spectrogram.
        """
        im = image.i
        meta = image.metadata

        reference_level = meta['reference_level']
        sample_rate = meta['sampling_frequency']
        nyquist = sample_rate / 2

        n_slices, fft_size = im.size
        fft_slices = []
        for i in range(n_slices):
            slice_values = []
            for j in range(fft_size):
                val = im.getpixel((i, fft_size - j - 1))
                level = (float(val) / 255) * reference_level
                slice_values.append(level)
            fft_amp = np.array(slice_values)

            # Restore further information from restored fft
            fft_rms = fft_amp * np.sqrt(2)
            fft_rms[0] /= np.sqrt(2)
            fft_pow = np.square(fft_rms)
            sample_count = len(fft_amp) * 2
            fft_bins = fftfreq(sample_count, 1.0 / sample_rate)
            bin_spac = sample_rate / sample_count
            max_freq = nyquist - bin_spac

            # TODO: restore phase properly
            fft_phase = np.array([0] * len(fft_amp))

            fft_dict = {
                'frequency_bins': fft_bins,
                'bin_spacing': bin_spac,
                'nyquist_frequency': nyquist,
                'max_frequency': max_freq,
                'amp_spectrum': fft_amp,
                'phase_spectrum': fft_phase,
                'rms_spectrum':fft_rms,
                'power_spectrum': fft_pow,
                'reference_level': reference_level,
                'window_type': meta['window_type'],
                'metadata': {
                    'sampling_frequency': sample_rate
                }
            }

            # Create slice and append it to array of slices
            fft_slices.append(FFTResult(**fft_dict))

        metadata = {
            'sampling_frequency': sample_rate,
            'window_type': meta['window_type']
        }
        return Spectrogram(fft_slices, fft_size, metadata)

    @staticmethod
    def fft(sample, window=None):
        # Instantiate a default window if none provided
        if not window:
            window = default.WindowClass()

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

        fft_phase = np.angle(fft_y)

        # First, scale the FFT output (relative to the sample count in the input wave)
        fft_amp /= len(wave)
        # Multiply freq amps by 2: we cut off half of the spectrum and we want to preserve the overall energy
        # We multiply by 2 everywhere because the spectrum is symmetrical around 0
        fft_amp = 2 * fft_amp
        # The 0-frequency however does not appear twice in the original spectrum so we restore it to half its new value
        # The DC offset should be 0 so there would theoretically be no need for that, but we do it just to make sure
        fft_amp[0] /= 2

        # The RMS amplitude spectrum can be useful for certain computations
        fft_rms = fft_amp * np.sqrt(2)
        fft_rms[0] /= np.sqrt(2)
        # The power spectrum too
        fft_pow = np.square(fft_rms)

        fft_dict = {
            'frequency_bins': fft_bins,
            'bin_spacing': bin_spac,
            'nyquist_frequency': nyquist,
            'max_frequency': max_freq,
            'amp_spectrum': fft_amp,
            'phase_spectrum': fft_phase,
            'rms_spectrum':fft_rms,
            'power_spectrum': fft_pow,
            'reference_level': max_value,
            'window_type': type(window),
            'metadata': {
                'sampling_frequency': sample.sample_rate
            }
        }
        return FFTResult(**fft_dict)

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
