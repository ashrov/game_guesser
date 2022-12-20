import json
import socket
from time import time
from logging import getLogger
from threading import Thread

from config import SAME_GAME_SELECTION_SIZE, SERVER_PORT
from gamesdb import Tag, Game, User, CustomJSONEncoder
from guesser import Guesser


logger = getLogger(__name__)


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


def func_time(func):
    def _wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()

        logger.debug(f"function {func.__name__} handled in {end - start} seconds")
        return result
    return _wrapper


class ClientThread:
    def __init__(self, user: User):
        self.user = user
        self.connection = user.connection
        self.address = user.address
        self.guesser = Guesser()

        self.listen_client()

    def _close(self):
        self.guesser.close()

    def listen_client(self):
        logger.info(f"listening connection with {self.address}")

        try:
            while data := self.connection.recv(4096):
                message = data.decode('utf-8')
                response = self.handle_message(message)
                self.connection.send(response.encode('utf-8'))
        except ConnectionResetError:
            logger.info(f"Connection reset by client {self.address}")
        except Exception as er:
            logger.exception(f"Exception at connection with {self.address}. Error: {er}")

        self._close()
        logger.info(f"connection with {self.address} closed.")

    @func_time
    def handle_message(self, mes: str) -> str:
        """ :return: server answer (json dump string) """
        json_message = json.loads(mes)
        logger.debug(f"handling request {json_message}")

        match json_message.get(INTENT):
            case "answer":
                response = self.handle_question_answer(json_message.get(ANSWER))
            case "start":
                response = self.start()
            case "get_current_games":
                response = {CURRENT_GAMES: self.user.current_games}
            case "get_same_games":
                response = {SAME_GAMES: self.guesser.guess_game(self.user, selection_size=SAME_GAME_SELECTION_SIZE)}
            case _:
                response = {ERROR: "bad intent"}

        response_str = json.dumps(response, cls=CustomJSONEncoder)
        logger.debug(f"returning response {response_str}")
        return response_str

    def start(self):
        self.user.reset_tags()
        self.user.current_games = self.guesser.db.all_games
        return {NEW_TAG: self.get_next_tag()}

    def get_next_tag(self) -> Tag:
        new_tag = self.guesser.get_new_tag(self.user)
        self.user.current_tag = new_tag
        return new_tag

    def handle_question_answer(self, result: str) -> dict:
        match result:
            case "yes":
                self.user.add_good_tag(self.user.current_tag)
            case "no":
                self.user.add_bad_tag(self.user.current_tag)
            case "dn":
                self.user.used_tags.append(self.user.current_tag)
            case _:
                return {ERROR: "bad answer result"}

        if self.user.current_games:
            self.user.current_games = self.guesser.guess_game(self.user)
        data = {NEW_TAG: self.get_next_tag(),
                GAMES_COUNT: len(self.user.current_games)}
        return data


class MainServer:
    _clients: dict[User]
    _clint_threads: list[Thread]

    def __init__(self):
        self._clint_threads = []
        self.server = socket.socket()
        addr = ("0.0.0.0", SERVER_PORT)
        logger.info(f"starting server at {addr}")
        self.server.bind(addr)
        logger.info("listening")
        self.handle_connections()

    def handle_connections(self):
        while True:
            self.server.listen(10)
            conn, addr = self.server.accept()
            user = User(conn, addr)

            client_thread = Thread(target=ClientThread, args=(user, ))
            client_thread.start()


if __name__ == "__main__":
    server = MainServer()
