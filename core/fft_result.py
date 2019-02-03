class FFTResult:
    """
    Dummy object essentially used for type checking purposes for now.
    May prove handy later on.
    """
    def __init__(self, frequency_bins, bin_spacing, nyquist_frequency, max_frequency, amp_spectrum,
                       phase_spectrum, rms_spectrum, power_spectrum, reference_level, window_type):
        self.frequency_bins = frequency_bins
        self.bin_spacing = bin_spacing
        self.nyquist_frequency = nyquist_frequency
        self.max_frequency = max_frequency
        self.amp_spectrum = amp_spectrum
        self.phase_spectrum = phase_spectrum
        self.rms_spectrum = rms_spectrum
        self.power_spectrum = power_spectrum
        self.reference_level = reference_level
        self.window_type = window_type