from flask_restful import reqparse, abort, Api, Resource, request
from ..model.configuration import Configuration, ConfigurationLogic
from ..model.db import Init

class Configuration(Resource):
    def get(self):
        config = ConfigurationLogic(Init.get_engine()).get()
        return { 'status' : 'Ok', 'data' : config }
    
    def post(self):
        o = request.get_json()
        ConfigurationLogic(Init.get_engine()).add(o)
        return { 'status' : 'Ok', 'data' : f'Configuration done' }