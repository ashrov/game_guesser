from server import Server

server = None
try:
    server = Server()
finally:
    if server:
        server.close()
