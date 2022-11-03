import socket


sock = socket.socket()
sock.connect(('127.0.0.1', 5678))
sock.send(b'(123;123)')
sock.recv(1024)
sock.close()
