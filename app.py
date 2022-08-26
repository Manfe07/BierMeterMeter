import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from cashRegister import cashRegister
from items import items
from teams import teams
from info import info
from user import user
import settings
import datahandler
import json

from datetime import timedelta
from pprint import pprint
import logging

buttonList = {'1':[],'2':[],'3':[]}
buttonList = cashRegister.addButtons(buttonList)
buttonList = items.addButtons(buttonList)
buttonList = teams.addButtons(buttonList)
buttonList = info.addButtons(buttonList)
buttonList = user.addButtons(buttonList)

app = Flask(__name__)
app.permanent_session_lifetime = settings.session_lifetime
datahandler.init()

app.register_blueprint(cashRegister.cashRegister, url_prefix="/kasse")
app.register_blueprint(items.items, url_prefix="/artikel")
app.register_blueprint(teams.teams, url_prefix="/teams")
app.register_blueprint(info.info, url_prefix="/info")
app.register_blueprint(user.user, url_prefix="/user")

#logging.basicConfig(filename='flask.log', level=logging.DEBUG)
#logging.basicConfig(filename='flask.log',
#    level=logging.DEBUG,
#    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.route('/')
def ranking():  # put application's code here
    ranking_list = cashRegister.datahandler.get_List_By_Date()
    if settings.hideRanking:
        return render_template('secret.html')
    else:
        return render_template('ranking.html', ranking_list = ranking_list)

@app.route('/tv')
def ranking_TV():  # put application's code here
    if settings.hideRanking:
        return render_template('secret.html')
    else:
        return render_template('ranking_tv.html')


@app.route('/admin')
def admin():
    if session.get("logged_in") and session.get("permission") >= 1:
        user = {
            'name': session.get('user_name'),
            'permission': session.get('permission'),
        }
        return render_template('admin.html', user = user, buttonList = buttonList)
    else:
        return redirect(url_for('user.login'))



@app.route('/api/getRanking')
def getRanking():  # put application's code here
    topList = cashRegister.datahandler.get_List_By_Date()
    return json.dumps(topList)

@app.route('/api/getRanking_TV')
def getRanking_TV():  # put application's code here
    topList = cashRegister.datahandler.get_List_for_Today()
    return json.dumps(topList)




if __name__ == '__main__':
    app.secret_key = settings.secret_key
    app.run(debug=settings.debug, port=settings.port, host="0.0.0.0")