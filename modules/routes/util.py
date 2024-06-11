from flask_restful import reqparse, abort, Api, Resource, request
from ..libs.utils import get_encoded_payload

class Util(Resource):
    def post(self):
        command = request.args.get("command")
        payload = request.json
        if(command == "encode"):
            encoded_payload = get_encoded_payload(payload=payload)
            return { 'status' : 'Ok', 'data' : { 'encoded' : encoded_payload } }
        else:
            return { 'status' : 'Ok' }
