from database import db

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from module_teams.models import Team
from module_users.datahandler import User

class ItemGroup(db.Model):
  __tablename__ = 'itemGroup'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.VARCHAR(100), nullable=False)
  description = db.Column(db.VARCHAR(100), nullable=True)
  color = db.Column(db.VARCHAR(10), nullable=True)
  state = db.Column(db.Integer, server_default= "0")

  items = db.Relationship('Item', backref='item', order_by='item.columns.name.asc()')

class Item(db.Model):
  __tablename__ = 'item'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.VARCHAR(100), nullable=False)
  description = db.Column(db.VARCHAR(100), nullable=True)
  price = db.Column(db.Float, nullable=True)
  state = db.Column(db.Integer, server_default= "0")
  groupId = db.Column(db.Integer, db.ForeignKey('itemGroup.id'))
  changedBy = db.Column(db.Integer, server_default= "0")


  # Relationships
  #itemGroup = db.relationship("Item", back_populates="items")
  #orderItems = db.relationship("OrderItem.id", back_populates="Item")

class Order(db.Model):
  __tablename__ = 'order'
    
  id = db.Column(db.Integer, primary_key=True)
  sum = db.Column(db.Float, nullable=False)
  teamId = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
  cashierId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  created_at = db.Column(db.DateTime(timezone=True),
                          server_default=func.now())
  items = db.Relationship('OrderItem', backref='orderItem', order_by='orderItem.columns.id.asc()')
  itemCount = db.Column(db.Integer, nullable=False)

  # Relationships
  team = db.relationship("Team")
  user = db.relationship("User")


class OrderItem(db.Model):
  __tablename__ = 'orderItem' 

  id = db.Column(db.Integer, primary_key=True)
  orderId = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
  itemId = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
  quantity = db.Column(db.Integer, nullable=False)
  price = db.Column(db.Float, nullable=False)
  sum = db.Column(db.Float, nullable=False)
 
  # Relationships
  order = db.relationship("Order")
  item = db.relationship("Item")