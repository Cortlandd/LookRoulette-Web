from flask import Flask
import os
import boto3, botocore

S3_BUCKET                 = "lookru-bucket"
S3_KEY                    = "AKIAJNAFT2ZYDUJ7DBFA"
S3_SECRET                 = "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"
S3_LOCATION = 'https://{}.s3.us-east-2.amazonaws.com/'.format(S3_BUCKET)

app = Flask(__name__)
UPLOAD_FOLDER = app.root_path + '/imgs/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)

# This has to be at the bottom for some reason
from app import routes


