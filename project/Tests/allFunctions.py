from sqlalchemy import create_engine
from flask import Flask, flash, render_template, request, abort, jsonify


###############################
## Functions from Connect_DB ##
###############################
# To create engine - adapted from previous projects and http://docs.sqlalchemy.org/en/latest/core/engines.html
def connect_db(URI, PORT, DB, USER, password):
    ''' Function to connect to the database '''
    try:
        fh = open(password)
        PASSWORD = fh.readline().strip()
        engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)
        return engine
    except Exception as e:
        print("Error Type: ", type(e))
        print("Error Details: ", e)


def test_query():
    ''' Query to return the number of items returned from the MySQL database '''
    engine = connect_db('137.43.49.45', '3306', 'DBus', 'remoteuser', 'password2.txt')
    sql = "SELECT count(trip_headsign) from routes where route_short_name = '0150';"
    rows = engine.execute(sql).fetchall()
    engine.dispose()
    answer = rows[0][0]
    return answer

#################################
## Functions from create_table ##
#################################
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
        
        
def make_table_and_write_to_table():
    ''' Query to return the number of items returned from the MySQL database '''
    engine = connect_db('137.43.49.45', '3306', 'Team1010_Test', 'remoteuser', 'password2.txt')
    make_table()
    write_to_table()
    sql = "SELECT * from test2;"
    rows = engine.execute(sql).fetchall()
    results = []
    for i in rows:
        for j in i:
            results.append(j)
    engine.dispose()
    return results