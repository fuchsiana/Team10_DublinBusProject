'''
Created on 20 Jun 2017

@author: EByrn
'''

from flask import Flask, flash, render_template, request, abort, jsonify
from flask_cors import CORS, cross_origin
from Connect_DB import connect_db
import get_predictive_time as gpt
import json
import time
import datetime
import sys, os
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)
app.debug = True

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


@app.route('/form', methods=['POST'])
def form():
    ''' Function to get time predictions from db '''
    # Engine when running on server
    #engine = connect_db('127.0.0.1', '3306', 'DBus', 'root', 'password2.txt')
    # Engine when running locally
    engine = connect_db('137.43.49.45', '3306', 'DBus', 'remoteuser', 'password2.txt')
    req = {}
    req['route'] = ROUTE
    req['direction'] = DIRECTION
    req['orig_stop_id']=request.form['origin'].split(', ')[0]
    req['dest_stop_id'] = request.form['destination'].split(', ')[0]
    req['time'] = request.form['time']
    # Idea to split date format dd/mm/yy into day, month and date adapted from https://stackoverflow.com/questions/4056683/python-getting-weekday-from-an-input-date
    inputDate = time.strftime("%A %d-%m-%Y", time.strptime(request.form['date'], "%d/%m/%Y"))
    req['day'] = inputDate.split()[0]
    req['date'] = inputDate.split()[1]

    print(req)
    # Get prediction timetable
    predictive_time_tables, travel_time = gpt.get_predictive_timetable(req)
    print(predictive_time_tables, travel_time)

    # Get stops information from pickle file
    thisPlace = os.path.dirname(os.path.abspath(__file__))
    stopsInfo = os.path.join(thisPlace, 'stops_info.pkl')
    file = open(stopsInfo, 'rb')
    stops = pickle.load(file)
    file.close()

    # Convert travel_time to a cleaner output (HH:MM:SS) - https://stackoverflow.com/questions/775049/python-time-seconds-to-hms
    convert_travel_time = np.asscalar(np.int16(travel_time))
    travel_time_formatted = datetime.timedelta(seconds=convert_travel_time)
    
    return render_template('form.html', journeyTime=travel_time_formatted, origin=req['orig_stop_id'], destination=req['dest_stop_id'], inputTime=req['time'],
                           time=predictive_time_tables, day=req['day'], date=req['date'], stops=stops, req=req, timetable=predictive_time_tables, route=req['route'])



@app.route('/direction', methods=['GET'])
def direction():
    ''' This function gets the corresponding stops for the direction when the route is typed into the input field '''

    global ROUTE

    ROUTE = request.args.get('route').zfill(4)
    # Engine when running on server
    #engine = connect_db('127.0.0.1', '3306', 'DBus', 'root', 'password2.txt')
    # Engine when running locally
    engine = connect_db('137.43.49.45', '3306', 'DBus', 'remoteuser', 'password2.txt')

    # Get the direction
    sql = "SELECT trip_headsign FROM routes WHERE route_short_name = %s;"
    rows = engine.execute(sql, ROUTE).fetchall()
    selectDirection = []
    # rows returns a 2D array
    for i in rows:
        selectDirection.append(i[0])
    
    output = {}
    output['selectDirection'] = selectDirection
    return jsonify(output)
    

@app.route('/stops', methods=['GET'])
def stops():
    global ROUTE
    global DIRECTION

    ''' This function gets the corresponding stops for the direction along the chosen route '''
    DIRECTION = request.args.get('direction')

    # Engine when running on server
    #engine = connect_db('127.0.0.1', '3306', 'DBus', 'root', 'password2.txt')
    # Engine when running locally
    engine = connect_db('137.43.49.45', '3306', 'DBus', 'remoteuser', 'password2.txt')

    sql = """ SELECT stop_id, stop_name FROM routes_stops WHERE route_short_name = %s AND trip_headsign = %s;"""
    rows = engine.execute(sql, ROUTE.zfill(4), DIRECTION).fetchall()
    originStops = []
    for i in rows:
        originStops.append(i[0] + ", " +i[1])
            
    engine.dispose()    
    output = {}
    output['originStops'] = originStops
    return jsonify(output)


if __name__ == "__main__":
    app.run()