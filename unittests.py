import unittest
from pwgen import *

class TestPwGen(unittest.TestCase):

    def test_pw_without_numbers(self):
        self.assertEqual(generate_pw('constant','facebook.com'), 'ccsoKKlcufAt99')

    def test_regular_pw(self):
        self.assertEqual(generate_pw('c0mpl3xity','facebook.com'), 'c0sl45nlMAam')

    def test_pw_too_short(self):
        with self.assertRaises(SystemExit):
            generate_pw('1', 'facebook.com')

if __name__ == '__main__':
    unittest.main()