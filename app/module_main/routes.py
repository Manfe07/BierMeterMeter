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
        'days':[]
    }
    indexShowTable = module_settings.models.getSettingElseCreate("indexShowTable",True,permission=2)

    # Get Teams as list, get add names in ranking
    Team = module_teams.models.Team
    teams = db.session.query(Team)
    teamsList = {}
    for team in teams:
        teamsList[team.id] = team.name

    # Create Ranking table
    indexTableItemId = module_settings.models.getSettingElseCreate("indexTableItemId",1,permission=3)
    tableShowOnlyToday = module_settings.models.getSettingElseCreate("tableShowOnlyToday",True,permission=2)

    Item = module_sales.models.Item
    Order = module_sales.models.Order
    OrderItem = module_sales.models.OrderItem

    ## ToDo: from datetime import timedelta
    orders = []
    data['itemName'] = db.session.query(Item).filter_by(id=indexTableItemId).first().name
    if tableShowOnlyToday == "True":
        orders = db.session.query(OrderItem,Order,func.sum(OrderItem.quantity).label('total_quantity'))\
            .filter(OrderItem.itemId==indexTableItemId)\
            .join(Order)\
            .filter(func.date(Order.created_at) == datetime.date.today())\
            .group_by(
                Order.teamId,
                func.date(Order.created_at)
                )\
            .order_by(
                func.date(Order.created_at),
                text('total_quantity DESC')
            )
            
    else:
        orders = db.session.query(OrderItem,Order,func.sum(OrderItem.quantity).label('total_quantity'))\
            .filter(OrderItem.itemId==indexTableItemId)\
            .join(Order)\
            .group_by(
                Order.teamId,
                func.date(Order.created_at)
                )\
            .order_by(
                func.date(Order.created_at),
                text('total_quantity DESC')
            )
    logger.debug(orders.all())
    days = {}
    for row in orders.all():
        entry = {
            'team': teamsList[row[1].teamId],
            'amount': row[2],
            'date' : row[1].created_at.strftime("%d.%m.%Y"),
        }
        if days.get(entry["date"]):
            days[entry["date"]].append(entry)
        else:
            days[entry["date"]] = []
            days[entry["date"]].append(entry)
    data['days'] = days
    logger.debug(days)
    
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