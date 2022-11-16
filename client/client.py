import json
import socket
import config_network


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(config_network.SERVER_ADDR)
        self.start()

    def start(self):
        while cmd := input():
            if cmd.startswith('answer'):
                intent, answer = cmd.split()
                message = json.dumps({'intent': intent, 'answer': answer})
            else:
                message = json.dumps({'intent': cmd})
            self.client.send(message.encode('utf-8'))
            response = self.client.recv(4096).decode('utf-8')
            if not response:
                break
            print(response)

    def get_response(self):
        message = ""
        while response := self.client.recv(4096):
            message += response.decode('utf-8')
        print(message)


if __name__ == "__main__":
    client = Client()
