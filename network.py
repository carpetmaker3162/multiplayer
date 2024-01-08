import socket
from utils import get_local_ip, load_dict

# change if you want to use a server on a different address in your network
SERVER = get_local_ip()
PORT = 5555

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = SERVER
        self.port = PORT
        self.addr = (self.server, self.port)
        self.connect()
    
    # connect and receive initial data
    def connect(self):
        try:
            # NOTE: update this if ever re-fmt data sending
            self.client.connect(self.addr)
            initial_data = load_dict(self.client.recv(2048).decode())
            self.pos = initial_data["pos"]
            self.id = initial_data["id"]
        except socket.error as e:
            print("Error (Network.connect):", e)
    
    # send data to server and return the server's reply
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print("Error (Network.send):", e)
