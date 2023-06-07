"""Unit-тесты сервера"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import response, error, users, name_account, TIME, action, presence
from server import process_client_message

class TestServer(unittest.TestCase):
    err_dict = {
        response: 400,
        error: 'Bad Request'
    }
    ok_dict = { response: 200}

    def test_no_action(self):
        self.assertEqual(process_client_message(
            {TIME: '1.1', users: {name_account: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        self.assertEqual(process_client_message(
            {action: 'Wrong', TIME: '1.1', users: {name_account: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        self.assertEqual(process_client_message(
            {action: presence, users: {name_account: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        """Ошибка - нет пользователя"""
        self.assertEqual(process_client_message(
            {action: presence, TIME: '1.1'}), self.err_dict)

    def test_unknown_user(self):
        self.assertEqual(process_client_message(
            {action: presence, TIME: 1.1, users: {name_account: 'Guest1'}}), self.err_dict)

    def test_ok_check(self):
        self.assertEqual(process_client_message(
            {action: presence, TIME: 1.1, users: {name_account: 'Guest'}}), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
