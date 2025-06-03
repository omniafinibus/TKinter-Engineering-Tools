import base64
from io import BytesIO
import tkinter_tools.resources._encoded_images as assets

def decode_image(data):
    """Return texture object from base64 encoded data"""
    im_bytes = base64.b64decode(data) # im_bytes is a binary image
    return BytesIO(im_bytes)          # convert image to file-like object