from flask import Blueprint, render_template, Flask, request, jsonify, redirect, url_for, session, flash

from . import blueprint, logger
from .models import db, Team, TeamGroup

@blueprint.route('/', methods=['GET'])
def overview():
    teams = Team.query.all()
    teamGroups = TeamGroup.query.all()
    #teams = datahandler.db.session.query(datahandler.Team)
    #result = {}
    #for r in query:
    #   result[r.id] = r.getDict()
    return render_template('teams/manageTeams.html', teams=teams, teamGroups=teamGroups)


@blueprint.route('/deleteTeam', methods=['POST'])
def deleteTeam():
    if request.method == 'POST':
        try:
            data = request.json
            id=data.get("id")
            team = Team.query.get(id)
            db.session.delete(team)
            db.session.commit()
            return {'delteded' : id}
        except Exception as e:
            return {'error': e}

    else:
        return {'error': 0}

@blueprint.route('/updateTeam', methods=['POST', 'GET'])
def updateTeam():
    if session.get('permission', 0) >= 2:
        if request.method == 'POST':
            form = request.form
            id = int(form.get("id",0))
            try:
                if id != 0:
                    team = Team.query.filter_by(id=id).first()
                    team.name = form.get("name_long","")
                    team.nameShort = form.get("name_short",None)
                    team.contact = form.get("contact",None)
                    team.phoneNumber = form.get("phone", None)
                    team.state = form.get("state", None)
                    team.groupId = int(form.get("groupId",0))
                    db.session.commit()
                else:
                    newTeam = Team(
                        name = form["name_long"],
                        nameShort = form.get("name_short",None),
                        contact = form.get("contact",None),
                        phoneNumber = form.get("phone", None),
                        state = form.get("state", 1),
                        groupId = int(form.get("groupId",0))
                        )
                    db.session.add(newTeam)
                    db.session.commit()
                
                return redirect(url_for('teams.overview'))


            except Exception as e:
                logger.debug(e)
                flash("Error updating team " + form["name_long"] )
            return redirect(url_for('teams.overview'))
            
        elif request.method == 'GET':
            return redirect(url_for('teams.overview'))
    else:
        return redirect(url_for('index'))

@blueprint.route('/updateTeamGroup', methods=['POST', 'GET'])
def updateTeamGroup():
    if session.get('permission', 0) >= 2:
        if request.method == 'POST':
            form = request.form
            id = int(form.get("id",0))
            try:
                if id != 0:
                    group = TeamGroup.query.filter_by(id=id).first()
                    group.name = form.get("name",group.name)
                    group.description = form.get("description",group.description)
                    group.color = form.get("color",group.color)
                    group.state = form.get("state",group.state)
                    db.session.commit()
            
                else:
                    group = TeamGroup(
                        name = form.get("name"),
                        description = form.get("description",""),
                        color = form.get("color","#006329"),
                        state = form.get("state",0),
                    )
                    db.session.add(group)
                    db.session.commit()

                return redirect(url_for('teams.overview'))


            except Exception as e:
                logger.debug(e)
                flash("Error updating itemGroup " + form["name"] )
            return redirect(url_for('teams.overview'))
            
        elif request.method == 'GET':
            return redirect(url_for('teams.overview'))
    else:
        return redirect(url_for('index'))


@blueprint.route('/deleteTeamGroup', methods=['POST'])
def deleteTeamGroup():
    if request.method == 'POST':
        try:
            data = request.json
            id=data.get("id")
            teamGroup = TeamGroup.query.get(id)
            db.session.delete(teamGroup)
            db.session.commit()
            return {'delteded' : id}
        except Exception as e:
            return {'error': e}

    else:
        return {'error': 0}



@blueprint.route('/getTeams', methods=['GET'])
def getTeams():    
    if session.get('permission', 0) >= 1:

        teams = db.session.query(Team)
        data = {}
        for team in teams:
            data[team.id] = {
                "id" : team.id,
                "name" : team.name,
                "nameShort" : team.nameShort,
                "contact" : team.contact,
                "state" : team.state,
                "phone" : team.phoneNumber,
                "created_at" : team.created_at,
                "group_id" : team.groupId
            }
        return jsonify(data)
    else:
        return None

@blueprint.route('/getGroups', methods=['GET'])
def getGroups():    
    if session.get('permission', 0) >= 0:
    
        teamGroups = db.session.query(TeamGroup)

        groupData = {}
        for group in teamGroups:
            teamData = []
            for team in group.teams:
                teamData.append(
                    {
                        "id" : team.id,
                        "name" : team.name,
                        "nameShort" : team.nameShort,
                        "contact" : team.contact,
                        "state" : team.state,
                        "phone" : team.phoneNumber,
                        "created_at" : team.created_at,
                    }
            )
            groupData[group.id] = {
                "id" : group.id,
                "name" : group.name,
                "description" : group.description,
                "color" : group.color,
                "state" : group.state,
                "teams" : teamData,
            }
        response = jsonify(groupData)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        return None
