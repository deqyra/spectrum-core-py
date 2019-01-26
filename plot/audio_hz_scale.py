from matplotlib import scale, transforms
from matplotlib.ticker import ScalarFormatter
import numpy as np

class AudioHzScale(scale.ScaleBase):
    name = 'audio_hz'
    _default_stops = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000]
    _log_params = {
        'h_shift': 0,
        'v_shift': 0,
        'h_scale': 1,
        'v_scale': 1
    }

    def __init__(self, axis, **kwargs):
        super(AudioHzScale, self).__init__()
        self.stops = AudioHzScale._default_stops
        if 'stops' in kwargs:
            self.stops = kwargs['stops']

    def get_transform(self):
        return self.AudioTransform(self.stops)

    def set_default_locators_and_formatters(self, axis):
        axis.set_ticks(self.stops)
        axis.set_major_formatter(ScalarFormatter())
        axis.set_units('Hz')

    class AudioTransform(transforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, stops=None):
            super(AudioHzScale.AudioTransform, self).__init__()
            self.stops = stops
            if not self.stops:
                self.stops = AudioHzScale._default_stops

        def transform_non_affine(self, a):
            log_params = AudioHzScale._log_params

            b = a * log_params['h_scale']
            b = b + log_params['h_shift']
            b = np.where(b < 1, 1, b)
            b = np.log2(b)
            b = b * log_params['v_scale']
            b = b + log_params['v_shift']

            return b

        def inverted(self):
            return AudioHzScale.InvertedAudioTransform(self.stops)

    class InvertedAudioTransform(transforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self, stops=None):
            super(AudioHzScale.InvertedAudioTransform, self).__init__()
            self.stops = stops
            if not self.stops:
                self.stops = AudioHzScale._default_stops

        def transform_non_affine(self, a):
            log_params = AudioHzScale._log_params

            b = a - log_params['v_shift']
            b = b / log_params['v_scale']
            b = np.where(b < 0, 0, b)
            b = np.float_power(2, b)
            b = b - log_params['h_shift']
            b = b / log_params['h_scale']

            return b

        def inverted(self):
            return AudioHzScale.AudioTransform(self.stops)

scale_names = scale.get_scale_names()
if 'audio_hz' not in scale_names:
    scale.register_scale(AudioHzScale)
