import socket

import guesser
import config_network


class Server:
    def __init__(self):
        self.clients = []
        self.server = socket.socket()
        self.server.bind(config_network.SERVER_ADDR)
        self.server.listen(1)
        self.accept_clients()

    def accept_clients(self):
        conn, addr = self.server.accept()
        self.clients.append(conn)
        self.listen_clients(conn)

    def listen_clients(self, conn):
        tags_message = conn.recv(4096).decode('utf-8')
        answer = guesser.guesser(tags_message)
        conn.send(str(answer).encode('utf-8'))


server = Server()
