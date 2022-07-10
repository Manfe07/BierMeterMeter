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
        return render_template('admin.html', user = user)
    else:
        return redirect(url_for('login'))

@app.route('/admin/theke')
def adminTheke():
    if session.get("logged_in") and session.get("permission") >= 1:
        teams = datahandler.get_Teams()
        return render_template('admin_theke.html', teams = teams)
    else:
        return redirect(url_for('login'))

@app.route('/admin/infos')
def adminInfos():
    if session.get("logged_in") and session.get("permission") >= 2:
        infos = datahandler.get_Infos()
        return render_template('admin_info.html', infos = infos)
    else:
        return redirect(url_for('login'))

@app.route('/admin/teams')
def adminTeams():
    if session.get("logged_in") and session.get("permission") >= 2:
        teams = datahandler.get_Teams()
        return render_template('admin_teams.html', teams = teams)
    else:
        return redirect(url_for('login'))


@app.route('/api/addInfo', methods=['POST'])
def api_addInfo():
    if session.get("logged_in") and session.get("permission") >= 2:
        title = request.form.get("title")
        content = request.form.get("content")
        if (title and content):
            datahandler.add_Info(title, content)
        return redirect(url_for('adminInfos'))

    else:
        return redirect(url_for('login'))


@app.route('/api/deleteInfo', methods=['POST'])
def api_deleteInfo():
    if session.get("logged_in") and session.get("permission") >= 2:
        request_data = request.get_json()
        if 'id' in request_data:
            id = request_data["id"]
            datahandler.delete_Info(id)

        return redirect(url_for('adminInfos'))
    else:
        return redirect(url_for('login'))

@app.route('/api/deleteTeam', methods=['POST'])
def api_deleteTeam():
    if session.get("logged_in") and session.get("permission") >= 2:
        request_data = request.get_json()
        if 'id' in request_data:
            id = request_data["id"]
            datahandler.delete_Team(id)

        return redirect(url_for('adminTeams'))
    else:
        return redirect(url_for('login'))


@app.route('/api/addTeam', methods=['POST'])
def api_addTeam():
    if session.get("logged_in") and session.get("permission") >= 2:
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
    if session.get("logged_in") and session.get("permission") >= 1:
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