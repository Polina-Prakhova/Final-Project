import unittest


class Test(unittest.TestCase):
    """ Temporary test """
    def check(self):
        self.assertEqual('foo'.upper(), 'FOO')
