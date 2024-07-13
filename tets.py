import unittest
import threading
import time
import socket

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234


class TestChatServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Start the server in a separate thread
        cls.server_thread = threading.Thread(target=cls.run_server)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(1)  # Wait a bit for the server to start

    @classmethod
    def run_server(cls):
        import server
        server.run_server()

    def setUp(self):
        # Connect client1
        self.client1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client1_socket.connect((IP, PORT))
        self.client1_socket.setblocking(False)
        self.client1_username = "client1"
        self.send_message(self.client1_socket, self.client1_username)

        # Connect client2
        self.client2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client2_socket.connect((IP, PORT))
        self.client2_socket.setblocking(False)
        self.client2_username = "client2"
        self.send_message(self.client2_socket, self.client2_username)

    def send_message(self, client_socket, message):
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

    def receive_message(self, client_socket):
        try:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not username_header:
                return None

            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            return username, message

        except:
            return None

    def test_message_exchange(self):
        # Client1 sends a message
        self.send_message(self.client1_socket, "Hello from client1")

        # Client2 should receive the message
        time.sleep(1)  # Give some time for the message to be processed
        received = self.receive_message(self.client2_socket)
        self.assertIsNotNone(received)
        username, message = received
        self.assertEqual(username, "client1")
        self.assertEqual(message, "Hello from client1")

        # Client2 sends a message
        self.send_message(self.client2_socket, "Hello from client2")

        # Client1 should receive the message
        time.sleep(1)  # Give some time for the message to be processed
        received = self.receive_message(self.client1_socket)
        self.assertIsNotNone(received)
        username, message = received
        self.assertEqual(username, "client2")
        self.assertEqual(message, "Hello from client2")

    def tearDown(self):
        self.client1_socket.close()
        self.client2_socket.close()


if __name__ == "__main__":
    unittest.main()
