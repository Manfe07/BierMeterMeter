from flask import Blueprint, render_template, Flask, request, jsonify, redirect, url_for, session, flash
import info.datahandler as datahandler

datahandler.init()

info = Blueprint('info', __name__,  template_folder='templates')

def addButtons(buttonList : dict):
    buttonList['2'].append({
        'text' : "Infos verwalten",
        'class' : "btn btn-primary",
        'site' : 'info.manage'
    })
    return buttonList

@info.route('/')
def infos():  # put application's code here
    infos = datahandler.get_Infos()
    return render_template('info/infos.html', infos = infos)


@info.route('/manage')
def manage():
    if session.get("logged_in") and session.get("permission") >= 2:
        infos = datahandler.get_Infos()
        return render_template('info/manage.html', infos = infos)
    else:
        return redirect(url_for('user.login'))


@info.route('/api/addInfo', methods=['POST'])
def addInfo():
    if session.get("logged_in") and session.get("permission") >= 2:
        title = request.form.get("title")
        content = request.form.get("content")
        if (title and content):
            datahandler.add_Info(title, content)
        return redirect(url_for('info.manage'))

    else:
        return redirect(url_for('user.login'))


@info.route('/api/deleteInfo', methods=['POST'])
def deleteInfo():
    if session.get("logged_in") and session.get("permission") >= 2:
        request_data = request.get_json()
        if 'id' in request_data:
            id = request_data["id"]
            datahandler.delete_Info(id)

        return redirect(url_for('info.manage'))
    else:
        return redirect(url_for('user.login'))
