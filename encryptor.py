from proxy.utils.encode import encrypt


if __name__ == "__main__":
    print("彩虹島物語封包加密工具")
    try:
        while True:
            decrypted_data = input("[input]:   ")
            try:
                encrypted_data = encrypt(bytes.fromhex(decrypted_data))
            except ValueError:
                continue
            else:
                print("[output]: ", encrypted_data.hex(" ").upper())
    except KeyboardInterrupt:
        print("\n感謝使用")
