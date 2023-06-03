"""Unit-тесты сервера"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import resp, eror, users, name_accaunte, TIME, act, presen
from server import process_client_message

class TestServer(unittest.TestCase):
    err_dict = {
        resp: 400,
        eror: 'Bad Request'
    }
    ok_dict = {resp: 200}

    def no_action(self):
        self.assertEqual(process_client_message(
            {TIME: '1.1', users: {name_accaunte: 'Guest'}}), self.err_dict)

    def wrong_action(self):
        self.assertEqual(process_client_message(
            {act: 'Wrong', TIME: '1.1', users: {name_accaunte: 'Guest'}}), self.err_dict)

    def no_time(self):
        self.assertEqual(process_client_message(
            {act: resp, users: {name_accaunte: 'Guest'}}), self.err_dict)

    def no_user(self):
        self.assertEqual(process_client_message(
            {act: presen, TIME: '1.1'}), self.err_dict)

    def unknown_user(self):
        self.assertEqual(process_client_message(
            {act: presen, TIME: 1.1, users: {name_accaunte: 'Guest1'}}), self.err_dict)

    def ok_check(self):
        self.assertEqual(process_client_message(
            {act: presen, TIME: 1.1, users: {name_accaunte: 'Guest'}}), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
