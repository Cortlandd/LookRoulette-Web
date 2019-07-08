import os
import requests
from app import app, s3, S3_BUCKET, S3_LOCATION
from flask import render_template, request, jsonify, send_from_directory, after_this_request
from app.util import preprocess, deprocess, randomString, transfer
import random
import string
import os
import numpy as np
from flask import jsonify
import random
import string
from werkzeug.urls import url_unquote

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/v1/makeup_transfer', methods=['POST'])
def makeup_transfer():

    nomakeup_url = request.args['nomakeup_url']
    makeup_url = request.args['makeup_url']

    url_unquote(nomakeup_url, charset='utf-8')
    url_unquote(makeup_url, charset='utf-8')
    
    result = None
    try:
        result = transfer(nomakeup_url, makeup_url)
    except Exception as e:
        raise e

    return jsonify(transferImage=result)
    
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
