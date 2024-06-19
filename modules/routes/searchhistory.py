from flask_restful import reqparse, abort, Api, Resource, request
from ..model.db import Init
from ..model.chathistory import ChatHistory, ChatHistoryLogic
from ..model.errors import NoSessionExistError, QuotaRanOutError
from flask import g


class SearchHistory(Resource):
    def get(self):
        user = request.args.get("user")
        chatHistoryLogic = ChatHistoryLogic(Init.get_engine())
        chatHistories = chatHistoryLogic.find_search_history(user)
        return { 'status' : 'Ok', 'data' : chatHistories }
    
    def post(self):
        apiresponse = None
        session = request.args.get("session")
        user = g.user
        data = request.get_json()
        query = data["query"]
        chatHistoryLogic = ChatHistoryLogic(Init.get_engine())

        try:
            response = chatHistoryLogic.chat_search(user, session, query)
            apiresponse = { 'status' : 'Ok', 'data' : response }
        except NoSessionExistError as e1:
            print(e1)
            apiresponse = { 'status' : "Error", 'message' : 'No session exists for ' + session}
        except QuotaRanOutError as e2:
            print(e2)
            apiresponse = { 'status' : "Error", 'message' : 'Quota ran out for ' + session}

        return apiresponse
