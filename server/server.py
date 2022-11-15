import json
import socket
from threading import Thread

from config import GAME_SELECTION_SIZE
from utils import Tag, Game, User
from guesser import Guesser
import config_network


class ClientThread(Thread):
    def __init__(self, func):
        super().__init__(target=func)


class Server:
    _clients: dict[User]
    _clint_threads: list[ClientThread]

    def __init__(self):
        self.guesser = Guesser()
        self._clients = dict()
        self._clint_threads = []
        self.server = socket.socket()
        self.server.bind(config_network.SERVER_ADDR)
        print("listening")
        self.process_connections()

    def close(self):
        self.guesser.close()

    def process_connections(self):
        while True:
            self.server.listen(1)
            client_thread = ClientThread(self.accept_clients)
            self._clint_threads.append(client_thread)
            client_thread.start()

    def accept_clients(self):
        conn, addr = self.server.accept()
        user = User(conn)
        self._clients[addr] = user
        print(f"[+] starting thread for connection: {conn}")
        while True:
            self.listen_client(conn, user)

    def listen_client(self, conn, user: User):
        message = conn.recv(4096).decode('utf-8')
        response = self.handle_message(message, user)
        conn.send(response.encode('utf-8'))

    def handle_message(self, mes: str, user: User) -> str:
        """ :return: server answer (json dump string) """
        js = json.loads(mes)
        match js.get("intent", ""):
            case "answer_yes":
                response = self.answer_yes(user)
            case "answer_no":
                response = self.answer_no(user)
            case "start":
                response = self.get_next_tag(user)
            case "get_current_games":
                response = user.current_games
            case _:
                response = None

        return response.to_json()

    def get_next_tag(self, user: User) -> Tag:
        new_tag = self.guesser.get_new_tag(user.good_tags + user.bad_tags)
        user.current_tag = new_tag
        return new_tag

    def answer_yes(self, user: User) -> Tag:
        user.good_tags.append(user.current_tag)
        user.current_games = self.guesser.guess_game(user.good_tags, GAME_SELECTION_SIZE)
        return self.get_next_tag(user)

    def answer_no(self, user: User) -> Tag:
        user.bad_tags.append(user.current_tag)
        user.current_games = self.guesser.guess_game(user.good_tags, GAME_SELECTION_SIZE)
        return self.get_next_tag(user)


if __name__ == "__main__":
    server = Server()
