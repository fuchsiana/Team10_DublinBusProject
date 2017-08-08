'''
Created on 20 Jun 2017
    
@author: EByrn
'''
    
# Creating init file
import flask
from flask import Flask
from flask_cors import CORS, cross_origin
    
app = Flask(__name__)
CORS(app) # This is to get the real time api connecting
from webApp import main