from core import default

class Spectrogram:
    _default_metadata = {
        'sampling_frequency': default.SAMPLING_FREQUENCY,
        'window_type': default.WindowClass
    }

    def __init__(self, fft_slices, fft_size, metadata=None):
        """
        Represents a spectrogram.

        Args:
            fft_slices (:obj:`list` of :obj:`FFTResult`): Overlapping FFT slices
            fft_size: used FFT size
            metadata: various info.
        """

        self.fft_slices = fft_slices
        self.fft_size = fft_size
        self.overlap = fft_size / 2
        self.sample_span = fft_size + ((len(fft_slices) - 1) * (fft_size / 2))

        self.metadata = metadata
        if not isinstance(metadata, dict):
            self.metadata = {}

        # Merge default metadata keys if not present in passed dictionary
        for k, v in self._default_metadata:
            if k not in self.metadata:
                self.metadata[k] = v
