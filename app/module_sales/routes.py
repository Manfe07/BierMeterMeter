from flask import Blueprint, render_template, Flask, request, jsonify, redirect, url_for, session, flash
from module_users.datahandler import User
from module_users.users import getSessionUser
from module_teams.models import Team

from . import blueprint, logger
from .models import db, Item, ItemGroup, Order, OrderItem


def init():
    return True

@blueprint.route('/', methods=['GET'])
def overviewItems():
    if session.get('permission', 0) >= 1:
        itemGroups = db.session.query(ItemGroup).order_by(ItemGroup.name)
        items = db.session.query(Item).order_by(Item.name)
        users = {}
    
        return render_template('sales/overviewItems.html', itemGroups=itemGroups, items=items, users=users)
    else:
        return redirect(url_for('index'))

@blueprint.route('/viewOrders', methods=['GET'])
def overviewOrders():
    if session.get('permission', 0) >= 1:
        #orders = db.session.query(Order)
        orders = db.session.query(Order,Team).join(Team)
    
        return render_template('sales/overviewOrders.html', orders=orders)
    else:
        return redirect(url_for('index'))


@blueprint.route('/cashRegister', methods=['GET'])
def cashRegister():
    if session.get('permission', 0) >= 1:
    
        itemGroups = db.session.query(ItemGroup)

        return render_template('sales/cashRegister.html', itemGroups=itemGroups)
    else:
        return redirect(url_for('index'))


@blueprint.route('/updateItemGroup', methods=['GET','POST'])
def updateItemGroup():
    if session.get('permission', 0) >= 2:
        if request.method == 'POST':
            form = request.form
            id = int(form.get("id",0))
            try:
                if id != 0:
                    group = ItemGroup.query.filter_by(id=id).first()
                    group.name = form.get("name",group.name)
                    group.description = form.get("description",group.description)
                    group.color = form.get("color",group.color)
                    group.state = form.get("state",group.state)
            
                else:
                    group = ItemGroup(
                        name = form.get("name"),
                        description = form.get("description",""),
                        color = form.get("color","#006329"),
                        state = form.get("state",0),
                    )
                    db.session.add(group)

                db.session.commit()
                return redirect(url_for('sales.overviewItems'))


            except Exception as e:
                print(e)
                flash("Error updating itemGroup " + form["name"] )
            return redirect(url_for('sales.overviewItems'))
            
        elif request.method == 'GET':
            return redirect(url_for('sales.overviewItems'))
    else:
        return redirect(url_for('index'))


@blueprint.route('/updateItem', methods=['GET','POST'])
def updateItem():
    if session.get('permission', 0) >= 2:
        if request.method == 'POST':
            form = request.form
            id = int(form.get("id",0))
            try:
                if id != 0:
                    item = Item.query.filter_by(id=id).first()
                    item.name = form.get("name",item.name)
                    item.description = form.get("description",item.description)
                    item.price = form.get("price",item.price)
                    item.state = form.get("state",item.state)
                    item.groupId = form.get("groupId",item.groupId)
                    item.changedBy = session.get('user_id', None)
            
                else:

                    item = Item(
                        name = form.get("name"),
                        description = form.get("description",None),
                        price = form.get("price",0.0),
                        state = form.get("state", 0),
                        groupId = form.get("groupId",0),
                        changedBy = session.get('user_id', None)
                    )
                    db.session.add(item)

                db.session.commit()
                return redirect(url_for('sales.overviewItems'))


            except Exception as e:
                print(e)
                flash("Error updating itemGroup " + form["name"] )
            return redirect(url_for('sales.overviewItems'))
            
        elif request.method == 'GET':
            return redirect(url_for('sales.overviewItems'))
    else:
        return redirect(url_for('index'))
    


    if session.get('permission', 0) >= 2:
        if request.method == 'POST':
            form = request.form
            newItem = Item(
                name = form.get("name"),
                description = form.get("description",None),
                price = form.get("price",0.0),
                state = form.get("state", 0),
                groupId = form.get("groupId",0),
                changedBy = session.get('user_id', None)
            )
            print(newItem)
            db.session.add(newItem)
            db.session.commit()

            return redirect(url_for('sales.overview'))

        elif request.method == 'GET':
            return redirect(url_for('sales.overview'))
    else:
        return redirect(url_for('index'))


@blueprint.route('/getGroups', methods=['GET'])
def getGroups():    
    if session.get('permission', 0) >= 0:
    
        itemGroups = db.session.query(ItemGroup)

        groupData = {}
        for group in itemGroups:
            itemData = []
            for item in group.items:
                itemData.append(
                    {
                        "id" : item.id,
                        "name" : item.name,
                        "description" : item.description,
                        "price" : item.price,
                        "state" : item.state,
                        "changedBy" : item.changedBy,
                    }
            )
            groupData[group.id] = {
                "id" : group.id,
                "name" : group.name,
                "description" : group.description,
                "color" : group.color,
                "state" : group.state,
                "items" : itemData,
            }
        response = jsonify(groupData)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        return None

@blueprint.route('/createOrder', methods=['POST'])
def createOrder():    
    if session.get('permission', 1) >= 0:
        data = request.json
        logger.debug(data)
        

        order = Order(
            teamId = data['team_id'],
            cashierId = session['user_id'],
            sum = data['sum'],
            itemCount = data['itemCount']
        )

        db.session.add(order)
        db.session.commit()

        itemCount = 0
        for item in data['items']:
            orderItem = OrderItem(
                orderId=order.id,
                itemId=item['itemId'],
                quantity=item['amount'],
                price=item['price'],
                sum=item['sum']
            )
            db.session.add(orderItem)
        db.session.commit()
        

        return {'success': True }
    else:
        return None


@blueprint.route('/getOrders', methods=['GET'])
def viewOrders():
    orders = db.session.query(Order,Team).join(Team)
    data = []
    for order, team in orders:
        items= []
        for item in order.items:
            items.append({
                'id': item.id,
                'itemId': item.itemId,
                'quantity': item.quantity,
                'price': item.price,
                'sum': item.sum
            })
        data.append({
            'id': order.id,
            'sum': order.sum,
            'teamId': team.id,
            'teamName': team.name,
            'cashierId': order.cashierId,
            'created_at': order.created_at,
            'items': items,
            'itemCount': order.itemCount
        })
        
    return data

@blueprint.route('/getItems', methods=['GET'])
def getItems():    
    if session.get('permission', 0) >= 0:

        items = db.session.query(Item)

        data = {}
        for item in items:
            data[item.id] = {
                "id" : item.id,
                "name" : item.name,
                "description" : item.description,
                "price" : item.price,
                "state" : item.state,
                "groupId" : item.groupId,
                "changedBy" : item.changedBy,
            }
        response = jsonify(data)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        return None



