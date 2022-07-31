from flask import Blueprint, render_template, Flask, request, jsonify, redirect, url_for, session, flash
import teams.datahandler as datahandler

datahandler.init()

teams = Blueprint('teams', __name__,  template_folder='templates')

def addButtons(buttonList : dict):
    buttonList['2'].append({
        'text' : "Teams verwalten",
        'class' : "btn btn-primary",
        'site' : 'teams.manage'
    })

    return buttonList

@teams.route('/')
@teams.route('/verwalten')
def manage():
    if session.get("logged_in") and session.get("permission") >= 2:
        teams = datahandler.get_Teams()
        return render_template('teams/manage.html', teams = teams)
    else:
        return redirect(url_for('user.login'))

@teams.route('/deleteTeam', methods=['POST'])
def deleteTeam():
    if session.get("logged_in") and session.get("permission") >= 2:
        request_data = request.get_json()
        if 'id' in request_data:
            id = request_data["id"]
            datahandler.delete_Team(id)

        return redirect(url_for('teams.manage'))
    else:
        return redirect(url_for('user.login'))


@teams.route('/addTeam', methods=['POST', 'GET'])
def addTeam():
    if session.get("logged_in") and session.get("permission") >= 2:
        if request.method == 'POST':
            form = request.form
            name = form["name"]
            contactPerson = form["contactPerson"]
            email = form["email"]
            datahandler.add_Team(name, contactPerson=contactPerson, email=email)

            return redirect(url_for('teams.manage'))
        else:
            return redirect(url_for('user.login'))
