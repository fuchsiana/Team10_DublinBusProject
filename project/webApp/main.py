'''
Created on 20 Jun 2017

@author: EByrn
'''
# Make sure you install sql alchemy and pymysql to run these. Just use pip install to do so
# This is the main flask app

from webApp import app
from flask import render_template, request, jsonify
from webApp.Connect_DB import connect_db

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('greeting.html', Route=request.form['route'], Time=request.form['time'], Embark=request.form['embark'], Disembark=request.form['disembark'])   

@app.route('/db')
def show_db():
    ''' Function to connect to the database and display the contents of the test table on the front end '''
    engine = connect_db('team1010-test.cnmhll8wqxlt.us-west-2.rds.amazonaws.com', '3306', 'Team1010_Test', 'root', 'password.txt')
    sql = "SELECT * FROM test;"
    rows = engine.execute(sql).fetchall()
    info = jsonify(info=[dict(row) for row in rows])    
    engine.dispose()
    return info   

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



