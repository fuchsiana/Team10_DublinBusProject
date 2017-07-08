'''
Created on 20 Jun 2017

@author: EByrn
'''
from app import app
from flask import Flask, render_template, request

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('greeting.html', Route=request.form['route'], Time=request.form['time'], Embark=request.form['embark'], Disembark=request.form['disembark'])   


######################################################################################################################
# Test code obtained from https://developer.mozilla.org/en-US/docs/Learn/HTML/Forms/Sending_and_retrieving_form_data #
######################################################################################################################
# from app import app
# from flask import Flask, render_template, request
# 
# @app.route('/', methods=['GET', 'POST'])
# def form():
#     return render_template('form.html')
# 
# @app.route('/hello', methods=['GET', 'POST'])
# def hello():
#     return render_template('greeting.html', say=request.form['say'], to=request.form['to'])   



