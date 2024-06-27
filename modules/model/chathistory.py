from sqlalchemy import create_engine, Column, Sequence, Integer, String, Text, DateTime, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass
from flask import Flask, jsonify
from sqlalchemy import inspect
from ..libs.utils import serialize_datetime, myjson, randomstr
import json
import requests
from requests.auth import HTTPBasicAuth

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

    def find_auto_history(self, user):
        rows = self.session.query( ChatHistory.session).filter(
            and_( ChatHistory.userID.like(f"%{user}%"), 
                  ChatHistory.question_query_type.like(f"semantic-auto")
                )).distinct().all()
        arr = []
        for c in rows:
            arr.append( { 'session': c.session } )
        return arr

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
            and_( ChatHistory.session.like(f"%{session}%"), 
                  ChatHistory.question_query_type.like(f"semantic-search")
                )).all()
        return myjson(rows=rows)


    def find_query_history_by_session(self, session):
        rows = self.session.query(ChatHistory).filter(
            and_( ChatHistory.session.like(f"%{session}%"), 
                  ChatHistory.question_query_type.like(f"semantic-query")
                )).all()
        return myjson(rows=rows)
    
    def find_all_history_by_session(self, session):
        rows = self.session.query(ChatHistory).filter(ChatHistory.session.like(f"%{session}%")).all()
        return myjson(rows=rows)
    
    def check_session(user, session):
        registeredSessionLogic =  RegisteredSessionLogic(Init.get_engine())
        checkSession = registeredSessionLogic.check_session(user=user, session=session)
        return checkSession


    def chat_search(self, user, session, query, history):
        print("QUERY")
        print(query)
        print("HISTORY")
        print(history)

        registeredSessionLogic = RegisteredSessionLogic(Init.get_engine())
        chat_session = registeredSessionLogic.get_session(user["user"], session)

        if(chat_session is None):
            raise NoSessionExistError("No session '" + session + "' exists for user " + user["user"]) 
        elif (chat_session.quota <= 0):
            raise QuotaRanOutError("Quota ran out for session " + session)
        else:
            chatID = "chat-" + randomstr(10)
            quota = chat_session.quota - 1

            # If quota is not -1
            if (quota >= 0):
                registeredSessionLogic.update_session_quota(user["user"], session, quota)
                chat_session = registeredSessionLogic.get_session(user["user"], session)

                now = datetime.now()
                formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

                url = os.environ.get("semantic-search-url")
                headers = {
                    "accept" : "application/json",
                    "user-id" : user["user"],
                    "session-id" : session,
                    "role-id" : user["role"],
                    "Content-Type" : "application/json"
                }
                
                data = {
                    "prompt" : query,
                    "user_id" : user["user"],
                    "history" : history
                }

                response = requests.post(url, headers=headers, json=data, auth=HTTPBasicAuth("vertex", "BigData123!"))
                print(response)
                return { 'quota' : chat_session.quota, 'response' : response.text, 'session' : session, 'chatID' : chatID, 'date' : formatted_datetime, 'type' : 'semantic-search'  }


    def chat_query(self, user, session, query, history):
        print("QUERY")
        print(query)
        print("HISTORY")
        print(history)     
        
        registeredSessionLogic = RegisteredSessionLogic(Init.get_engine())
        chat_session = registeredSessionLogic.get_session(user["user"], session)

        if(chat_session is None):
            raise NoSessionExistError("No session '" + session + "' exists for user " + user["user"]) 
        elif (chat_session.quota <= 0):
            raise QuotaRanOutError("Quota ran out for session " + session)
        else:

            quota = chat_session.quota - 1
            registeredSessionLogic.update_session_quota(user["user"], session, quota)
            chat_session = registeredSessionLogic.get_session(user["user"], session)

            chatID = "chat-" + randomstr(10)
            now = datetime.now()
            formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

            url = os.environ.get("semantic-query-url")
            headers = {
                "accept" : "application/json",
                "user-id" : user["user"],
                "session-id" : session,
                "role-id" : user["role"],
                "Content-Type" : "application/json"
             }
            
            data = {
                "prompt" : query,
                "user_id" : user["user"],
                "history" : history
            }

            response = requests.post(url, headers=headers, json=data, auth=HTTPBasicAuth("vertex", "BigData123!"))
            print(response)
            return { 'quota' : chat_session.quota, 'response' : response.text, 'session' : session, 'chatID' : chatID, 'date' : formatted_datetime, 'type' : 'semantic-query'  }


    def chat_auto(self, user, session, query, history):
        print("USER")
        print(user)      

        print("History")
        print(history)  
        
        registeredSessionLogic = RegisteredSessionLogic(Init.get_engine())
        chat_session = registeredSessionLogic.get_session(user["user"], session)

        if(chat_session is None):
            raise NoSessionExistError("No session '" + session + "' exists for user " + user["user"]) 
        elif (chat_session.quota <= 0):
            raise QuotaRanOutError("Quota ran out for session " + session)
        else:

            quota = chat_session.quota - 1
            registeredSessionLogic.update_session_quota(user["user"], session, quota)
            chat_session = registeredSessionLogic.get_session(user["user"], session)

            chatID = "chat-" + randomstr(10)
            now = datetime.now()
            formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")

            url = os.environ.get("semantic-auto-url")
            headers = {
                "accept" : "application/json",
                "user-id" : user["user"],
                "session-id" : session,
                "role-id" : user["role"],
                "Content-Type" : "application/json"
             }
            
            data = {
                "prompt" : query,
                "user_id" : user["user"],
                "history" : history
            }

            response = requests.post(url, headers=headers, json=data, auth=HTTPBasicAuth("vertex", "BigData123!"))
            print(response)
            return { 'quota' : chat_session.quota, 'response' : response.text, 'session' : session, 'chatID' : chatID, 'date' : formatted_datetime, 'type' : 'semantic-auto'  }


    #def save_chat_history(self, user, session, chatID, query, response, time):
