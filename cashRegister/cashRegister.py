from flask import Blueprint, render_template, Flask, request, jsonify, redirect, url_for, session, flash
import cashRegister.datahandler as datahandler
import items.datahandler as itemlist
import teams.datahandler as teamlist

datahandler.init()

cashRegister = Blueprint('cashRegister', __name__, template_folder='templates')



def addButtons(buttonList : dict):
    buttonList['1'].append({
        'text' : "Kasse",
        'class' : "btn btn-success btn-lg",
        'site' : 'cashRegister.teams'
    })
    buttonList['1'].append({
        'text' : "Abrechungen",
        'class' : "btn btn-info",
        'site' : 'cashRegister.bills'
    })
    buttonList['2'].append({
        'text' : "Käufe verwalten",
        'class' : "btn btn-warning",
        'site' : 'cashRegister.history'
    })
    return buttonList


@cashRegister.route('/', methods=['GET', 'POST'])
@cashRegister.route('/teams', methods=['GET', 'POST'])
def teams():
    if session.get("logged_in") and session.get("permission") >= 1:
        teams = teamlist.get_Teams()
        return render_template('cashRegister/teams.html', teams = teams)
    else:
        return redirect(url_for('user.login'))

@cashRegister.route('/items', methods=['GET', 'POST'])
def items():
    if session.get("logged_in") and session.get("permission") >= 1:
        if not (request.args.get('team_id') == 0):
            team = {
                'team_name' : request.args.get('team_name'),
                'team_id' : int(request.args.get('team_id'))
            }
        else:
            team = {
                'team_name' : "Ohne Mannschaft",
                'team_id' : None
            }
        return render_template('cashRegister/items.html', team=team, itemlist = itemlist.get_Items(asGroup=True))
    else:
        return redirect(url_for('user.login'))

@cashRegister.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if session.get("logged_in") and session.get("permission") >= 1:
        request_data = request.get_json()
        if 'basket' in request_data:
            _data = {
                'basket' : request_data["basket"],
                'team_id' : request_data["team_id"],
                'team_name' : request_data["team_name"],
                'cash' : request_data["cash"],
                'user' : session.get("user_name")
            }
            datahandler.add_Order(_data)

        return redirect(url_for('cashRegister/teams'))
    else:
        return redirect(url_for('user.login'))

@cashRegister.route('/verlauf')
def history():
    if session.get("logged_in") and session.get("permission") >= 2:
        history = datahandler.get_OrderHistory()
        return render_template('cashRegister/history.html', history = history)
    else:
        return redirect(url_for('user.login'))

@cashRegister.route('/abrechnung')
def bills():
    if session.get("logged_in") and session.get("permission") >= 1:
        bills = datahandler.get_TeamBills(True)
        return render_template('cashRegister/bills.html', bills = bills)
    else:
        return redirect(url_for('user.login'))

@cashRegister.route('/deleteOrder', methods=['POST'])
def deleteOrder():
    if session.get("logged_in") and session.get("permission") >= 2:
        request_data = request.get_json()
        if 'id' in request_data:
            id = request_data["id"]
            datahandler.delete_Order(id)
        return redirect(url_for('cashRegister.history'))

    else:
        return redirect(url_for('user.login'))

