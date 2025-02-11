from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from database import db

import datetime
from passlib.hash import sha256_crypt
import sys

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.VARCHAR(100), nullable=False, unique=True)
  password = db.Column(db.VARCHAR(200), nullable=False)
  email = db.Column(db.VARCHAR(200), nullable=False)
  permission = db.Column(db.Integer, server_default= "0")
  last_login = db.Column(db.DateTime(timezone=True),
                          server_default=func.now())


def init():  
  try:
    # If no user exist create default admin
    print("initUserDB")
    if db.session.query(User).first() is None:
        add_User('admin','admin',3,"mail@mail.com")

  except Exception as e:
    print(e)

  try:
    return 0

#  except Error as e:
#    print(e)
#    return -2

  except Exception as e:
    print(e)
    return -1

#  finally:
#    if con:
#     con.close()
def check_User(username):
        try:
                return  db.session.query(User).where(User.username == username).first() is not None
        except:
               return False

def add_User(username, password, permission, email = None):
        
        
        hash = sha256_crypt.hash(password)
        if not check_User(username):
                newUser = User(
                       username = username,
                       password = hash,
                       permission = permission,
                       email = email
                )
                db.session.add(newUser)
                db.session.commit()
                return 1
        else:
                return -1       #-1 == User exists

def verify(username, password):
        if check_User(username):
                user = db.session.query(User).where(User.username == username).first()
                hash = user.password
                if sha256_crypt.verify(password, hash):
                        updateLastLogin(user)
                        return True, user.permission, user
                else:
                        return False, 0, None
        else:
                return False, 0, None


def updateLastLogin(user):
        try:
                now = datetime.datetime.now().timestamp()
                user.last_login = now
                db.session.commit
        except Exception as e:
                print(e)


def getUsers():
        users = db.session.query(User).order_by(User.username.asc())

        return users


def deleteUser(id):
        try:
                user = db.session.query(User).where(User.id == id).first()
                db.session.delete(user)
                db.session.commit()

        except Exception as e:
               print(e)


if __name__ == "__main__":
        init()
        if(sys.argv[1] and sys.argv[2]):
                name = sys.argv[1]
                pw = sys.argv[2]
                add_User(name, pw, 3)

                print("Created User")
                print("name : " + name)
                print("password : " + pw)