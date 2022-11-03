import socket

import config_network


class Server:
    def __init__(self):
        self.clients = []
        self.server = socket.socket()
        self.server.bind(config_network.SERVER_ADDR)
        self.server.listen(1)
        print("server started")
        conn, addr = self.server.accept()
        self.clients.append(conn)
        print("accepted another client")
        conn.send("Hell no".encode('utf-8'))


server = Server()
