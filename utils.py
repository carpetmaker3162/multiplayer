import json
import re
import socket

def parse_tuple(string):
    ints = map(int, string.split(","))
    return tuple(ints)

def make_tuple(tup: tuple[int]):
    return ",".join(map(str, tup))

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 1))
    ip = s.getsockname()[0]

    s.close()
    return ip

def get_available_id(players):
    i = 0
    sentinel = object()

    while players.get(i, sentinel) is not sentinel:
        i += 1

    return i

def dump_dict(data: dict):
    new_data = {}

    for key, value in data.items():
        if isinstance(value, tuple):
            new_data[key] = make_tuple(value)
        else:
            new_data[key] = value
    
    return json.dumps(new_data)

def load_dict(data: str):
    data = json.loads(data)
    new_data = {}

    for key, value in data.items():
        if key.isnumeric():
            key = int(key)

        if isinstance(value, str) and re.match(r"^[0-9]+(,[0-9]+)*$", value):
            tup = parse_tuple(value)

            if len(tup) == 1:
                value = tup[0]
            else:
                value = tup

            new_data[key] = value
        else:
            new_data[key] = value

    return new_data
