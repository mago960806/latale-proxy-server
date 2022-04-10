from proxy.utils import decrypt


if __name__ == "__main__":
    print("彩虹島物語封包解密工具")
    try:
        while True:
            encrypted_data = input("[input]:   ")
            try:
                decrypted_data = decrypt(bytes.fromhex(encrypted_data))
            except ValueError:
                continue
            else:
                print("[output]: ", decrypted_data.hex(" ").upper())
    except KeyboardInterrupt:
        print("\n感謝使用")
