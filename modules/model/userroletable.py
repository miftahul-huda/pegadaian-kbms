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


class UserRoleTable(Base):
    __tablename__ = 'userroletable'
    id = Column(Integer, Sequence("user_role_table_id_seq"), primary_key=True)  # Auto-incrementing primary key
    table = Column(String)
    role = Column(String)
    storage = Column(String)
    createdAt = Column(DateTime)

    def toDict(self):
        dic = { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
        return dic


    
class UserRoleTableLogic:
    def __init__(self, engine):
        print("---UserRoleTableLogic.init---")
        self.engine = engine
        Session = sessionmaker(bind=engine)
        session = Session()
        self.session = session
        #Base = declarative_base()
        Base.metadata.create_all(engine)


    def add(self, o):
        o.createdAt = datetime.now()
        self.session.add(o)
        self.session.commit()

    def find_role_tables(self, role):
        rows = self.session.query(UserRoleTable).filter(UserRoleTable.role.like(f"%{role}%")).all()
        return myjson(rows=rows)

        

    