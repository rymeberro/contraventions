from flask import Flask

app = Flask(__name__)
schedule_app = Flask(__name__)
from app import index
def getApp():
    return app
