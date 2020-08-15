
from mongoengine import *
from flask import Flask
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(20)
connect('nolansbigbutt', host='mongodb://dongo:nollieb99@ds113692.mlab.com:13692/nolansbigbutt')



from .routes import *
