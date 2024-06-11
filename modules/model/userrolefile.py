from sqlalchemy import create_engine, Column, Sequence, Integer, String, Text, DateTime, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass
from flask import Flask, jsonify
from sqlalchemy import inspect
from ..libs.utils import serialize_datetime, myjson
import json

Base = declarative_base()


class UserRoleFile(Base):
    __tablename__ = 'userrolefile'
    id = Column(Integer, Sequence("user_role_file_id_seq"), primary_key=True)  # Auto-incrementing primary key
    file = Column(String)
    role = Column(String)
    createdAt = Column(DateTime)

    def toDict(self):
        dic = { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
        return dic


    
class UserRoleFileLogic:
    def __init__(self, engine):
        print("---UserRoleFileLogic.init---")
        self.engine = engine
        Session = sessionmaker(bind=engine)
        session = Session()
        self.session = session
        #Base = declarative_base()
        Base.metadata.create_all(engine)


    def add(self, o):
        self.session.add(o)
        self.session.commit()

    def find_role_files(self, role):
        rows = self.session.query(UserRoleFile).filter(UserRoleFile.role.like(f"%{role}%")).all()
        return myjson(rows=rows)

        

    