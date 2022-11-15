import json
import socket
import config_network


test_message1 = 'Horror_Online Co-Op_Multiplayer_Psychological Horror_Co-op_VR_Supernatural_' \
                'First-Person_Investigation_Dark'
test_message2 = 'Exploration_Singleplayer_Robots_Third Person_Beautiful_Horror_BMX_Sniper'
test_message3 = 'Multiplayer_Strategy'


class Client:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(config_network.SERVER_ADDR)
        self.start()

    def start(self):
        while cmd := input():
            message = json.dumps({'intent': cmd})
            self.client.send(message.encode('utf-8'))
            m = self.client.recv(4096).decode('utf-8')
            print(m)


if __name__ == "__main__":
    client = Client()
