class Example:
    """
    Base class for examples to inherit and make it easier for test
    """
    @staticmethod
    def run():
        raise NotImplementedError('Example.run was called. Is an inherited Example overriding it correctly?')