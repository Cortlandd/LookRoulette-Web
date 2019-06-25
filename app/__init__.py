from flask import Flask
import os

app = Flask(__name__)
UPLOAD_FOLDER = app.root_path + '/imgs/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# This has to be at the bottom for some reason
from app import routes


