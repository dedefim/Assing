import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import response, error, users, name_account, TIME, action, presence
from client import create_presence, process_ans


class TestClass(unittest.TestCase):
    def test_def_presense(self):
        test = create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {action: presence, TIME: 1.1, users: {name_account: 'Guest'}})

    def test_200_ans(self):
        """Тест корректтного разбора ответа 200"""
        self.assertEqual(process_ans({response: 200}), '200 : OK')

    def test_400_ans(self):
        """Тест корректного разбора 400"""
        self.assertEqual(process_ans({response: 400, error: 'Bad Request'}), '400 : Bad Request')

    def test_no_response(self):
        """Тест исключения без поля RESPONSE"""
        self.assertRaises(ValueError, process_ans, {error: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
