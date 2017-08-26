'''
Created on 8 Jul 2017

@author: EByrn
'''
from Connect_DB import connect_db

def make_table():
    ''' Function to connect to the database and create a table if it doesn't already exist '''
    engine = connect_db('137.43.49.45', '3306', 'Team1010_Test', 'remoteuser', 'password2.txt')
    try:
        sql = """CREATE TABLE IF NOT EXISTS test2
            (route VARCHAR(45) NOT NULL,
            day VARCHAR(45) NOT NULL,
            origin_stop FLOAT NOT NULL,
            destination_stop FLOAT NOT NULL,
            PRIMARY KEY (route));"""
        engine.execute(sql)
        
    except Exception as e:
        print("Error Type: ",  type(e))
        print("Error Details: ", e)
        

def write_to_table():
    ''' Function to connect to the database and insert values into a specific table '''
    engine = connect_db('137.43.49.45', '3306', 'Team1010_Test', 'remoteuser', 'password2.txt')
    try:
        sql = """ INSERT INTO test2 (route, day, origin_stop, destination_stop) VALUES ("46A", "Monday", "1", "10"); """
        engine.execute(sql)
        
    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)