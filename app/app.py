from flask import Flask
from flask import Flask, send_file, render_template, redirect, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from flask_socketio import SocketIO, send, emit
from flask_migrate import Migrate
#from tools import * 


from database import db, socketio
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


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    


    metrics = PrometheusMetrics(app)
    metrics.info('app_info', 'Application info', version='1.0.3')

    app.config['SECRET_KEY'] = config['Flask']['SECRET_KEY']
    socketio = SocketIO(app, cors_allowed_origins='*')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = config['Flask']['SQLALCHEMY_DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['DEBUG'] = True


    with app.app_context():
        import module_main as main
        import module_sales as sales
        import module_settings as settings
        import module_teams as teams
        import module_users as users

        app.register_blueprint(main.blueprint, url_prefix="/")
        app.register_blueprint(users.users.blueprint, url_prefix="/users")
        app.register_blueprint(teams.blueprint, url_prefix="/teams")
        app.register_blueprint(sales.blueprint, url_prefix="/sales")
        app.register_blueprint(settings.blueprint, url_prefix="/settings")

        db.init_app(app)
        db.create_all()
        users.users.init()
        db.session.commit()

        # Migration for sqlalchemy
        MIGRATION_DIR = os.path.join('data', 'migrations')  
        migrate = Migrate(app, db, directory=MIGRATION_DIR)
        socketio.init_app(app)
    
    return app


if __name__ == '__main__':
    app = create_app(debug=True)
    socketio.init_app(app)
    socketio.run(app, port=5000, host='0.0.0.0')