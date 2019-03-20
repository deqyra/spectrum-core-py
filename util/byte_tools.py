from copy import deepcopy

class ByteTools:
    """
    Static class which offers functionality to manipulate byte objects as well as carry out general purpose
    binary-related operations.
    """

    @staticmethod
    def periodic_strip(array, length, period, offset=0):
        """
        Periodically strips byte-strings from bytearray obj.
        Returned object type is according to what is fed into the function in the first place.

        Args:
            array (bytes-like): a bytes or bytearray object to strip bytes from.
            length (int): how many bytes to strip at every new period.
            period (int): length of the period which the stripping will be triggered upon.
            offset (int): how many bytes to ignore at the beginning of a new period.

        Returns:
            bytes-like: object containing all stripped bytes.
        """
        o_type = type(array)
        if not (o_type is bytes or o_type is bytearray):
            raise TypeError('periodic_strip: Type of `array` must be either `bytes` or `bytearray`.')

        if length + offset > period:
            raise ValueError('periodic_strip: `length` ({}) and `offset` ({}) together cannot be greater than `period` ({}).'.format(length, offset, period))
        if length == 0:
            return bytearray()
        if length == period:
            return bytearray(array)

        res = bytearray()

        i = 0
        while i < len(array):
            i += offset
            if i >= len(array):
                break
            upper_bound = i + length
            upper_bound = min(upper_bound, len(array))
            res.extend(array[i:upper_bound])
            i += period - offset

        if o_type is bytes:
            res = bytes(res)

        return res

    @staticmethod
    def to_int(array, byte_length, little_endian=False, padding_number=None):
        """
        Converts the given bytes or bytearray object to a list of integers.

        Args:
            array (bytes-like): the byte array from which to generate integers.
            byte_length (int): the length of a byte word to interpret as a single integer.
            little_endian (bool): whether to interpret byte words in big or little endian.
                Applies only to byte words longer than one byte.
            padding_number (int): if not None, pads the output with the specified number so its length is a power of 2.

        Returns:
            list of int: the same bytes converted to integers.
        """
        o_type = type(array)
        if not (o_type is bytes or o_type is bytearray):
            raise TypeError('to_int: Type of `array` must be either `bytes` or `bytearray`.')

        endian = 'big'
        if little_endian:
            endian = 'little'

        res = []
        i = 0
        while (i + byte_length) <= len(array):
            byte_string = array[i:i + byte_length]
            res.append(int.from_bytes(byte_string, byteorder=endian, signed=True))
            i += byte_length

        if padding_number is not None:
            res = ByteTools.power2_pad(res, padding_number)

        return res

    @staticmethod
    def to_bytearray(array, byte_width, little_endian=False):
        endian = 'big'
        if little_endian:
            endian = 'little'

        res = bytearray()
        for i in array:
            res += int(i).to_bytes(byte_width, endian, signed=True)

        return res

    @staticmethod
    def to_bytes(array, byte_width, little_endian=False):
        return bytes(ByteTools.to_bytearray(array, byte_width, little_endian))

    @staticmethod
    def reverse_byte_order(byte_string):
        """
        Reverses the order in which bytes appear in the input bytes-like.

        Args:
            byte_string (bytes-like): object to reverse.

        Returns:
            bytes-like: object with bytes in reverse order.
        """
        o_type = type(byte_string)
        if not (o_type is bytes or o_type is bytearray):
            raise TypeError('reverse_byte_order: Type of `array` must be either `bytes` or `bytearray`.')

        res = bytearray()
        for b in byte_string[::-1]:
            res.append(b)

        if o_type is bytes:
            res = bytes(res)

        return res

    @staticmethod
    def power2_pad(array, pad_number=0):
        """
        Pads the input list with a number so its length is a power of 2.
        Doesn't really fit in module `bytes_manip`.

        Args:
            array (iterable): list to pad
            pad_number (object): number to pad the array with.

        Returns (type(array)): the input list padded with pad_number so its length is a power of 2.
        """
        res = deepcopy(array)
        n_pad = ByteTools.nearest_power2(len(array), upper=True) - len(array)

        res.extend([pad_number] * n_pad)
        return res

    @staticmethod
    def is_power2(value):
        """
        Tells whether the input number is a power of 2.

        Args:
            value (int): the value to check.

        Returns:
            bool: whether or not value is a power of 2.
        """
        if value == 0:
            return True

        bits = value.bit_length()
        return value == (1 << (bits - 1))

    @staticmethod
    def nearest_power2(value, upper=False, lower=False):
        """
        Returns the power of 2 nearest to value.
        If value is exactly halfway between its upper and lower powers of 2, the upper one is returned.

        Args:
            value (int): the value whose nearest power of 2 to find.
            upper (bool): whether to return the smallest greater power of 2 instead of the nearest.
            lower (bool): whether to return the greatest lower power of 2 instead of the nearest.

        Returns:
            int: a power of 2.
        """
        if upper and lower:
            raise ValueError('nearest_power2: `upper` and `lower` cannot be used in conjunction.')

        if ByteTools.is_power2(value):
            return value

        lower_power = 1 << (value.bit_length() - 1)
        upper_power = 1 << value.bit_length()

        if upper:
            return upper_power

        if lower:
            return lower_power

        lower_diff = value - lower_power
        upper_diff = upper_power - value

        if lower_diff < upper_diff:
            return lower_power
        else:
            return upper_power
