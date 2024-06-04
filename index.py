from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from classes.access import Access

app = Flask(__name__)
api = Api(app)


api.add_resource(Access, "/access")

@app.route('/')
def index():
    return "hello world"


if __name__ == '__main__':
    app.run(debug=True)
