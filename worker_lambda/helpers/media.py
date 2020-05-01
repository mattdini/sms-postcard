from __future__ import print_function

import base64
import os
import random
import string
import urllib.parse
import urllib.request

from PIL import Image, ImageOps

import boto3
import requests
from worker_lambda.helpers import secrets


def save_to_s3(filename):

    bucket_name = os.environ['LOB_BUCKET']
    prefix = ''.join(random.choice(string.ascii_lowercase)
                        for i in range(15))

    prefix = 'test'   
    s3_path = prefix + "/" + filename.split('/')[-1] + ".jpg"
    s3_client = boto3.client('s3')

    with open(filename, 'rb') as f:
        file = f.read()
        s3_client.put_object(Body=file, Bucket=bucket_name,
                                Key=s3_path, ACL='public-read')
    
    public_url = f"https://{bucket_name}.s3-us-west-2.amazonaws.com/{s3_path}"
                                
    return public_url

def save_to_tmp(MediaURL):
    normal = urllib.parse.unquote(MediaURL)
    filename = "/tmp/" + normal.rsplit('/', 1)[1]
    print(normal)

    r = requests.get(normal)

    with open(filename, 'wb') as outfile:
        outfile.write(r.content)

    im = Image.open(filename)
    width, height = im.size

    print(width)
    print(height)

    return filename

def normal_url(MediaURL):
    return urllib.parse.unquote(MediaURL)
    
    
def resize_image(image):
    print('Incoming Image: ' + image)
    new_size = (1875,1275)
    im = Image.open(image)
    resized_img = ImageOps.fit(im, new_size, method = Image.ANTIALIAS, centering = (0.5,0.5))
    resized_img.save(image + "_resized", 'JPEG', quality=95)
    
    return image + "_resized"

def delete_media(MessageSid, MediaURL):
    secretsDict = secrets.get_secret()
    normalURL = urllib.parse.urlparse(urllib.parse.unquote(MediaURL))
    Sid = normalURL.path.rsplit('/', 1)[1]

    TWILIO_ACCOUNT_SID = secretsDict.get("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = secretsDict.get("TWILIO_AUTH_TOKEN")
    TWILIO_DELETE_MEDIA_URL = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages/{MessageSid}/Media/{Sid}.json"

    req = urllib.request.Request(TWILIO_DELETE_MEDIA_URL)
    authentication = "{}:{}".format(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    base64string = base64.b64encode(authentication.encode("utf-8"))
    req.add_header("Authorization", "Basic %s" %
                    base64string.decode("ascii"))
    req.get_method = lambda: "DELETE"

    print(TWILIO_DELETE_MEDIA_URL)

    with urllib.request.urlopen(req) as f:
        print("Twilio returned {}".format(str(f.read().decode("utf-8"))))
