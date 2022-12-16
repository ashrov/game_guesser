import json
import logging
import socket
import config_network


CONSOLE_HELP_MESSAGE = "start - начать угадывать\n" \
                       "answer [yes/no/dn] - ответить на тэг да/нет/не знаю\n" \
                       "get_current_games - получить подходящие игры\n" \
                       "get_same_games - получить не полностью подходящие игры (нужно, если нет полностью подходящих)\n"


logging.basicConfig(level=logging.INFO)
socket_buffer_size = 1024


class BasicClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = ("localhost", config_network.SERVER_PORT)
        logging.info(f"trying to connect to {server_addr}")
        self.client.connect(server_addr)
        logging.info(f"connected to {server_addr}")

    def send_message(self, message: dict) -> dict:
        self.client.send(json.dumps(message).encode('utf-8'))
        response = self._get_response()
        return json.loads(response)

    def _get_response(self):
        message = ""
        response_len = socket_buffer_size
        while response_len == socket_buffer_size:
            response = self.client.recv(socket_buffer_size)
            message += response.decode('utf-8')
            response_len = len(response)

        return message


class Client(BasicClient):
    def start_guessing(self):
        message = {"intent": "start"}
        return self.send_message(message)

    def answer(self, answer: str):
        message = {"intent": "answer", "answer": answer}
        return self.send_message(message)

    def get_current_games(self):
        message = {"intent": "get_current_games"}
        return self.send_message(message)

    def get_same_games(self):
        message = {"intent": "get_same_games"}
        return self.send_message(message)


class ConsoleClient(BasicClient):
    def start(self):
        print(CONSOLE_HELP_MESSAGE)
        while cmd := input():
            if cmd.startswith('answer'):
                intent, answer = cmd.split()
                message = json.dumps({'intent': intent, 'answer': answer})
            else:
                message = json.dumps({'intent': cmd})
            self.client.send(message.encode('utf-8'))

            response = self._get_response()
            if not response:
                break
            print(response)


if __name__ == "__main__":
    client = ConsoleClient()
    client.start()
