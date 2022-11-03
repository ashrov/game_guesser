import socket

import config_network


class Client:

    def __init__(self):
        self.client = socket.socket()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(config_network.SERVER_ADDR)
        message = self.client.recv(4096).decode('utf-8')
        print(message)


client = Client()
