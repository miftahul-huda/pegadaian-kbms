from sqlalchemy import create_engine, Column, Sequence, Integer, String, Text, DateTime, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass
from flask import Flask, jsonify
from sqlalchemy import inspect
from ..libs.utils import serialize_datetime, myjson, randomstr
import json

import google.generativeai as genai
from google.api_core import retry
import os

from .registeredsession import RegisteredSession, RegisteredSessionLogic
from .db import Init

from .errors import QuotaRanOutError, NoSessionExistError
from datetime import datetime


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
    
    def check_session(user, session):
        registeredSessionLogic =  RegisteredSessionLogic(Init.get_engine())
        checkSession = registeredSessionLogic.check_session(user=user, session=session)
        return checkSession


    def chat_search(self, user, session, query):

        registeredSessionLogic = RegisteredSessionLogic(Init.get_engine())
        chat_session = registeredSessionLogic.get_session(user["user"], session)

        if(chat_session is None):
            raise NoSessionExistError("No session exists : " + session) 
        elif (chat_session.quota <= 0):
            raise QuotaRanOutError("Quota ran out for session " + session)
        else:
            genai.configure(api_key=os.environ.get("gemini-api-key"))
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(query)

            quota = chat_session.quota - 1
            registeredSessionLogic.update_session_quota(user["user"], session, quota)
            chat_session = registeredSessionLogic.get_session(user["user"], session)

            chatID = "chat-" + randomstr(10)
            now = datetime.now()
            formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

            return { 'quota' : chat_session.quota, 'response' : response.text, 'session' : session, 'chatID' : chatID, 'date' : formatted_datetime, 'type' : 'semantic-search'  }


    def chat_query(self, user, session, query):

        registeredSessionLogic = RegisteredSessionLogic(Init.get_engine())
        chat_session = registeredSessionLogic.get_session(user["user"], session)

        if(chat_session is None):
            raise NoSessionExistError("No session exists : " + session) 
        elif (chat_session.quota <= 0):
            raise QuotaRanOutError("Quota ran out for session " + session)
        else:
            genai.configure(api_key=os.environ.get("gemini-api-key"))
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(query, generation_config=genai.GenerationConfig(response_mime_type="application/json"))

            quota = chat_session.quota - 1
            registeredSessionLogic.update_session_quota(user["user"], session, quota)
            chat_session = registeredSessionLogic.get_session(user["user"], session)

            chatID = "chat-" + randomstr(10)
            now = datetime.now()
            formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

            return { 'quota' : chat_session.quota, 'response' : response.text, 'session' : session, 'chatID' : chatID, 'date' : formatted_datetime, 'type' : 'semantic-query'  }


    