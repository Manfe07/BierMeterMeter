from flask import Blueprint, render_template, Flask, request, jsonify, redirect, url_for, session, flash
from flask_socketio import emit, join_room, leave_room
import module_teams
import module_sales
import module_settings
from database import db, socketio
from sqlalchemy import func, text

import datetime

from . import blueprint, logger

@blueprint.route('/',methods = ['GET'])
def index():
    return render_template('main/index.html')


@blueprint.route('/getData',methods = ['GET'])
def getData():
    data = {
        'indexShowTable': False,
        'teams':[]
    }
    indexShowTable = module_settings.models.getSettingElseCreate("indexShowTable",True,permission=2)
    

    # Get Teams as list, get add names in ranking
    Team = module_teams.models.Team
    teams = db.session.query(Team)
    teamsList = {}
    for team in teams:
        teamsList[team.id] = team.name

    ## Create Ranking table
    indexTableItemId = module_settings.models.getSettingElseCreate("indexTableItemId",1,permission=3)

    data['itemName'] = db.session.query(module_sales.models.Item).filter_by(id=indexTableItemId).first().name

    Order = module_sales.models.Order
    OrderItem = module_sales.models.OrderItem
    orders = db.session.query(OrderItem,Order,func.sum(OrderItem.quantity).label('total_quantity')).filter_by(itemId=indexTableItemId).join(Order).group_by(Order.teamId).order_by(text('total_quantity DESC'))
    #logger.debug(orders.statement.columns.keys())
    #data['dev'] = orders.statement.columns.keys()
    for row in orders.all():
        data['teams'].append({
            'team': teamsList[row[1].teamId],
            'amount': row[2]
        })
    
    # Parse Setting to show Ranking Table
    if(indexShowTable.lower() in ['true', '1', 'yes']):
        data['indexShowTable'] = True
    else:
        data['indexShowTable'] = False

    return jsonify(data)



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