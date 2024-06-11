from flask_restful import reqparse, abort, Api, Resource, request
from ..model.userroleapplication import UserRoleApplication, UserRoleApplicationLogic
from ..model.db import Init

class AppAccessCheck(Resource):
    def get(self):
        role = request.args.get("role")
        app = request.args.get("app")

        print("\n\nAppAccessCheck")

        res = UserRoleApplicationLogic(Init.get_engine()).check_app_role(role, app)
        return { 'status' : 'Ok', 'data' : res }
    