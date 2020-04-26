from __future__ import print_function

import os
import sys

from worker_lambda.helpers import secrets

# Load lob-python root directory into the import path so you can use the lob package without having to install it through pip.
sys.path.insert(0, os.path.abspath(__file__+'../..'))
import lob

secretsDict = secrets.get_secret()
lob.api_key = secretsDict.get("LOB_KEY")

def postcard(to_address, from_address, img_url):
    lob.Postcard.create(
        description='Postcard',
        to_address=to_address,
        from_address=from_address,
        back="""
          <html>
            <head>
            <link href="https://fonts.googleapis.com/css2?family=Caveat&display=swap" rel="stylesheet">
            <style>
                #safe-area {
                position: absolute;
                width: 5.875in;
                height: 3.875in;
                left: 0.1875in;
                top: 0.7in;
                background-color: rgba(255, 255, 255, 0.5);
                font-family: 'Caveat', cursive;
                }
            </style>
            </head>

            <body id="safe-area">
            <h1>Hi!</h1>
            <div>Thought you would enjoy this moment! </div>
            <div>{{FROM}}</body>

            </html>

            """,
        merge_variables={
            'FROM': os.environ['FROM_LINE'],
        },
         front = img_url,
    )

def get_address(prefix):
    address = lob.Address.create(
        name=os.environ.get(prefix + "_NAME"),
        address_line1=os.environ.get(prefix + "_ADDRESS_LINE_1"),
        address_city=os.environ.get(prefix + "_CITY"),
        address_state=os.environ.get(prefix + "_STATE"),
        address_country=os.environ.get(prefix + "_COUNTRY"),
        address_zip=os.environ.get(prefix + "_ZIP")
    )
    return(address)