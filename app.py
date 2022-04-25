from flask import Flask, render_template, request, jsonify, redirect, url_for

import settings
import datahandler
import json

app = Flask(__name__)
datahandler.init()

@app.route('/')
def ranking():  # put application's code here
    return render_template('ranking.html')

@app.route('/infos')
def infos():  # put application's code here
    infos = datahandler.get_Infos()
    return render_template('infos.html', infos = infos)

@app.route('/admin/')
def admin():
    return render_template('admin.html')

@app.route('/admin/theke')
def adminTheke():
    topList = datahandler.get_List()
    teams = datahandler.get_Teams()
    return render_template('admin_theke.html', topList = topList, teams = teams)

@app.route('/admin/infos')
def adminInfos():
    infos = datahandler.get_Infos()
    return render_template('admin_info.html', infos = infos)

@app.route('/api/addInfo', methods=['POST'])
def api_addInfo():
    title = request.form.get("title")
    content = request.form.get("content")
    if (title and content):
        datahandler.add_Info(title, content)
    print(title)
    print(content)

    return redirect(url_for('infos'))

@app.route('/api/beer', methods=['POST'])
def api_beer():
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

    return render_template('index.html')


@app.route('/api/getRanking')
def getRanking():  # put application's code here
    topList =datahandler.get_List(True)
    return json.dumps(topList)

if __name__ == '__main__':
    app.run(debug=settings.debug, port=settings.port)
