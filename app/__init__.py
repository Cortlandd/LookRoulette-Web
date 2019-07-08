from flask import Flask
import os
import boto3, botocore
import tensorflow as tf

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

def load_graph():
    print("Initialized Graph")
    ###
    # Load Graph
    ###
    # May regret this
    tf.reset_default_graph()
    frozen_graph="output_graph.pb"
    with tf.gfile.GFile(frozen_graph, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    with tf.Graph().as_default() as graph:
        tf.import_graph_def(
            graph_def,
            input_map=None,
            return_elements=None,
            name=""
        )
    return graph

graph = load_graph()

# This has to be at the bottom for some reason
from app import routes


