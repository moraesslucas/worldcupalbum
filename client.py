import socket
import threading


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, address):
        self.sock.connect((address, 10000))

        self.sock.send(bytes(input("Username: "), 'utf-8'))
        self.sock.send(bytes(input("Password: "), 'utf-8'))

        i_thread = threading.Thread(target=self.send_message)
        i_thread.daemon = True
        i_thread.start()

        while True:
            data = self.sock.recv(2048)
            if not data:
                break
            print(data.decode('utf-8'))

    def send_message(self):
        while True:
            self.sock.send(bytes(input(""), 'utf-8'))


client = Client('127.0.0.1')