from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from sqlalchemy.orm import relationship

DataBase = declarative_base()

#здесь добавим классы
class Bouquets(DataBase):
    __tablename__ = 'bouquets'
    bouquet_id = Column(Integer, primary_key=True)
    bouquet_name = Column(String(100), nullable=False)
    bouquet_cost =Column(Integer, nullable=False)
    bouquet_desc = Column(Text, nullable=False)
    height = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    bouquet_image = Column(String)
    order = relationship("Orders", backref='bouquets')

class Papers(DataBase):
    __tablename__ = 'papers'
    paper_id = Column(Integer, primary_key=True)
    paper_name = Column(String(50), nullable=False)
    paper_desc = Column(Text, nullable=False)
    paper_cost = Column(Float, nullable=False)
    paper_image = Column(String) 
    order = relationship("Orders", backref='papers')

class Tapes(DataBase):
    __tablename__ = 'tapes'
    tape_id = Column(Integer, primary_key=True)
    tape_name = Column(String(50), nullable=False)
    tape_desc = Column(Text, nullable=False)
    tape_cost = Column(Float, nullable=False)
    tape_image = Column(String) 
    order = relationship("Orders", backref='tapes')

class Users(DataBase):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_email = Column(String, nullable=False)
    user_password = Column(String(255), nullable=False, server_default='')
    order = relationship("Orders", backref='users')

class Orders(DataBase):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    bouquet_id = Column(Integer, ForeignKey('bouquets.bouquet_id'))
    paper_id = Column(Integer, ForeignKey('papers.paper_id'))
    tape_id = Column(Integer, ForeignKey('tapes.tape_id'))
    day = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

engine = create_engine('sqlite:///bloom.db')
DataBase.metadata.create_all(engine)
