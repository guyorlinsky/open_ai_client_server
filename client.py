import socket
import threading

HEADER_LENGTH = 10
"""
the ChatClient is a simple client.
uses the same ip as the server to run on localhost. 
"""


class ChatClient:
    def __init__(self, username, ip="127.0.0.1", port=1234):
        self._username = username
        self._ip = ip
        self._port = port
        self._header_length = HEADER_LENGTH
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_socket.connect((self._ip, self._port))
        self._client_socket.setblocking(False)

        self._send_username()

        self._receive_thread = threading.Thread(target=self._receive_messages)
        self._receive_thread.start()

        self._send_thread = threading.Thread(target=self._send_messages)
        self._send_thread.start()

    def _send_username(self):
        username_encoded = self._username.encode('utf-8')
        username_header = f"{len(username_encoded):<{self._header_length}}".encode(
            'utf-8')
        self._client_socket.send(username_header + username_encoded)

    def _receive_messages(self):
        while True:
            try:
                username_header = self._client_socket.recv(self._header_length)
                if not username_header:
                    self._on_connection_closed()
                    return

                # Validate the username header
                try:
                    username_length = int(
                        username_header.decode('utf-8').strip())
                except ValueError:
                    self._on_error(
                        f"Invalid username header received: {username_header}")
                    continue
                username = self._client_socket.recv(username_length).decode(
                    'utf-8')

                message_header = self._client_socket.recv(self._header_length)
                message_length = int(message_header.decode('utf-8').strip())
                message = self._client_socket.recv(message_length).decode(
                    'utf-8')

                self._on_message_received(username, message)

            except IOError:
                continue

            except Exception as e:
                self._on_error(e)
                break

    def _send_messages(self):
        while True:
            message = input(f'{self._username} > ')
            if message:
                message_encoded = message.encode('utf-8')
                message_header = f"{len(message_encoded):<{self._header_length}}".encode(
                    'utf-8')
                self._client_socket.send(message_header + message_encoded)

    def _on_message_received(self, username, message):
        print(f"{username}: {message}")

    def _on_connection_closed(self):
        print('Connection closed by the server')

    def _on_error(self, e):
        print(f'Error: {e}')


if __name__ == "__main__":
    my_username = input("Username: ")
    chat_client = ChatClient(my_username)
