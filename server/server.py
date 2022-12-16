import json
import logging
import socket
from threading import Thread

from config import GAME_SELECTION_SIZE, SERVER_PORT
from gamesdb import Tag, Game, User, CustomJSONEncoder
from guesser import Guesser

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
ALL_TAGS = "all_tags"


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
        try:
            while data := self.connection.recv(4096):
                message = data.decode('utf-8')
                response = self.handle_message(message)
                self.connection.send(response.encode('utf-8'))
        except ConnectionResetError:
            logging.info(f"Connection reset by client {self.address}")
        except Exception as er:
            logging.exception(f"Exception at connection with {self.address}. Error: {er}")
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
            case "get_all_tags":
                tags = sorted(self.guesser.db.get_all_tags(), reverse=True)
                response = {ALL_TAGS: tags}
            case "get_by_tags":
                response = {CURRENT_GAMES: self.get_games_by_tags(js)}
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

    def get_games_by_tags(self, js: dict) -> list[Game]:
        tags = js.get("tags", "")
        tmp_user = User(None, None)
        for tag_name in tags:
            tag = self.guesser.db.get_tag_by_name(tag_name)
            tmp_user.good_tags.append(tag)
        return self.guesser.guess_game(tmp_user)


class MainServer:
    _clients: dict[User]
    _clint_threads: list[Thread]

    def __init__(self):
        self._clients = dict()
        self._clint_threads = []
        self.server = socket.socket()
        addr = ("localhost", SERVER_PORT)
        logging.info(f"starting server at {addr}")
        self.server.bind(addr)
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


if __name__ == "__main__":
    server = MainServer()
