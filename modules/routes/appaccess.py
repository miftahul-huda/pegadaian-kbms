from flask_restful import reqparse, abort, Api, Resource, request
from ..model.userroleapplication import UserRoleApplication, UserRoleApplicationLogic
from ..model.db import Init

class AppAccess(Resource):
    def get(self):
        role = request.args.get("role")
        apps = UserRoleApplicationLogic(Init.get_engine()).find_role_application(role)
        return { 'status' : 'Ok', 'data' : apps }
    
    def post(self):
        role = request.args.get("role")
        data = request.get_json()
        apps = data['apps']
        for app in apps:
            t = UserRoleApplication(role=role, app=app['app'] )    
            o = UserRoleApplicationLogic(Init.get_engine())
            o.add(t)

        return { 'status' : 'Ok', 'data' : f'applications have been saved for role \'{role}\'' }