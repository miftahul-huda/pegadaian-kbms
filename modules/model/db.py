import os
from sqlalchemy import create_engine, Column, Sequence, Integer, String, Text, DateTime


class Init:
    def get_engine():
        # Create the engine (replace with your PostgreSQL connection details)
        s = f'{os.environ.get("dbengine")}://{os.environ.get("dbuser")}:{os.environ.get("dbpassword")}@{os.environ.get("dbhost")}:{os.environ.get("dbport")}/{os.environ.get("dbname")}'
        print(s)
        engine = create_engine(s)    
        return engine