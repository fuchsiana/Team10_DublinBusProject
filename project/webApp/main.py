'''
Created on 20 Jun 2017

@author: EByrn
'''
# Make sure you install sql alchemy and pymysql to run these. Just use pip install to do so
# This is the main flask app, run the run.py file to run the code

from webApp import app
from flask import Flask, flash, render_template, request, abort, jsonify
from flask_cors import CORS, cross_origin
from webApp.Connect_DB import connect_db
import webApp.get_predictive_time as gpt
import json
import time
from datetime import datetime
import sys, os
import pickle

# Global variable
global ROUTE
global DIRECTION

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/fareInfo", methods=["GET"])
def fareInfo():
    return render_template('fareInfo.html')

@app.route("/generalInfo", methods=["GET"])
def generalInfo():
    return render_template('generalInformation.html')


@app.route('/test', methods=['POST'])
def test():
    ''' Test function to get time predictions from db '''
    engine = connect_db('team1010.cnmhll8wqxlt.us-west-2.rds.amazonaws.com', '3306', 'DBus', 'Team1010_User',
                        'password.txt')
    req = {}
    req['route'] = ROUTE
    req['direction'] = DIRECTION
    req['orig_stop_id']=request.form['origin'].split(', ')[0]
    req['dest_stop_id'] = request.form['destination'].split(', ')[0]
    req['time'] = request.form['time']
    # Idea to split date format dd/mm/yy into day, month and date adapted from https://stackoverflow.com/questions/4056683/python-getting-weekday-from-an-input-date
    inputDate = time.strftime("%A %Y-%m-%d", time.strptime(request.form['date'], "%d/%m/%Y"))
    req['day'] = inputDate.split()[0]
    req['date'] = inputDate.split()[1]
    # Get prediction timetable
    predictive_time = gpt.get_predictive_timetable(req)
    # Get stops information from pickle file
    thisPlace = os.path.dirname(os.path.abspath(__file__))
    stopsInfo = os.path.join(thisPlace, 'stops_info.pkl')
    file = open(stopsInfo, 'rb')
    #file = open('stops_info.pkl', 'rb')
    stops = pickle.load(file)
    file.close()
    return render_template('form.html', journeyTime=predictive_time[2], origin=req['orig_stop_id'], destination=req['dest_stop_id'],
                           time=predictive_time[0], day=req['day'], date=req['date'], stops=stops, req=req)


@app.route('/direction', methods=['GET'])
def direction():
    ''' This function gets the corresponding stops for the direction when the route is typed into the input field '''

    global ROUTE

    ROUTE = request.args.get('route').zfill(4)
    engine = connect_db('team1010.cnmhll8wqxlt.us-west-2.rds.amazonaws.com', '3306', 'DBus', 'Team1010_User',
                        'password.txt')

    # Get the direction
    sql = "SELECT trip_headsign FROM routes WHERE route_short_name = %s;"
    rows = engine.execute(sql, ROUTE).fetchall()
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
    global ROUTE
    global DIRECTION

    ''' This function gets the corresponding stops for the direction along the chosen route '''
    DIRECTION = request.args.get('direction')

    engine = connect_db('team1010.cnmhll8wqxlt.us-west-2.rds.amazonaws.com', '3306', 'DBus', 'Team1010_User',
                        'password.txt')
    # Get origin stops - dividing this section into origin and destination stops may not be necessary
    # as the stops for origin and destination will be the same for that route
    #sql = "SELECT origin FROM TestTable where route = %s order by origin asc;"
    sql = """ SELECT stop_id, stop_name FROM routes_stops WHERE route_short_name = %s AND trip_headsign = %s;"""
    rows = engine.execute(sql, ROUTE.zfill(4), DIRECTION).fetchall()
    originStops = []
    # rows returns a 2D array
    for i in rows:
        originStops.append(i[0] + ", " +i[1])
            
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