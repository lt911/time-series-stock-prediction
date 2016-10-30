__author__ = 'liz'

import unittest
from analysis import *

'''This is a module for testing the class Analysis'''

class MyTestCase(unittest.TestCase):
    def setUp(self):
        start = "2014-11-11"
        end = "2015-12-14"
        ticker = "YHOO"
        self.data = Analysis(start, end, ticker)

    def test_Date(self):
        ''' test if the file is emtpy '''
        self.assertFalse(self.data.df.empty)

    def test_d_param(self):
        '''test if the d_param will rasie error if arg is not [0,1,2]'''
        self.assertRaises(InvalidParamError, lambda: self.data.d_param(3))
        self.assertRaises(InvalidParamError, lambda: self.data.d_param(10))

    def test_d_determination(self):
        ''' test data_d_determination() returns only values in [0,1,2'''
        self.assertTrue(self.data.d_determination() in [0,1,2])
        self.assertFalse(self.data.d_determination() == [x for x in range(3,10)])

    def test_param_df(self):
        ''' test the param_df is not empty in order for future param determination'''
        self.assertFalse(self.data.param_df().empty)

    def test_param_determination(self):
        ''' test to check every entry in the param order is in [0,1,2]'''
        self.assertTrue(self.data.param_determination()[0] in [0,1,2])
        self.assertTrue(self.data.param_determination()[1] in [0,1,2])
        self.assertTrue(self.data.param_determination()[2] in [0,1,2])

    def test_predict_val(self):
        ''' test to check arima model generates a nonempty array of predicted values for the predict df'''
        self.assertFalse(self.data.predict_val().empty)




if __name__ == '__main__':
    unittest.main()
