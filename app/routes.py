import os
import requests
from app import app, s3, S3_BUCKET, S3_LOCATION
from flask import render_template, request, jsonify, send_from_directory, after_this_request
from app.util import preprocess, deprocess, randomString
import random
import string
import tensorflow as tf
import cv2
import os
import numpy as np
from flask import jsonify
from imageio import imread, imsave
import random
import string

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/v1/makeup_transfer')
def makeup_transfer():

    nomakeup_file = request.files['nomakeup_file']
    makeup_file = request.files['makeup_file']

    img_size = 256

    nomakeup = cv2.resize(imread(nomakeup_file), (img_size, img_size))
    makeup = cv2.resize(imread(makeup_file), (img_size, img_size))

    X_img = np.expand_dims(preprocess(nomakeup), 0)
    Y_img = np.expand_dims(preprocess(makeup), 0)

    ###
    # Load Graph
    ###
    #frozen_graph=os.path.join(app.root_path, 'app', 'output_graph.pb')
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

    ###
    # Get tensors by name
    # X:0 = Input
    # Y:0 = Input
    # generator/xs:0 = Output
    ###
    X = graph.get_tensor_by_name('X:0') # Makeup Image
    Y = graph.get_tensor_by_name('Y:0') # No Makeup Image
    Xs = graph.get_tensor_by_name('generator/xs:0')

    # Run session feeding input 
    sess = tf.Session(graph=graph)
    n = sess.run(Xs, feed_dict={X: X_img, Y: Y_img})
    sess.close()
    n = deprocess(n)

    r = n[0]

    result_img_name = 'transfer-'+randomString()+'.png'

    imsave(app.config['UPLOAD_FOLDER']+result_img_name, (r * 255).astype(np.uint8))

    result_img = app.config['UPLOAD_FOLDER']+result_img_name

    result = {}

    try:
        s3.upload_file(
            result_img,
            S3_BUCKET,
            result_img_name,
            ExtraArgs={
                "ACL": "public-read"
            }
        )
        result = {
            'transferImage': S3_LOCATION+result_img_name
        }
    except Exception as e:
        result = {
            'error': e
        }

    if result_img is not None:
        os.remove(result_img)
    
    return jsonify(result)
    
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

