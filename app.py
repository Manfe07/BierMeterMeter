import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from cashRegister import cashRegister
from items import items
from teams import teams
from info import info
import settings
import datahandler
import user
import json

from pprint import pprint
import logging

buttonList = {'1':[],'2':[],'3':[]}
buttonList = cashRegister.addButtons(buttonList)
buttonList = items.addButtons(buttonList)
buttonList = teams.addButtons(buttonList)
buttonList = info.addButtons(buttonList)

app = Flask(__name__)
datahandler.init()
user.init()

app.register_blueprint(cashRegister.cashRegister, url_prefix="/kasse")
app.register_blueprint(items.items, url_prefix="/artikel")
app.register_blueprint(teams.teams, url_prefix="/teams")
app.register_blueprint(info.info, url_prefix="/info")

#logging.basicConfig(filename='flask.log', level=logging.DEBUG)
#logging.basicConfig(filename='flask.log',
#    level=logging.DEBUG,
#    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.route('/')
def ranking():  # put application's code here
    return render_template('ranking.html')

@app.route('/tv')
def ranking_TV():  # put application's code here
    return render_template('ranking_tv.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login = request.form
        userName = login['username']
        password = login['password']

        signedIn, permission = user.verify(userName,password)
        if signedIn:
            session['logged_in'] = True
            session['permission'] = permission
            session['user_name'] = userName
        else:
            session['logged_in'] = False
            session['permission'] = 0
            session['user_name'] = None
            flash('wrong password!')
        return redirect(url_for('admin'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['permission'] = 0
    session['user_name'] = None
    return redirect(url_for('ranking'))


@app.route('/admin/addUser', methods=['POST','GET'])
def add_user():
    if session.get("logged_in") and session.get("permission") >= 2:
        if request.method == 'POST':
            login = request.form

            userName = login['username']
            password = login['password']
            email = login['email']
            permission = login['permission']
            if user.add_User(userName,password,permission,email):
                return redirect(url_for('admin'))
            else:
                flash("Error creating User " + userName)
                return redirect(url_for('add_user'))
        elif request.method == 'GET':
            return render_template('admin_addUser.html')
    else:
        return redirect(url_for('ranking'))


@app.route('/admin')
def admin():
    if session.get("logged_in") and session.get("permission") >= 1:
        user = {
            'name': session.get('user_name'),
            'permission': session.get('permission'),
        }
        return render_template('admin.html', user = user, buttonList = buttonList)
    else:
        return redirect(url_for('login'))



@app.route('/api/getRanking')
def getRanking():  # put application's code here
    topList = cashRegister.datahandler.get_List()
    return json.dumps(topList)




if __name__ == '__main__':
    app.secret_key = settings.secret_key
    app.run(debug=settings.debug, port=settings.port, host="0.0.0.0")