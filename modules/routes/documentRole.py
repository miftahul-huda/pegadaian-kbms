from flask_restful import reqparse, abort, Api, Resource, request
from ..model.userrolefile import UserRoleFile, UserRoleFileLogic
from ..model.db import Init

class DocumentRole(Resource):
    def get(self):
        role = request.args.get("role")
        documents = UserRoleFileLogic(Init.get_engine()).find_role_tables(role)
        return { 'status' : 'Ok', 'data' : documents }
    
    def post(self):
        role = request.args.get("role")
        data = request.get_json()
        files = data['documents']
        for file in files:
            t = UserRoleFile(role=role, file=file['file'] )    
            o = UserRoleFileLogic(Init.get_engine())
            o.add(t)

        return { 'status' : 'Ok', 'data' : f'documents have been saved for role \'{role}\'' }