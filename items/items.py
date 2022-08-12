from flask import Blueprint, render_template, Flask, request, jsonify, redirect, url_for, session, flash
import items.datahandler as datahandler

datahandler.init()

def addButtons(buttonList : dict):
    buttonList['2'].append({
        'text' : "Artikel verwalten",
        'class' : "btn btn-warning",
        'site' : 'items.manage'
    })
    return buttonList


items = Blueprint('items', __name__,
                        template_folder='templates')


@items.route('/', methods=['GET'])
@items.route('/verwalten', methods=['GET'])
def manage():
    if session.get("logged_in") and session.get("permission") >= 2:
        return render_template("items/manage.html", itemlist = datahandler.get_Items())
    else:
        return redirect(url_for('user.login'))

@items.route('/addItem', methods=['GET', 'POST'])
def addItem():
    if session.get("logged_in") and session.get("permission") >= 2:
        if request.method == 'POST':
            form = request.form
            name = form["name"]
            price = float(form["price"])
            editor = session.get("user_name")
            datahandler.addItem(name, price=price, editor=editor)

        return redirect(url_for('items.manage'))
    else:
        return redirect(url_for('user.login'))

@items.route('/deleteItem', methods=['POST'])
def deleteItem():
    if session.get("logged_in") and session.get("permission") >= 2:
        request_data = request.get_json()
        if 'id' in request_data:
            id = request_data["id"]
            datahandler.deleteItem(id)

        return redirect(url_for('item.manage'))
    else:
        return redirect(url_for('user.login'))

