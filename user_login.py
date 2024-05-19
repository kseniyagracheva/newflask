
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import DataBase, Bouquets, Papers, Tapes, Users, Orders

engine = create_engine('sqlite:///bloom.db') 
DataBase.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

class UserLogin():
    def __init__(self):
        self.user_id = None
        
    def fromDB(self, user_id):
        self.__user = session.query(Users).filter_by(user_id=user_id).first()
        self.user_id = user_id
        return self
    
    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id) 
