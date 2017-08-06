#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/Team-10/project/webApp")

from project.webApp import app as application
application.secret_key = 'Team1010_Key'