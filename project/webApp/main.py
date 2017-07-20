'''
Created on 20 Jun 2017

@author: EByrn
'''
# Make sure you install sql alchemy and pymysql to run these. Just use pip install to do so
# This is the main flask app, run the run.py file to run the code

from webApp import app
from flask import render_template, request, jsonify
from webApp.Connect_DB import connect_db

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test():
    ''' Test function to get time predictions from db '''
    engine = connect_db('team1010-test.cnmhll8wqxlt.us-west-2.rds.amazonaws.com', '3306', 'Team1010_Test', 'root', 'password.txt')
    Origin=request.form['origin']
    Destination=request.form['destination']
    # This is just a random query I made to test functionality of more complex queries, I set my table up only to have stopID from 1-10
    sql = "SELECT ABS(t2.time - t1.time) FROM time_table t1, time_table t2 where t1.stopID = %s and t2.stopID = %s;"
    rows = engine.execute(sql, Origin, Destination).fetchall() 
    engine.dispose()
    return render_template('form.html', origin=Origin, destination=Destination, time=int(rows[0][0]))
 
 
@app.route('/test2', methods=['GET', 'POST'])
def test2():
    ''' Test function to access data submitted via form and display on front end '''
    engine = connect_db('team1010-test.cnmhll8wqxlt.us-west-2.rds.amazonaws.com', '3306', 'Team1010_Test', 'root', 'password.txt')
    Route=request.form['route']
    sql = "SELECT * FROM test where route = %s;" # %s is a placeholder for route in this case
    rows = engine.execute(sql, Route).fetchall()
    info = jsonify(info=[dict(row) for row in rows])    
    engine.dispose()
    return info
    #return render_template('index.html', Route=request.form['route'], Time=request.form['time'], Origin=request.form['origin'], Destination=request.form['destination'])   
   
   
@app.route('/routes', methods=['GET'])
def routes():
    ''' This function gets the corresponding stops for the route when the route is typed into the input field '''
    x = request.args.get('route')
    engine = connect_db('team1010-test.cnmhll8wqxlt.us-west-2.rds.amazonaws.com', '3306', 'Team1010_Test', 'root', 'password.txt')
    
    # Get origin stops - dividing this section into origin and destination stops may not be necessary
    # as the stops for origin and destination will be the same for that route
    sql = "SELECT origin_stop FROM test2 where Route = %s order by origin_stop asc;"
    rows = engine.execute(sql, x).fetchall()
    originStops = []
    # rows returns a 2D array
    for i in rows:
        for j in i:
            originStops.append(j)
            
    # Get destination stops        
    sql2 = "SELECT origin_stop FROM test2 where Route = %s order by destination_stop asc;"
    rows2 = engine.execute(sql2, x).fetchall()
    destinationStops = []
    for i in rows2:
        for j in i:
            destinationStops.append(j)
            
    engine.dispose()    
    output = {}
    output['originStops'] = originStops
    output['destinationStops'] = destinationStops
    return jsonify(output)

