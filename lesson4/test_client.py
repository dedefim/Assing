
import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import resp, eror, users, name_accaunte, TIME, act, presen
from client import create_presence, process_ans

class TestClass(unittest.TestCase):
    def test_presense(self):
        test = create_presence()
        test[TIME] = 1.1

        self.assertEqual(test, {act: presen, TIME: 1.1, users: {name_accaunte: 'Guest'}})

    def ans_200(self):
        self.assertEqual(process_ans({resp: 200}), '200 : OK')

    def ans_400(self):
        self.assertEqual(process_ans({resp: 400, eror: 'Bad Request'}), '400 : Bad Request')

    def response(self):
        self.assertRaises(ValueError, process_ans, {eror: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
