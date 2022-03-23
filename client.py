import socket
import threading
import time

from enum import Enum


class OperationType(Enum):
    GET = 1
    ADD = 2


class TinyLFUClient:

    def __init__(self, port=5555, ip=socket.gethostbyname(socket.gethostname())):

        self.port = port
        self.ip = ip
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.size = 2048

    def start(self):

        try:

            self.client.connect((self.ip, self.port))
            print(f"[CONNECTED] Client connected to server at {self.ip}:{self.port}")

            ping_thread = threading.Thread(target=self.__ping_server, args=(self.client,))
            listening_thread = threading.Thread(target=self.__handle_server_connection, args=(self.client,))
            ping_thread.start()
        except socket.error as exc:
            pass
        except KeyboardInterrupt as exc:
            pass
        finally:
            try:
                self.client.close()
                print("Closing the client.")
            except socket.error as exc:
                pass

    def __ping_server(self, connection):

        try:
            connected = True
            while connected:
                data = connection.recv(self.size)
                if not data:
                    break

                time.sleep(2)
                connection.send(data)
        except socket.error as exc:
            pass
        finally:
            try:
                print(f"[DISCONNECTION] {self.port} disconnected.")
                connection.close()
            except socket.error as exc:
                pass

    def __handle_server_connection(self, connection):

        try:
            msg = connection.recv(self.size)
            print(f"[SERVER] {msg}")
        except socket.error as exc:
            pass
        finally:
            try:
                connection.close()
                print("Closing connection")
            except socket.error as exc:
                pass

    def get(self, key):

        return self.send_message(OperationType.GET, key)

    def add(self, key, value):

        return self.send_message(OperationType.ADD, key, value)

    def send_message(self, *args):

        try:
            if self.client:
                if len(args) == 2 and args[0] == OperationType.GET:
                    msg = f"GET {args[1]}"
                    self.client.send(msg)
                    return 0
                if len(args) == 3 and args[0] == OperationType.ADD:
                    msg = f"ADD {args[1]} && {args[2]}"
                    self.client.send(msg)
                    return 0
                return -1
            else:
                return -1
        except socket.error as exc:
            print("Error occurred. Unable to send message.")
            return -1


if __name__ == "__main__":
    client = TinyLFUClient()
    client.start()
