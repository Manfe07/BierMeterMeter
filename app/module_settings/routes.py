from flask import Blueprint, render_template, Flask, request, jsonify, redirect, url_for, session, flash
from module_users.datahandler import User
from module_users.users import getSessionUser
from module_teams.models import Team

from . import blueprint, logger
from .models import db, Setting
from database import socketio


@blueprint.route('/', methods=['GET'])
def overviewSettings():
    if session.get('permission', 0) >= 3:
        try:
            settings = Setting.query.all()
        except Exception as e:
            print(e)
        return render_template('settings/overviewSettings.html', settings=settings)
    else:
        return redirect(url_for('users.login'))


@blueprint.route('/updateSetting', methods=['POST','GET'])
def updateSetting():
    if request.method == 'POST':
        response = {}
        response['success'] = False
        if session.get('permission', 0) >= 2:
            form = request.form
            name = form.get("name",None)
            value = form.get("value",None)    
            if((name != None) & (value != None)):
                setting = Setting.query.filter_by(name=name).first()
                
                if session.get('permission', 0) >= setting.permission:
                    setting.value = value
                    db.session.commit()
                    response['success'] = True

                response['setting'] = {
                    'id' : setting.id,
                    'name' : setting.name,
                    'value' : setting.value,
                    'permission' : setting.permission,
                }
            emit('newData', broadcast=True)
    logger.debug(response)
    return redirect(url_for('settings.overviewSettings'))
        