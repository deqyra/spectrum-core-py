from copy import deepcopy
from os import urandom
from random import randint
from util.byte_tools import ByteTools as b

def test_periodic_strip():
    parameters = [
        (1, 1, 0),
        (1, 2, 0),
        (1, 2, 1),
        (4, 8, 2),
        (1, 16, 15)
    ]
    for params in parameters:
        arr = bytearray(urandom(256))
        length, period, offset = params
        stripped = b.periodic_strip(arr, length, period, offset)

        current_offset = 0
        periods = 0
        count = 0
        for e in arr:
            if current_offset == period:
                current_offset = 0
                periods += 1

            if current_offset < offset:
                current_offset += 1
                continue

            if current_offset >= length + offset:
                current_offset += 1
                continue

            assert e == stripped[count]
            current_offset += 1
            count += 1

def test_bytes_to_int():
    parameters = [
        (1, False, None),
        (2, False, None),
        (4, False, None),
        (1, True, None),
        (2, True, None),
        (4, True, None)
    ]
    # Not testing padding because the underlying function is part of another test.

    for params in parameters:
        byte_length, little_endian, padding_number = params
        arr = []
        byte_arr = bytearray()
        endianness = 'little' if little_endian else 'big'

        bit_depth = 8 * byte_length
        max_val = 2 ** (bit_depth - 1) - 1
        min_val = - (2 ** (bit_depth - 1))

        for i in range(256):
            n = randint(min_val, max_val)
            arr.append(n)
            try:
                byte_arr.extend(n.to_bytes(byte_length, endianness, signed=True))
            except OverflowError:
                print('Overflow error for value {} (min: {}; max: {}; bytes: {})'.format(n, min_val, max_val, byte_length))

        assert b.to_int(byte_arr, byte_length, little_endian, padding_number) == arr

def test_reverse_byte_order():
    for i in range(4):
        array = urandom(256)
        reverse = b.reverse_byte_order(array)
        assert array == b.reverse_byte_order(reverse)

def test_is_power2():
    powers = [0,       1,       2,       4,        8,        16,       32,        64,        128,       256,    512,
              1024,    2048,    4096,    8192,     16384,    32768,    65536,     131072,    262144,    524288, 1048576,
              2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912 ]

    computed = []
    for i in powers:
        for j in range(max(0, i - 100), i + 100):
            if b.is_power2(j) and j not in computed:
                computed.append(j)

    assert powers == computed

def test_nearest_power2():
    powers = [0,       1,       2,       4,        8,        16,       32,        64,        128,       256,    512,
              1024,    2048,    4096,    8192,     16384,    32768,    65536,     131072,    262144,    524288, 1048576,
              2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912 ]

    assert b.nearest_power2(0) == 0
    assert b.nearest_power2(0, upper=True) == 0
    assert b.nearest_power2(0, lower=True) == 0

    assert b.nearest_power2(1) == 1
    assert b.nearest_power2(1, upper=True) == 1
    assert b.nearest_power2(1, lower=True) == 1

    assert b.nearest_power2(2) == 2
    assert b.nearest_power2(2, upper=True) == 2
    assert b.nearest_power2(2, lower=True) == 2

    for i, p in enumerate(powers):
        assert b.nearest_power2(p) == p
        if p - 1 > 2:
            assert b.nearest_power2(p - 1) == p
            assert b.nearest_power2(p - 1, upper=True) == p
            assert b.nearest_power2(p - 1, lower=True) == powers[i - 1]

        if p + 1 >= 4:
            assert b.nearest_power2(p + 1) == p
            assert b.nearest_power2(p + 1, lower=True) == p
            if i + 1 < len(powers):
                assert b.nearest_power2(p + 1, upper=True) == powers[i + 1]

def test_power2_pad():
    for i in range(256):
        pad_number = randint(-128, 127)
        length = randint(2, 1000)
        arr = []
        for j in range(length):
            arr.append(randint(-128, 127))

        padded = deepcopy(arr)
        padded = b.power2_pad(padded, pad_number)

        pad_length = b.nearest_power2(length, upper=True) - length
        arr.extend([pad_number] * pad_length)

        assert arr == padded
