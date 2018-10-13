import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__) #initialize Flask app
CORS(app)
app.config.from_object(os.environ['APP_SETTINGS']) #config must be defined in an envvar, ex.: "config.DevelopmentConfig"
api = Api(app) #make an Flask_RESTful api for the app

#create all db tables
@app.before_first_request
def create_tables():
    from database import init_db
    init_db()

from database import db_session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def hello():
    return "Hello World!"

import endpoints
# create a deadline
api.add_resource(endpoints.CreateDeadline, '/create-deadline')
# get complete info of specific deadline
api.add_resource(endpoints.OneDeadline, '/deadline/<string:id>')

# Routes we need:
# get general info of all deadlines
# destroy a deadline

if __name__ == '__main__':
    app.run()
