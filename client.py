import socket
from proxy.db import DATABASE
import struct
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 2222))


def do_action(action_name: str, action_params: int = 0):
    action_id = DATABASE.get_action_id_by_name(action_name)
    if action_id is not None:
        data = struct.pack("<HHLQL", 20, 1, 200000500, action_id, action_params)
        print(data.hex(" ").upper())
        # client.sendall(data)


while True:
    # data = "15 00 01 00 0A C9 EB 0B 79 DC 10 00 00 01 00 01 FF FF FF FF 01"
    # data = "15 00 01 00 0A C9 EB 0B 4C 80 1B 00 00 00 00 01 FF FF FF FF 00"
    data = input()
    client.sendall(bytes.fromhex(data))
    time.sleep(0.5)


# 1C 00 01 00 D8 C5 EB 0B 10 00 00 00 01 01 00 00 00 00 00 01 9C 60 00 A4 00 00 00 00

# 14 00 01 00 88 C5 EB 0B 00 00 00 00 01 01 00 0D 00 00 00 10
# 14 00 01 00 88 C5 EB 0B 0D 00 00 00 10 01 00 00 00 00 00 01
# 14 00 01 00 88 C5 EB 0B 00 00 00 00 02 01 00 0D 00 00 00 12
