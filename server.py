import socket
import threading
from user_control import UserControl


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    users = {}

    def __init__(self):
        self.sock.bind(('127.0.0.1', 10000))
        self.sock.listen(5)

    def handler(self, c, a):
        while True:
            try:
                data = c.recv(2048)
                ip = self.get_remote_address(a)
                active_user = self.users.get(ip, None)
                
            except Exception as err:
                print('Socket disconnected', err)
                break

            try:
                if active_user is None:
                    self.users[ip] = UserControl(data.decode('utf-8'))
                    continue
                if active_user.logged_in is False:
                    if self.users[ip].validate_login(data.decode('utf-8')) is False:
                        c.sendall(bytes('{"status": "401", "error_message": "invalid credentials"}', 'utf-8'))
                        self.disconnect(c, ip)
                        break
                    for connection in self.connections:
                        connection.sendall(bytes(active_user.user + ' connected!', 'utf-8'))
                    continue

                if data.decode('utf-8') == 'exit':
                    for connection in self.connections:
                        connection.send(bytes(active_user.user + ' disconnected!', 'utf-8'))
                    self.disconnect(c, ip)
                    break

                if not data:
                    self.disconnect(c, ip)
                    break

            except Exception as err:
                print('Error:', err, connection)

            for connection in self.connections:
                try:
                    connection.sendall(bytes(active_user.user + ": " + data.decode('utf-8'), 'utf-8'))
                except Exception as err:
                    print('Error', err, connection)

    def disconnect(self, c, ip):
        print(ip, "disconnected")

        if self.users[ip]:
            del self.users[ip]

        self.connections.remove(c)
        c.close()

    def run(self):
        while True:
            c, a = self.sock.accept()
            c_thread = threading.Thread(target=self.handler, args=(c, a))
            c_thread.daemon = True
            c_thread.start()
            self.connections.append(c)
            ip = self.get_remote_address(a)
            self.users[ip] = None
            print(str(ip), "entered the server")

    @staticmethod
    def get_remote_address(a):
        return str(a[0]) + ':' + str(a[1])


server = Server()
server.run()
