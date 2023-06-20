"""Unit-тесты утилит"""

import sys
import os
import unittest
import json
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import resp, eror, users, name_accaunte, TIME, act, presen, ENCODING
from common.utils import get_message, send_message

class TestSocket:
    def __init__(self, test_di):
        self.test_di = test_di
        self.encoded_message = None
        self.receved_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_di)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.receved_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_di)
        return json_test_message.encode(ENCODING)


class Tests(unittest.TestCase):
    test_di_send = {
        act: presen,
        TIME: 111111.111111,
        users: {
            name_accaunte: 'test_test'
        }
    }
    test_dict_recv_ok = {resp: 200}
    test_dict_recv_err = {
        resp: 400,
        eror: 'Bad Request'
    }

    def send_message(self):
        socket = TestSocket(self.test_di_send)
        send_message(socket, self.test_di_send)
        self.assertEqual(socket.encoded_message, socket.receved_message)
        with self.assertRaises(Exception):
            send_message(socket, socket)

    def get_message(self):
        sock_ok = TestSocket(self.test_dict_recv_ok)
        sock_err = TestSocket(self.test_dict_recv_err)
        self.assertEqual(get_message(sock_ok), self.test_dict_recv_ok)
        self.assertEqual(get_message(sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
