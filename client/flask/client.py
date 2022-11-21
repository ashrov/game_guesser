import json
import logging
import socket
import config_network


CONSOLE_HELP_MESSAGE = "start - начать угадывать\n" \
                       "answer [yes/no/dn] - ответить на тэг да/нет/не знаю\n" \
                       "get_current_games - получить подходящие игры\n" \
                       "get_same_game - получить не полностью подходящие игры (нужно, если нет полностью подходящих)\n"


logging.basicConfig(level=logging.INFO)
socket_buffer_size = 1024


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = ("localhost", config_network.SERVER_PORT)
        logging.info(f"trying to connect to {server_addr}")
        self.client.connect(server_addr)
        logging.info(f"connected to {server_addr}")

    def send_message(self, js: dict) -> dict:
        self.client.send(json.dumps(js).encode('utf-8'))
        response = self.get_response()
        print(response)
        return json.loads(response)

    def get_response(self):
        message = ""
        response_len = socket_buffer_size
        while response_len == socket_buffer_size:
            response = self.client.recv(socket_buffer_size)
            message += response.decode('utf-8')
            response_len = len(response)

        return message


class ConsoleClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = ("localhost", config_network.SERVER_PORT)
        logging.info(f"trying to connect to {server_addr}")
        self.client.connect(server_addr)
        logging.info(f"connected to {server_addr}")
        self.start()

    def start(self):
        print(CONSOLE_HELP_MESSAGE)
        while cmd := input():
            if cmd.startswith('answer'):
                intent, answer = cmd.split()
                message = json.dumps({'intent': intent, 'answer': answer})
            else:
                message = json.dumps({'intent': cmd})
            self.client.send(message.encode('utf-8'))
            response = self.get_response()
            if not response:
                break
            print(response)

    def get_response(self):
        message = ""
        response_len = socket_buffer_size
        while response_len == socket_buffer_size:
            response = self.client.recv(socket_buffer_size)
            message += response.decode('utf-8')
            response_len = len(response)
        return message


if __name__ == "__main__":
    client = ConsoleClient()
