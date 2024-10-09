import threading
import time
from ai_bot_base import AIBotBase

"""
This bot outputs a random message at a specified interval using 
the ChatGPT API.
"""

class AIBotMode2(AIBotBase):
    def __init__(self, username, interval, ip="127.0.0.1", port=1234):
        super().__init__(username, ip, port)
        self.interval = interval
        self.ai_thread = threading.Thread(target=self._ai_bot_mode_2)
        self.ai_thread.daemon = True  # Allows the thread to exit when the main program exits
        self.ai_thread.start()


    def _ai_bot_mode_2(self):
        while True:
            message = self._generate_message()
            self._send_message(message)
            print(f"{self._username} said: {message}")
            time.sleep(self.interval)
