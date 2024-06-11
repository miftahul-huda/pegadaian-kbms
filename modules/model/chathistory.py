from sqlalchemy import create_engine, Column, Sequence, Integer, String, Text, DateTime, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass
from flask import Flask, jsonify
from sqlalchemy import inspect
from ..libs.utils import serialize_datetime, myjson
import json


Base = declarative_base()

    
class ChatHistory(Base):
    __tablename__ = 'chathistory'
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)  # Auto-incrementing primary key
    session = Column(String)
    question_query = Column(Text)
    response = Column(Text)
    question_query_type = Column(String)
    userID = Column(String)
    createdAt = Column(DateTime)

    def toDict(self):
        dic = { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
        return dic


    
class ChatHistoryLogic:
    def __init__(self, engine):
        print("---ChatHistoryLogic.init---")
        self.engine = engine
        Session = sessionmaker(bind=engine)
        session = Session()
        self.session = session
        #Base = declarative_base()
        Base.metadata.create_all(engine)


    def add(self, o):
        self.session.add(o)
        self.session.commit()

    def find_search_history(self, user):
        rows = self.session.query( ChatHistory.session).filter(
            and_( ChatHistory.userID.like(f"%{user}%"), 
                  ChatHistory.question_query_type.like(f"semantic-search")
                )).distinct().all()
        arr = []
        for c in rows:
            arr.append( { 'session': c.session } )
        return arr

    def find_query_history(self, user):
        rows = self.session.query(ChatHistory).with_entities(ChatHistory.session, ChatHistory.userID).filter(
            and_( ChatHistory.userID.like(f"%{user}%"), 
                  ChatHistory.question_query_type.like(f"semantic-query")
                )).distinct().all()
        
        arr = []
        for c in rows:
            arr.append( { 'session': c.session } )
        return arr
    
    def find_search_history_by_session(self, session):
        rows = self.session.query(ChatHistory).filter(
            and_( ChatHistory.userID.like(f"%{session}%"), 
                  ChatHistory.question_query_type.like(f"semantic-search")
                )).all()
        return myjson(rows=rows)


    def find_query_history_by_session(self, session):
        rows = self.session.query(ChatHistory).filter(
            and_( ChatHistory.userID.like(f"%{session}%"), 
                  ChatHistory.question_query_type.like(f"semantic-query")
                )).all()
        return myjson(rows=rows)
        

    