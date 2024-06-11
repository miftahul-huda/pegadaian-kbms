import os
from flask import Flask, request, jsonify, g
from flask_restful import reqparse, abort, Api, Resource
from modules.routes.appaccess import AppAccess
from modules.routes.searchhistory import SearchHistory
from modules.routes.queryHistory import QueryHistory
from modules.routes.documentRole import DocumentRole
from modules.routes.tableRole import TableRole
from modules.routes.registeredsession import RegisteredSession
from modules.routes.util import Util
from modules.libs.utils import extract_bearer_token

app = Flask(__name__)
api = Api(app)

def before_request():
    # Pre-processing logic (e.g., set global variables)
    print("before_request")
    auth_header = request.headers.get('Authorization')
    user = extract_bearer_token(auth_header)
    print(user)
    if(user is None):
        return jsonify({"error": "Unauthorized"}), 401
    else:
        g.user = user

def after_request(response):
    print("after_request")
    print(response)
    return response

app.before_request(before_request)
app.after_request(after_request)
api.add_resource(RegisteredSession, "/session/new")
api.add_resource(AppAccess, "/app-access")
api.add_resource(SearchHistory, "/semantic-search")
api.add_resource(QueryHistory, "/semantic-query")
api.add_resource(DocumentRole, "/document-role")
api.add_resource(TableRole, "/table-role")
api.add_resource(Util, "/util")


@app.route('/')
def index():
    return "hello world"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)