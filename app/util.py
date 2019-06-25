import random
import string
from flask import send_from_directory
from app import app
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

