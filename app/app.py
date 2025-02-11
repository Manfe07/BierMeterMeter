from flask import Flask, send_file, render_template, redirect
from prometheus_flask_exporter import PrometheusMetrics
from flask_socketio import SocketIO, send, emit
from flask_migrate import Migrate
from tools import * 

import module_users.users as users
from module_teams import teams_Blueprint
from module_sales import sales_Blueprint

from database import db
import logging

import datetime
import time
import os
import configparser
import json

os.environ['TZ'] = "Europe/Berlin"
time.tzset()

config = configparser.ConfigParser()
config.read('config/config.ini')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('logs/app.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)



app = Flask(__name__) 

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.3')

app.config['SECRET_KEY'] = config['Flask']['SECRET_KEY']
socketio = SocketIO(app, cors_allowed_origins='*')

app.register_blueprint(users.users_Blueprint, url_prefix="/users")
app.register_blueprint(teams_Blueprint, url_prefix="/teams")
app.register_blueprint(sales_Blueprint, url_prefix="/sales")

app.config['SQLALCHEMY_DATABASE_URI'] = config['Flask']['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True


with app.app_context():
    db.init_app(app)
    db.create_all()
    users.init()
    db.session.commit()

    # Migration for sqlalchemy
    MIGRATION_DIR = os.path.join('data', 'migrations')  
    migrate = Migrate(app, db, directory=MIGRATION_DIR)

@app.route('/',methods = ['GET'])
def index():
    return render_template('index.html')



@socketio.on('ping')
def handle_ping(data):
    data["pong"] = datetime.datetime.now().timestamp()
    emit('pong', data, broadcast=False)

@socketio.on('connect')
def test_connect(auth):
    emit('my_response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

# main driver function
if __name__ == '__main__':
    app.run()

