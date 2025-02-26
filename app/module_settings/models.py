from database import db

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

class Setting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(100), nullable=False)
    permission = db.Column(db.Integer, nullable=False)  

    def __repr__(self):
      return f'<Setting {self.name}: {self.value}>'





def getSettingElseCreate(name, default_value, permission = 3):
  response = Setting.query.filter_by(name=name).first()
  if response is not None:
    return response.value
  else:
    db.session.add(
      Setting(
        name = name,
        value = str(default_value),
        permission = permission,
      )
    ) 
    db.session.commit()
    return default_value
