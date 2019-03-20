from PIL import Image

from core import default

class SpectrogramImage:
    _default_metadata = {
        'sampling_frequency': default.SAMPLING_FREQUENCY,
        'window_type': default.WindowClass,
        'reference_level': default.REFERENCE_LEVEL
    }

    def __init__(self, image, metadata):
        self.i = image

        self.metadata = metadata
        if not isinstance(metadata, dict):
            self.metadata = {}

        # Merge default metadata keys if not present in passed dictionary
        for k, v in self._default_metadata.items():
            if k not in self.metadata:
                self.metadata[k] = v
