from ai_bot_base import AIBotBase

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

   def _on_message_received(self, username, message):
    self.conversation.append(f"{username}: {message}")
    self.lines_count += 1
    if self.lines_count >= self.lines_to_response:
        response_message = self._generate_message()
        self._send_message(response_message)
        print(f"{self._username} > {response_message}")
        self.lines_count = 0
