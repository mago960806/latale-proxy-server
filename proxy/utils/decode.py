KEYS = [0x66, 0x61, 0x6B, 0x74, 0x6E, 0x70, 0x67, 0x6A, 0x73, 0x71, 0x6D]


def decrypt(data: bytes, key: int = 0x00) -> str:
    data = bytearray(data)
    # 解密头部信息
    header = data[:6]
    for i in range(len(header)):
        header[i] = header[i] ^ key
    # 解密正文信息
    content = data[6:]
    for i in range(len(content)):
        if content[i] == key:
            content[i] = content[i] ^ key
        else:
            content[i] = content[i] ^ KEYS[i % len(KEYS)]
    data = header + content
    return data.hex(" ").upper()
