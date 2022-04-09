import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 2222))

while True:
    data = input("[input]: ")
    try:
        data = bytes.fromhex(data)
    except Exception:
        pass
    else:
        client.sendall(data)
