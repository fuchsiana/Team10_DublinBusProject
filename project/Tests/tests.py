'''
Created on 27 July 2017

@author: EByrn
'''

''' ******************* DISCLAIMER ****************************
All functions to be tested will be put into the allFunctions.py 
file and imported from there. This was necessary because there 
were many issues trying to import files from the webApp folder.
The necessary functions will therefore be copied and pasted into 
the allFunctions.py file and tested within this file 
****************************************************************
'''

import unittest
from allFunctions import *
from flask import Flask
import unittest
import os
from flask_testing import TestCase


class Test(unittest.TestCase):
    
    def test_setup(self):
        pass
    
    # Test that the Flask app is working
    def create_app(self):
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 5000
        return app
    
    # Test connecting to the database      
    def test_Connect_to_DB_and_return_value(self):
        self.assertEqual(test_query(), 2)

    # Test creating and populating tables
    def test_make_table_and_write_to_table(self):
        self.assertEqual(make_table_and_write_to_table(), ['46A', 'Monday', 1.0, 10.0])
        
    def test_readFile(self):
        """ This will test if files are being read and parsed correctly """
        line = "Team1010"
        with open('testingReadFile.txt', 'r') as f:
            first_line = f.readline()
            values = first_line.strip().split()
            x = values[0]
        self.assertEqual(line, x)
    
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()