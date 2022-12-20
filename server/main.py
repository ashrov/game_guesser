import logging

from server import MainServer


logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    server = MainServer()
