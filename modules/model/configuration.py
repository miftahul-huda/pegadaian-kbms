from sqlalchemy import create_engine, Column, Sequence, Integer, String, Text, DateTime, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass
from flask import Flask, jsonify
from sqlalchemy import inspect
from ..libs.utils import serialize_datetime, myjson
import json
from datetime import datetime

Base = declarative_base()


class Configuration(Base):
    __tablename__ = 'configuration'
    id = Column(Integer, Sequence("configuration_id_seq"), primary_key=True)  # Auto-incrementing primary key
    maxSessionPerUser = Column(Integer)
    maxQuestionPerSession = Column(Integer)
    chatbotFloat = Column(Integer)
    chatbotTitle = Column(String)
    chatbotAvatar = Column(Text)
    activateChatbot = Column(Integer)
    activatePortalOne = Column(Integer)
    isActive = Column(Integer)
    createdAt = Column(DateTime)

    def toDict(self):
        dic = { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
        return dic


    
class ConfigurationLogic:
    def __init__(self, engine):
        print("---ConfigurationLogic.init---")
        self.engine = engine
        Session = sessionmaker(bind=engine)
        session = Session()
        self.session = session
        #Base = declarative_base()
        Base.metadata.create_all(engine)


    def add(self, o):
        rows = self.session.query(Configuration).filter(Configuration.isActive == 1).all()
        if len(rows) > 0:
            self.session.delete(rows)

        o.isActive = 1
        o.createdAt = datetime.now()
        self.session.add(o)
        self.session.commit()

    def get(self):
        rows = self.session.query(Configuration).filter(Configuration.isActive == 1).first()
        print("rows")
        print(rows.toDict())
        return rows.toDict()

        

    