'''
Created on 20 Jun 2017

@author: EByrn
'''

# Creating init file
import flask
from flask import Flask

app = flask.Flask(__name__)
from webApp import main