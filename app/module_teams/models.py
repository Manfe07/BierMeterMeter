from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import db


class TeamGroup(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.VARCHAR(100), nullable=False)
  description = db.Column(db.VARCHAR(100), nullable=True)
  color = db.Column(db.VARCHAR(10), nullable=True)
  state = db.Column(db.Integer, server_default= "0")
  teams = db.Relationship('Team', backref='team', order_by='team.columns.name.asc()')


class Team(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.VARCHAR(100), nullable=False)
  nameShort = db.Column(db.VARCHAR(30), nullable=False)
  contact = db.Column(db.VARCHAR(100), nullable=True)
  phoneNumber = db.Column(db.VARCHAR(100), nullable=True)
  state = db.Column(db.Integer, server_default= "0")
  groupId = db.Column(db.Integer, db.ForeignKey('team_group.id'))
  created_at = db.Column(db.DateTime(timezone=True),
                          server_default=func.now())

  def __repr__(self):
    return f'<Team {self.name}>'
  