from ai_bot_base import AIBotBase

"""
This bot always keeps track of the conversation.
Every chosen amount of messages passed in the conversation,
it outputs a contextualized message to the conversation held on the server 
using the OpenAI API. It extends the base bot.
"""

class AIBotMode1(AIBotBase):
    def __init__(self, username, lines_to_response, ip="127.0.0.1", port=1234):
        super().__init__(username, ip, port)
        self.lines_to_response = lines_to_response
        self.lines_count = 0

    def _on_message_received(self, username, message):
        self.conversation.append(f"{username}: {message}")
        self.lines_count += 1

        if self.lines_count >= self.lines_to_response:
            response_message = self._generate_message()
            self._send_message(response_message)
            print(f"{self._username} > {response_message}")
            self.lines_count = 0
