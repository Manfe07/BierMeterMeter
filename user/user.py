from flask import Blueprint, render_template, Flask, request, jsonify, redirect, url_for, session, flash
import user.datahandler as datahandler

datahandler.init()

user = Blueprint('user', __name__,  template_folder='templates')

def addButtons(buttonList : dict):
    buttonList['3'].append({
        'text' : "Benutzer hinzufügen",
        'class' : "btn btn-danger",
        'site' : 'user.add_user'
    })
    buttonList['3'].append({
        'text' : "Benutzer verwalten",
        'class' : "btn btn-danger",
        'site' : 'user.manageUsers'
    })
    return buttonList

@user.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login = request.form
        userName = login['username']
        password = login['password']

        signedIn, permission = datahandler.verify(userName,password)
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
        return render_template('user/login.html')

@user.route('/logout')
def logout():
    session['logged_in'] = False
    session['permission'] = 0
    session['user_name'] = None
    return redirect(url_for('ranking'))


@user.route('/addUser', methods=['POST','GET'])
def add_user():
    if session.get("logged_in") and session.get("permission") >= 2:
        if request.method == 'POST':
            login = request.form

            userName = login['username']
            password = login['password']
            email = login['email']
            permission = login['permission']
            if datahandler.add_User(userName,password,permission,email):
                return redirect(url_for('admin'))
            else:
                flash("Error creating User " + userName)
                return redirect(url_for('user.add_user'))
        elif request.method == 'GET':
            return render_template('user/addUser.html')
    else:
        return redirect(url_for('ranking'))


@user.route('/manageUser', methods=['POST','GET'])
def manageUsers():
    if session.get("logged_in") and session.get("permission") >= 2:
        if request.method == 'POST':
            return redirect(url_for('user.manageUsers'))
        elif request.method == 'GET':
            return render_template('user/manageUsers.html',users = datahandler.getUsers())
    else:
        return redirect(url_for('ranking'))
