'''
Created on 20 Jun 2017

@author: EByrn
'''
# Make sure you install sql alchemy and pymysql to run these. Just use pip install to do so
# This is the main flask app, run the run.py file to run the code

from webApp import app
from flask import render_template, request, jsonify
from webApp.Connect_DB import connect_db
import json
import time
from datetime import datetime

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/test', methods=['POST'])
def test():
    ''' Test function to get time predictions from db '''
    engine = connect_db('team1010.cnmhll8wqxlt.us-west-2.rds.amazonaws.com', '3306', 'Team1010', 'Team1010_User', 'password.txt')
    Origin=request.form['origin']
    Destination=request.form['destination']
    Time=request.form['time']
    # Idea to split date format dd/mm/yy into day, month and date adapted from https://stackoverflow.com/questions/4056683/python-getting-weekday-from-an-input-date
    inputDate = time.strftime("%A %B %C", time.strptime(request.form['date'], "%d/%m/%Y"))
    Day = inputDate.split()[0]
    Month = inputDate.split()[1]
    Date = inputDate.split()[2]
    # This is just a random query I made to test functionality of more complex queries, I set my table up only to have stopID from 1-10
    #sql = "SELECT ABS(t2.time - t1.time) FROM time_table t1, time_table t2 where t1.stopID = %s and t2.stopID = %s;"
    #rows = engine.execute(sql, Origin, Destination).fetchall() 
    #engine.dispose()
    #time=int(rows[0][0])
    calc = abs(int(Origin) - int(Destination))
    return render_template('form.html', journeyTime=Time, origin=Origin, destination=Destination, time=calc, day=Day, month=Month, date=Date)
   
@app.route('/direction', methods=['GET'])
def direction():
    ''' This function gets the corresponding stops for the direction when the route is typed into the input field '''
    x = request.args.get('route')
    engine = connect_db('team1010.cnmhll8wqxlt.us-west-2.rds.amazonaws.com', '3306', 'Team1010', 'Team1010_User', 'password.txt')
    # Get the direction
    sql = "SELECT direction from TestTable_direction where route = %s;"
    rows = engine.execute(sql, x).fetchall()
    selectDirection = []
    # rows returns a 2D array
    for i in rows:
        for j in i:
            selectDirection.append(j)
    
    output = {}
    output['selectDirection'] = selectDirection
    return jsonify(output)
    

@app.route('/stops', methods=['GET'])
def stops():
    ''' This function gets the corresponding stops for the direction along the chosen route '''
    x = request.args.get('direction')
    engine = connect_db('team1010.cnmhll8wqxlt.us-west-2.rds.amazonaws.com', '3306', 'Team1010', 'Team1010_User', 'password.txt')
    # Get origin stops - dividing this section into origin and destination stops may not be necessary
    # as the stops for origin and destination will be the same for that route
    #sql = "SELECT origin FROM TestTable where route = %s order by origin asc;"
    sql = "SELECT origin from TestTable where direction=%s order by origin asc;"
    rows = engine.execute(sql, x).fetchall()
    originStops = []
    # rows returns a 2D array
    for i in rows:
        for j in i:
            originStops.append(j)
            
    # Get destination stops        
    #sql2 = "SELECT origin FROM TestTable where route = %s order by destination asc;"
    #rows2 = engine.execute(sql2, x).fetchall()
    #destinationStops = []
    #for i in rows2:
    #    for j in i:
    #        destinationStops.append(j)
            
    engine.dispose()    
    output = {}
    output['originStops'] = originStops
    #output['destinationStops'] = destinationStops
    return jsonify(output)  