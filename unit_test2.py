"""This is the unit test"""
"""author: sx444"""

import unittest
import other_functions
from unittest import TestCase


class Test(TestCase):
    '''this class is for the test of the functions in the module of other_functions'''
    def setUp(self):
        pass

    def test_get_company_name_1(self):
        self.assertEqual('Google Inc.', other_functions.get_company_name('goog'))

    def test_get_company_name_2(self):
        self.assertEqual('Yahoo! Inc.', other_functions.get_company_name('yhoo'))

    def test_ticker_symbol_1(self):
        self.assertEqual(False, other_functions.test_ticker('APPL'))

    def test_ticker_symbol_2(self):
        self.assertEqual(True,other_functions.test_ticker('GOOG'))

if __name__ == '__main__':
    unittest.main()

