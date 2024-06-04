from flask_restful import reqparse, abort, Api, Resource, request

class Access(Resource):
    def get(self):
        app = request.args.get("app")
        role = request.args.get("role")
        return { 'status' : 'Ok', 'data' : { 'app' : app, 'accessible': True } }