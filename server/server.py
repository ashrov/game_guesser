import socket

from guesser import Guesser
import config_network


class Server:
    def __init__(self):
        self.guesser = Guesser()
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
        answer = self.guesser.guess_game(tags_message)
        conn.send(answer.to_socket_message())

    def close(self):
        self.guesser.close()
