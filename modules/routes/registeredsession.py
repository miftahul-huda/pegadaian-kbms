from flask_restful import reqparse, abort, Api, Resource, request
from flask import g
from ..model.db import Init
from ..model.registeredsession import RegisteredSession, RegisteredSessionLogic
from ..libs.utils import serialize_datetime, myjson, randomstr

class RegisteredSession(Resource):
    def get(self):
        user = g.user
        session = RegisteredSessionLogic(Init.get_engine()).new(user=user)
        return { 'status' : 'Ok', 'data' : session }