from flask_restful import reqparse, abort, Api, Resource, request
from ..model.db import Init
from ..model.chathistory import ChatHistory, ChatHistoryLogic

class QueryHistory(Resource):
    def get(self):
        user = request.args.get("user")
        chatHistoryLogic = ChatHistoryLogic(Init.get_engine())
        chatHistories = chatHistoryLogic.find_query_history(user)
        return { 'status' : 'Ok', 'data' : chatHistories }
    
    def post(self):
        session = request.args.get("session")
        data = request.get_json()
        print(data)
        return { 'status' : 'Ok', 'data' : data }
