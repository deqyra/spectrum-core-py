class Spectrogram:
    def __init__(self, fft_slices, fft_size, overlap):
        self.fft_slices = fft_slices
        self.fft_size = fft_size
        self.overlap = overlap
        self.sample_span = fft_size + ((len(fft_slices) - 1) * (fft_size - overlap))