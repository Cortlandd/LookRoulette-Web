import random
import string
from flask import send_from_directory
import os

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


def send_image(img):
    if img is not None:
        send_from_directory('app/imgs', img, as_attachment=True)
        os.remove('app/imgs/'+img)
    else:
        return 
    
