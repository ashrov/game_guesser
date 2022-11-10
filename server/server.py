import socket

from guesser import Guesser
import config_network


class Server:
    def __init__(self):
        self.guesser = Guesser()
        self.clients = []
        self.server = socket.socket()
        self.server.bind(config_network.SERVER_ADDR)
        print("listening")
        while True:
            self.server.listen(1)
            self.accept_clients()

    def accept_clients(self):
        conn, addr = self.server.accept()
        self.clients.append(conn)
        self.listen_clients(conn)

    def listen_clients(self, conn):
        message = conn.recv(4096).decode('utf-8')

        self.handle_message(message)
        conn.close()

    def handle_message(self, mes: str):
        match mes:
            case "answer_yes":
                raise NotImplemented
            case "answer_no":
                raise NotImplemented
            case "start":
                raise NotImplemented
            case "get_current_games":
                raise NotImplemented

    def close(self):
        self.guesser.close()
