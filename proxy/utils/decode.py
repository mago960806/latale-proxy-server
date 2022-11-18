KEYS = [0x71, 0x6D, 0x66, 0x61, 0x6B, 0x74, 0x6E, 0x70, 0x67, 0x6A, 0x73]
KEY_LENGTH = 11


def decrypt(data: bytes) -> bytes:
    data = bytearray(data)

    for i in range(4, len(data)):
        if data[i] == 0x00:
            continue
        data[i] = data[i] ^ KEYS[(i - 4) % KEY_LENGTH]
    return data
