"""Unit-тесты утилит"""

import sys
import os
import unittest
import json
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import response, error, users, name_account, TIME, action, presence, ENCODING
from common.utils import get_message, send_message

class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.receved_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.receved_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class Tests(unittest.TestCase):
    test_dict_send = {
        action: presence,
        TIME: 111111.111111,
        users: {
            name_account: 'test_test'
        }
    }
    test_dict_recv_ok = {response: 200}
    test_dict_recv_err = {
        response: 400,
        error: 'Bad Request'
    }
    def test_send_message(self):
        test_socket = TestSocket(self.test_dict_send)
        send_message(test_socket, self.test_dict_send)
        self.assertEqual(test_socket.encoded_message, test_socket.receved_message)
        self.assertRaises(TypeError, send_message, test_socket, 1111)

    def test_get_message(self):
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)
        self.assertEqual(get_message(test_sock_ok), self.test_dict_recv_ok)
        self.assertEqual(get_message(test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
