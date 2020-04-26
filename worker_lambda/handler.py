from __future__ import print_function
from worker_lambda.helpers import media, lobHelper

import sys
import json
sys.path.append('../')

def lambda_handler(event, context):
    
    print("Received event: " + str(event))
    event_body = event['body']

    if event_body['NumMedia'] == '0':
        return respond('No Picture :(')

    normal_url = media.mediaHelper.normal_url(event_body['MediaUrl0'])
    tmp_file = media.mediaHelper.save_to_tmp(normal_url)
    resized = media.mediaHelper.resize_image(tmp_file)
    img_url = media.mediaHelper.save_to_s3(resized)
    
    lobHelper.postcard(lobHelper.get_address("TO"), lobHelper.get_address("FROM"), img_url)

    media.mediaHelper.delete_media(event_body['MessageSid'], event_body['MediaUrl0'])

    return respond('Thanks!')


def respond(message):
    response = f'<?xml version=\"1.0\" encoding=\"UTF-8\"?><Response><Message>{message}</Message></Response>'
    return response
