import json
import socket
from threading import Thread
import logging

from config import GAME_SELECTION_SIZE
from utils import Tag, User, CustomJSONEncoder
from guesser import Guesser
from client import config_network

logging.basicConfig(level=logging.INFO)


# JSON constants
INTENT = "intent"
NEW_TAG = "new_tag"
CURRENT_GAMES = "current_games"
SAME_GAMES = "same_games"
ERROR = "error"
GAMES_COUNT = "games_count"
ANSWER = "answer"
YES = "yes"
NO = "no"
DN = "dn"


class ClientThread:
    def __init__(self, sock: socket.socket, user: User):
        self.connection, self.address = user.connection, user.address
        self.guesser = Guesser()
        self.socket = sock
        self.user = user
        self.listen_client()

    def _close(self):
        self.guesser.close()

    def listen_client(self):
        logging.info(f"starting thread for {self.address}")
        while data := self.connection.recv(4096):
            message = data.decode('utf-8')
            response = self.handle_message(message)
            self.connection.send(response.encode('utf-8'))
        self._close()
        logging.info(f"Connection with {self.address} closed.")

    def handle_message(self, mes: str) -> str:
        """ :return: server answer (json dump string) """
        js = json.loads(mes)
        match js.get(INTENT, ""):
            case "answer":
                response = self.answer(js.get(ANSWER, ""))
            case "start":
                self.user.reset_tags()
                response = {NEW_TAG: self.get_next_tag()}
            case "get_current_games":
                response = {CURRENT_GAMES: self.user.current_games}
            case "get_same_games":
                response = {SAME_GAMES: self.guesser.guess_game(self.user, selection_size=GAME_SELECTION_SIZE)}
            case _:
                response = {ERROR: "bad intent"}

        return json.dumps(response, cls=CustomJSONEncoder)

    def get_next_tag(self) -> Tag:
        new_tag = self.guesser.get_new_tag(self.user)
        self.user.current_tag = new_tag
        return new_tag

    def answer(self, result: str) -> dict:
        match result:
            case "yes":
                self.user.add_good_tag(self.user.current_tag)
            case "no":
                self.user.add_bad_tag(self.user.current_tag)
            case "dn":
                self.user.used_tags.append(self.user.current_tag)
            case _:
                return {ERROR: "bad answer result"}

        self.user.current_games = self.guesser.guess_game(self.user)
        data = {NEW_TAG: self.get_next_tag(),
                GAMES_COUNT: len(self.user.current_games)}
        return data


class MainServer:
    _clients: dict[User]
    _clint_threads: list[Thread]

    def __init__(self):
        self._clients = dict()
        self._clint_threads = []
        self.server = socket.socket()
        self.server.bind(self.get_server_address())
        logging.info("listening")
        self.handle_connections()

    def handle_connections(self):
        while True:
            self.server.listen(5)
            conn, addr = self.server.accept()
            if addr not in self._clients.keys():
                user = User(conn, addr)
                self._clients[addr] = user
            else:
                user = self._clients[addr]

            client_thread = Thread(target=ClientThread, args=(self.server, user))
            self._clint_threads.append(client_thread)
            client_thread.start()

    @staticmethod
    def get_server_address():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect(('<broadcast>', 0))
        host = s.getsockname()[0]
        return host, config_network.SERVER_PORT


if __name__ == "__main__":
    server = MainServer()
