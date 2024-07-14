import requests
from client import ChatClient

# Constants
IP = "127.0.0.1"
PORT = 1234

MAX_TOKENS = 30
OPENAI_API_KEY = ""

"""
this is the base Bot.
it extends ChatClient.
add an OPENAI_API_KEY to activate. 
"""


class AIBotBase(ChatClient):
    def __init__(self, username, ip="127.0.0.1", port=1234):
        super().__init__(username, ip, port)
        self.conversation = []

    def _generate_message(self):
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        if self.conversation:
            messages = [{"role": "system",
                         "content": "You are a chat bot connected to a server with clients."},
                        {"role": "system",
                         "content": "respond to the following conversation of users in a car forum:"}]

            if len(self.conversation) > 10:
                self.conversation = self.conversation[-10:]

            for message in self.conversation:
                messages.append({"role": "user", "content": message})
        else:
            messages = [
                {"role": "system",
                 "content": "you are a chat bot connected to a server with clients"},
                {"role": "user",
                 "content": "Say something that would add spark to the ongoing conversation about cars."}
            ]
        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "max_tokens": MAX_TOKENS
        }

        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content'].strip()
            return message
        else:
            print(f"Error: {response.status_code}")
            return "I'm having trouble thinking of something right now."

    def _send_message(self, message):
        message_encoded = message.encode('utf-8')
        message_header = f"{len(message_encoded):<{self._header_length}}".encode(
            'utf-8')
        self._client_socket.send(message_header + message_encoded)
