import socket
import threading
import time

import wikipedia as wikipedia

IP = socket.gethostbyname(socket.gethostname())
PORT = 5560
ADDRESS = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"


class TinyLFUServer:

    def __init__(self, port=5555, ip=socket.gethostbyname(socket.gethostname())):
        self.port = port
        self.ip = ip
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):

        print("[STARTING] Server is starting...")

        self.server.bind((self.ip, self.port))
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.ip}:{self.port}")

        try:
            while True:
                connection, address = self.server.accept()
                ping_thread = threading.Thread(target=self.__ping_client, args=(connection, address))
                thread = threading.Thread(target=self.__handle_client, args=(connection, address))
                thread.start()
                ping_thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        except socket.error as exc:
            pass
        except KeyboardInterrupt as exc:
            pass
        finally:
            self.server.close()
            print("Closing the server.")


    def __handle_client(self, connection, address):

        try:
            print(f"[NEW CONNECTION] {address} connected.")

            connected = True
            while connected:
                msg = connection.recv(SIZE).decode(FORMAT)
                if msg == DISCONNECT_MSG:
                    connected = False

                print(f"[{address}] {msg}")
                msg = f"Msg received: {msg}"
                msg = wikipedia.summary(msg, sentences=1)
                connection.send(msg.encode(FORMAT))
        except socket.error as exc:
            pass
        finally:
            connection.close()

    def __ping_client(self, connection, address):

        try:
            connected = True
            while connected:
                data = connection.recv(SIZE)
                if not data:
                    break

                time.sleep(2)
                connection.send(data)
        except socket.error as exc:
            pass
        finally:
            print(f"[DISCONNECTION] {address} disconnected.")
            connection.close()


if __name__ == "__main__":
    server = TinyLFUServer()
    server.start()
