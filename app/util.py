import random
import string
from flask import send_from_directory
from app import app, global_graph
import os
from imageio import imread, imsave
from app import app, s3, S3_BUCKET, S3_LOCATION
import tensorflow as tf
import cv2
import numpy as np

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

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def transfer(nomakeup_url, makeup_url):

    img_size = 256

    nomakeup = cv2.resize(imread(nomakeup_url), (img_size, img_size))
    makeup = cv2.resize(imread(makeup_url), (img_size, img_size))

    X_img = np.expand_dims(preprocess(nomakeup), 0)
    Y_img = np.expand_dims(preprocess(makeup), 0)

    ###
    # Get tensors by name
    # X:0 = Input
    # Y:0 = Input
    # generator/xs:0 = Output
    ###
    # Use graph from app
    X = global_graph.get_tensor_by_name('X:0') # Makeup Image
    Y = global_graph.get_tensor_by_name('Y:0') # No Makeup Image
    Xs = global_graph.get_tensor_by_name('generator/xs:0')

    # Run session feeding input 
    sess = tf.Session(graph=global_graph)
    n = sess.run(Xs, feed_dict={X: X_img, Y: Y_img})
    sess.close()
    n = deprocess(n)

    r = n[0]

    result_img_name = 'transfer-'+randomString()+'.png'

    imsave(app.config['UPLOAD_FOLDER']+result_img_name, (r * 255).astype(np.uint8))

    result_img = app.config['UPLOAD_FOLDER']+result_img_name

    result = None

    try:
        s3.upload_file(
            result_img,
            S3_BUCKET,
            result_img_name,
            ExtraArgs={
                "ACL": "public-read"
            }
        )
        result = S3_LOCATION+result_img_name
        os.remove(result_img)
    except Exception as e:
        result = str(e)

    return result