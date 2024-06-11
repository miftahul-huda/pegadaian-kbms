from sqlalchemy import create_engine, Column, Sequence, Integer, String, Text, DateTime, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass
from flask import Flask, jsonify
from sqlalchemy import inspect
from ..libs.utils import serialize_datetime, myjson
import json

Base = declarative_base()


class UserRoleApplication(Base):
    __tablename__ = 'userroleapp'
    id = Column(Integer, Sequence("user_role_app_id_seq"), primary_key=True)  # Auto-incrementing primary key
    app = Column(String)
    role = Column(String)
    createdAt = Column(DateTime)

    def toDict(self):
        dic = { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
        return dic


    
class UserRoleApplicationLogic:
    def __init__(self, engine):
        print("---UserRoleApplicationLogic.init---")
        self.engine = engine
        Session = sessionmaker(bind=engine)
        session = Session()
        self.session = session
        #Base = declarative_base()
        Base.metadata.create_all(engine)


    def add(self, o):
        self.session.add(o)
        self.session.commit()

    def find_role_application(self, role):
        rows = self.session.query(UserRoleApplication).filter(UserRoleApplication.role.like(f"%{role}%")).all()
        return myjson(rows=rows)

        

    