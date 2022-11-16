import json
import socket
import config_network


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.get_server_address())
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

    @staticmethod
    def get_server_address():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect(('<broadcast>', 0))
        host = s.getsockname()[0]
        return host, config_network.SERVER_PORT


if __name__ == "__main__":
    client = Client()
