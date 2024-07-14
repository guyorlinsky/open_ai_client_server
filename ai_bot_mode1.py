import threading
from ai_bot_base import AIBotBase
import time

"""
this bot is all ways keeping track of the conversation.
every chosen amount of msgs passed in the conv it outputs a contextualized
msg to the conv held on the server using the open ai api.
it extends the base bot.
"""


class AIBotMode1(AIBotBase):
    def __init__(self, username, lines_to_response, ip="127.0.0.1", port=1234):
        super().__init__(username, ip, port)
        self.lines_to_response = lines_to_response
        self.lines_count = 0
        # self.ai_thread = threading.Thread(target=self._receive_messages)
        # self.ai_thread.daemon = True
        # self.ai_thread.start()

    def _receive_messages(self):
        while True:
            try:
                username_header = self._client_socket.recv(self._header_length)
                if not username_header:
                    self._on_connection_closed()
                    return

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

                if message:
                    self.conversation.append(f"{username}: {message}")
                    self.lines_count += 1

                    if self.lines_count >= self.lines_to_response:
                        response_message = self._generate_message()
                        time.sleep(
                            2)  # Simulate delay for generating the response
                        # print(self.conversation)
                        self._send_message(response_message)
                        print(f"{self._username} said: {response_message}")
                        self.lines_count = 0
                time.sleep(1)



            except IOError:
                continue

            except Exception as e:
                self._on_error(e)
                break
