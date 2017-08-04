'''
Created on 27 July 2017

@author: EByrn
'''
#import sys
#sys.path.append("C:/Users/EByrn/workspace/team1010/Team-10")
import unittest
from create_table import make_table

def t2(x,y):
    if x > y:
        return True
    else:
        return False


class Test(unittest.TestCase):
    
    def test_setup(self):
        pass
    
    #def test_connection(self):
        """ Tests if connection to database functions """
    #    self.assertEqual(connect_db('team1010-test.cnmhll8wqxlt.us-west-2.rds.amazonaws.com', '3306', 'Team1010_Test', 'root', 'password.txt'), create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True))
        
    def test_t2(self):
        self.assertEqual(t2(4, 2), True)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()