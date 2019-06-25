import tensorflow as tf
import cv2
import os
from app import app, s3, S3_BUCKET, S3_LOCATION
import numpy as np
from flask import jsonify
from imageio import imread, imsave
import requests
from PIL import Image
from io import BytesIO
import random
import string

def preprocess(img):
    """
    Preprocess image before passing to tensorflow
    """
    return (img / 255.0 - 0.5) * 2


def deprocess(img):
    """
    Deprocess image results.
    """
    return (img + 1) / 2

def transfer_makeup(nomakeup_img_url, makeup_img_url):
    
    img_size = 256

    n = S3_LOCATION + nomakeup_img_url
    m = S3_LOCATION + makeup_img_url

    print("No makeup image: ", n)
    print("Makeup image: ", m)

    nomakeup_img = imread(n)
    makeup_img = imread(m)

    nomakeup = cv2.resize(nomakeup_img, (img_size, img_size))
    makeup = cv2.resize(makeup_img, (img_size, img_size))

    X_img = np.expand_dims(preprocess(nomakeup), 0)
    Y_img = np.expand_dims(preprocess(makeup), 0)

    ###
    # Load Graph
    ###
    #frozen_graph=os.path.join(app.root_path, 'app', 'output_graph.pb')
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
    n = deprocess(n)

    r = n[0]

    result_img_name = 'transfer-'+randomString()+'.png'

    imsave('app/imgs/'+result_img_name, (r * 255).astype(np.uint8))

    result_img = 'app/imgs/'+result_img_name

    try:
        s3.upload_file(
            result_img,
            S3_BUCKET,
            result_img_name,
            ExtraArgs={
                "ACL": "public-read"
            }
        )
    except Exception as e:
        
        print("Upload Error: ", e)

    result = {
        'makeup_transfer_image': S3_LOCATION+result_img_name
    }

    os.remove('app/imgs/'+result_img_name)

    return jsonify(result)

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))