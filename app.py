#FLASK LIBRARY AND EXTENSIONS
from flask import Flask, request, Response, render_template, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message

#STANDARD LIBRARY
import os
import datetime
import random
import hashlib
import secrets

#OTHER THIRD PARTY LIBRARIES
from dotenv import load_dotenv
from validate_email import validate_email
import jwt

#CUSTOM FILES AND IMPORTS
from models import db, Stations, Plugs
from api import api, DirectionsResource

#INITIALIZE APP AND PLUGINS
app = Flask(__name__)
cors = CORS()
mail = Mail()

#CONFIGURE APP SETTINGS
load_dotenv(verbose = True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_PORT'] = 465

api.add_resource(DirectionsResource, '/api/directions')


#INITIALIZE FLASK EXTENSIONS
db.init_app(app)
mail.init_app(app)
cors.init_app(app)
api.init_app(app)

#OTHER ROUTES
@app.route('/', methods = ['GET'])
def index():
	return "Index"


if __name__ == "__main__":
	app.run(debug=True, use_reloader=True)
