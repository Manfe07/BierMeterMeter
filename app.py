import os

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash

import settings
import datahandler
import user
import json
import logging


app = Flask(__name__)
datahandler.init()
user.init()

#logging.basicConfig(filename='flask.log', level=logging.DEBUG)
logging.basicConfig(filename='flask.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

@app.route('/')
def ranking():  # put application's code here
    return render_template('ranking.html')

@app.route('/tv')
def ranking_TV():  # put application's code here
    return render_template('ranking_tv.html')

@app.route('/infos')
def infos():  # put application's code here
    infos = datahandler.get_Infos()
    return render_template('infos.html', infos = infos)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login = request.form

        userName = login['username']
        password = login['password']

        if user.verify(userName,password):
          session['logged_in'] = True
        else:
          session['logged_in'] = False
          flash('wrong password!')
        return redirect(url_for('admin'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
  session['logged_in'] = False
  return redirect(url_for('ranking'))


@app.route('/admin/addUser', methods=['POST','GET'])
def add_user():
    if session.get("logged_in"):
        if request.method == 'POST':
            login = request.form

            userName = login['username']
            password = login['password']
            email = login['email']
            if user.add_User(userName,password,email):
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
    if session.get("logged_in"):
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))

@app.route('/admin/theke')
def adminTheke():
    if session.get("logged_in"):
        teams = datahandler.get_Teams()
        return render_template('admin_theke.html', teams = teams)
    else:
        return redirect(url_for('login'))

@app.route('/admin/infos')
def adminInfos():
    if session.get("logged_in"):
        infos = datahandler.get_Infos()
        return render_template('admin_info.html', infos = infos)
    else:
        return redirect(url_for('login'))

@app.route('/admin/teams')
def adminTeams():
    if session.get("logged_in"):
        teams = datahandler.get_Teams()
        return render_template('admin_teams.html', teams = teams)
    else:
        return redirect(url_for('login'))


@app.route('/api/addInfo', methods=['POST'])
def api_addInfo():
    if session.get("logged_in"):
        title = request.form.get("title")
        content = request.form.get("content")
        if (title and content):
            datahandler.add_Info(title, content)
        return redirect(url_for('adminInfos'))

    else:
        return redirect(url_for('login'))


@app.route('/api/deleteInfo', methods=['POST'])
def api_deleteInfo():
    if session.get("logged_in"):
        request_data = request.get_json()
        if 'id' in request_data:
            id = request_data["id"]
            datahandler.delete_Info(id)

        return redirect(url_for('adminInfos'))
    else:
        return redirect(url_for('login'))

@app.route('/api/deleteTeam', methods=['POST'])
def api_deleteTeam():
    if session.get("logged_in"):
        request_data = request.get_json()
        if 'id' in request_data:
            id = request_data["id"]
            datahandler.delete_Team(id)

        return redirect(url_for('adminTeams'))
    else:
        return redirect(url_for('login'))


@app.route('/api/addTeam', methods=['POST'])
def api_addTeam():
    if session.get("logged_in"):
        if request.method == 'POST':
            form = request.form
            name = form["name"]
            contactPerson = form["contactPerson"]
            email = form["email"]
            datahandler.add_Team(name, contactPerson=contactPerson, email=email)

            return redirect(url_for('adminTeams'))
        else:
            return redirect(url_for('login'))


@app.route('/api/beer', methods=['POST'])
def api_beer():
    if session.get("logged_in"):
        request_data = request.get_json()

        team = None
        add = False
        remove = False

        if 'add' in request_data:
            add = request_data["add"]

        if 'remove' in request_data:
            remove = request_data["remove"]

        if 'team' in request_data:
            team = request_data["team"]
            datahandler.beer(team, add)
        return render_template('admin_theke.html')

    else:
        return redirect(url_for('login'))


@app.route('/api/getRanking')
def getRanking():  # put application's code here
    topList =datahandler.get_List(True)
    return json.dumps(topList)




if __name__ == '__main__':
    app.secret_key = settings.secret_key
    app.run(debug=settings.debug, port=settings.port, host="0.0.0.0")