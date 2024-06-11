from flask_restful import reqparse, abort, Api, Resource, request
from ..model.userroletable import UserRoleTable, UserRoleTableLogic
from ..model.db import Init

class TableRole(Resource):
    def get(self):
        role = request.args.get("role")
        documents = UserRoleTableLogic(Init.get_engine()).find_role_tables(role)
        return { 'status' : 'Ok', 'data' : documents }
    
    def post(self):
        role = request.args.get("role")
        data = request.get_json()
        tables = data['tables']
        for table in tables:
            t = UserRoleTable(role=role, table=table['table'], storage=table['storage'])    
            o = UserRoleTableLogic(Init.get_engine())
            o.add(t)

        return { 'status' : 'Ok', 'data' : f'tables have been saved for role \'{role}\'' }