import socket
import config_network


class Client:

    def __init__(self):
        self.client = socket.socket()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(config_network.SERVER_ADDR)
        self.recev_mes()

    def recev_mes(self):
        test_message1 = 'Horror_Online Co-Op_Multiplayer_Psychological Horror_Co-op_VR_Supernatural_' \
                        'First-Person_Investigation_Dark'
        test_message2 = 'Exploration_Singleplayer_Robots_Third Person_Beautiful_Horror_BMX_Sniper'
        test_message3 = 'Multiplayer_Strategy'
        self.client.send(test_message2.encode('utf-8'))
        while 1:
            m = self.client.recv(4096).decode('utf-8')
            print(m.split(", ")[1])
            break


client = Client()
