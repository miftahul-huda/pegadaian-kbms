import os
from flask import Flask, request, jsonify, g
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS

from modules.routes.appaccess import AppAccess
from modules.routes.appaccesscheck import AppAccessCheck
from modules.routes.searchhistory import SearchHistory
from modules.routes.queryhistory import QueryHistory
from modules.routes.autohistory import AutoHistory

from modules.routes.documentRole import DocumentRole
from modules.routes.tableRole import TableRole
from modules.routes.registeredsession import RegisteredSession
from modules.routes.util import Util
from modules.libs.utils import extract_bearer_token
from modules.routes.configuration import Configuration


app = Flask(__name__)
cors = CORS(app, origins=["*"], methods=["GET", "POST", "OPTIONS"])  # NOT RECOMMENDED FOR PRODUCTION

api = Api(app)

def before_request():
    # Pre-processing logic (e.g., set global variables)
    print("before_request")
    print(request.path)
    
    request_path = request.path
    request_path = request_path.split("/")
    notutil = True
    if ("util"  in request_path):
        notutil = False
    
    auth_header = request.headers.get('Authorization')

    
    if(notutil == True):
        content_type = request.headers.get('Content-Type')        
        user = extract_bearer_token(auth_header)
        if(user == None and request.method.lower() != "options"):
            return jsonify({"error": "Unauthorized"}), 401
        else:
            g.user = user
    
        

def after_request(response):
    print("after_request")
    print(response)
    return response

app.before_request(before_request)
#app.after_request(after_request)

prefix = "/api/v1"
api.add_resource(RegisteredSession, f"{prefix}/session/new")
api.add_resource(AppAccess, f"{prefix}/app-access")
api.add_resource(AppAccessCheck, f"{prefix}/app-access/check")

api.add_resource(SearchHistory, f"{prefix}/semantic-search")
api.add_resource(QueryHistory, f"{prefix}/semantic-query")
api.add_resource(AutoHistory, f"{prefix}/semantic-auto")

api.add_resource(DocumentRole, f"{prefix}/document-role")
api.add_resource(TableRole, f"{prefix}/table-role")
api.add_resource(Util, f"{prefix}/util")
api.add_resource(Configuration, f"{prefix}/configuration")


@app.route('/')
def index():
    return "hello world"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)