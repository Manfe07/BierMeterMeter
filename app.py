from flask import Flask, render_template, request, jsonify

import datahandler
import json

app = Flask(__name__)

@app.route('/')
def ranking():  # put application's code here
    return render_template('ranking.html')

@app.route('/admin/')
def admin():
    return render_template('admin.html')

@app.route('/admin/theke')
def adminTheke():
    topList = datahandler.get_List()
    return render_template('admin_theke.html', topList = topList)

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

    print(request_data)

    return render_template('index.html')


@app.route('/api/getRanking')
def getRanking():  # put application's code here
    topList =datahandler.get_List(True)
    return json.dumps(topList)

if __name__ == '__main__':
    app.run(debug=True)
