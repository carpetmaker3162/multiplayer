import json
import socket
import threading
from utils import make_tuple, parse_tuple, get_available_id, load_dict, dump_dict, get_local_ip

SERVER = get_local_ip()
PORT = 5555 # change if 5555 is taken, in network.py too

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER, PORT))
s.listen()
print("Server started")

players = {}

def threaded_client(conn, player_id):
    # send initial data
    pos = players[player_id]["pos"]
    initial_data = {}
    initial_data["pos"] = make_tuple(pos)
    initial_data["id"] = player_id
    conn.send(str.encode(dump_dict(initial_data)))

    reply = ""
    while True:
        # receive data from user (new player state/pos), reply with all players state/pos
        data = conn.recv(2048).decode("utf-8")
        
        if not data:
            print(f"User {player_id} disconnected")
            players.pop(player_id)
            break
        else:
            # update pos
            player_data = json.loads(data)
            players[player_id]["pos"] = parse_tuple(player_data["pos"])

            # if need to hide other player positions, dont reply with info on all players
            reply = json.dumps(players)
        
        conn.sendall(str.encode(reply))
    
    conn.close()

while True:
    conn, addr = s.accept()

    player_id = get_available_id(players)
    players[player_id] = {"pos": (100, 100)} # NOTE: change if ever re-fmt data

    print(f"User {player_id} connected", addr)

    thread = threading.Thread(target=threaded_client, args=(conn, player_id))
    thread.start()
