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
    sql = "SELECT (t2.time - t1.time) FROM time_table t1, time_table t2 where t1.stopID = %s and t2.stopID = %s;"
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
   

######################################################################################################################
# Test code obtained from https://developer.mozilla.org/en-US/docs/Learn/HTML/Forms/Sending_and_retrieving_form_data #
######################################################################################################################
# from web_app import web_app
# from flask import Flask, render_template, request
# 
# @web_app.route('/', methods=['GET', 'POST'])
# def form():
#     return render_template('form.html')
# 
# @web_app.route('/hello', methods=['GET', 'POST'])
# def hello():
#     return render_template('greeting.html', say=request.form['say'], to=request.form['to'])