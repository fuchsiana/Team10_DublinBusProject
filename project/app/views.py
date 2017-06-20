'''
Created on 20 Jun 2017

@author: EByrn
'''
from app import app
from flask import render_template

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/hello")
def hello():
    return "Hello world!!"
    