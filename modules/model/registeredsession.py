from sqlalchemy import create_engine, Column, Sequence, Integer, String, Text, DateTime, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass
from flask import Flask, jsonify
from sqlalchemy import inspect
from ..libs.utils import serialize_datetime, myjson, randomstr
import json
import datetime
from ..model.configuration import ConfigurationLogic
from ..model.db import Init



Base = declarative_base()


class RegisteredSession(Base):
    __tablename__ = 'registeredsession'
    id = Column(Integer, Sequence("registered_session_id_seq"), primary_key=True)  # Auto-incrementing primary key
    session = Column(String)
    user = Column(String)
    quota = Column(Integer)
    createdAt = Column(DateTime)

    def toDict(self):
        dic = { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
        return dic


    
class RegisteredSessionLogic:
    def __init__(self, engine):
        print("---RegisteredSessionLogic.init---")
        self.engine = engine
        Session = sessionmaker(bind=engine)
        session = Session()
        self.session = session
        #Base = declarative_base()
        Base.metadata.create_all(engine)


    def new(self, user):
        c = ConfigurationLogic(Init.get_engine()).get()
        quota = 10
        if(c != None):
            quota = c["maxQuestionPerSession"]
        sesid = "ses" + randomstr(10)
        o = RegisteredSession(session=sesid, createdAt=datetime.datetime.now(), user=user["user"], quota=quota)
        self.session.add(o)
        self.session.commit()
        return { 'user' : user["user"], 'quota' : quota, 'session' : sesid }
    
    def check_session(self, user, session):
        print("---RegisteredSessionLogic.check_session---")
        print(user, session)
        o = self.session.query(RegisteredSession).filter(and_(RegisteredSession.user == user, RegisteredSession.session == session)).first()
        print(o)
        if o is None:
            return False
        return True
    


        

    