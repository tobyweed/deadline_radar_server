import os
from flask import Flask
from flask_cors import CORS

app = Flask(__name__) #initialize Flask app
CORS(app)
app.config.from_object(os.environ['APP_SETTINGS']) #config must be defined in an envvar, ex.: "config.DevelopmentConfig"

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/trick')
def trick():
    return "Moose!"

if __name__ == '__main__':
    app.run()
