import os
import requests
from app import app, s3, S3_BUCKET, S3_LOCATION
from flask import render_template, request, jsonify
from werkzeug.utils import secure_filename
from app.transfer import transfer_makeup
import random
import string

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    nomakeup_file = request.files['nomakeup_file']
    makeup_file = request.files['makeup_file']

    nomakeup_filename = secure_filename(nomakeup_file.filename)
    makeup_filename = secure_filename(makeup_file.filename)

    nomakeup_extension = nomakeup_filename.split('.')[1]
    makeup_extension = makeup_filename.split('.')[1]

    ran_nomakeup = "nomakeup-"+randomString()+'.'+nomakeup_extension
    ran_makeup = "makeup-"+randomString()+'.'+makeup_extension

    try:
        s3.upload_fileobj(
            nomakeup_file,
            S3_BUCKET,
            ran_nomakeup,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": nomakeup_file.content_type
            }
        )

        s3.upload_fileobj(
            makeup_file,
            S3_BUCKET,
            ran_makeup,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": makeup_file.content_type
            }
        )
    except Exception as e:
        return e

    result = {
        'nomakeup-image': S3_LOCATION+ran_nomakeup,
        'makeup-image': S3_LOCATION+ran_makeup
    }

    return jsonify(result), 201

@app.route('/submit/nomakeup=<nomakeupURL>/makeup=<makeupURL>', methods=['POST'])
def submit_images(nomakeupURL, makeupURL):

    return transfer_makeup(nomakeup_img_url=nomakeupURL, makeup_img_url=makeupURL)

@app.route('/')
def index():
    return render_template('index.html')

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))