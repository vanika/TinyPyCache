import socket
import threading
import time


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
            thread = threading.Thread(target=self.__handle_server_connection, args=(self.client,))
            ping_thread.start()
            thread.start()
        except socket.error as exc:
            pass
        except KeyboardInterrupt as exc:
            pass
        finally:
            self.client.close()
            print("Closing the client.")

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
            print(f"[DISCONNECTION] {self.port} disconnected.")
            connection.close()

    def __handle_server_connection(self, connection):

        try:
            connected = True
            while connected:

                msg = "send message every 3 seconds"
                time.sleep(3)
                connection.send(msg)

                if msg == "disconnect":
                    connected = False
                else:
                    msg = connection.recv(self.size)
                    print(f"[SERVER] {msg}")
        except socket.error as exc:
            pass
        finally:
            connection.close()


if __name__ == "__main__":
    client = TinyLFUClient()
    client.start()
