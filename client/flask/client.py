import json
import logging
import socket
import config_network

logging.basicConfig(level=logging.INFO)
socket_buffer_size = 1024


def get_server_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    host = s.getsockname()[0]
    return "localhost", config_network.SERVER_PORT


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_addr = get_server_address()
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
        server_addr = get_server_address()
        logging.info(f"trying to connect to {server_addr}")
        self.client.connect(server_addr)
        logging.info(f"connected to {server_addr}")
        self.start()

    def start(self):
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
        response_len = 4096
        while response_len == 4096:
            response = self.client.recv(4096)
            message += response.decode('utf-8')
            response_len = len(response)
        return message


if __name__ == "__main__":
    client = ConsoleClient()
