# SMS to Postcard Serverless App

[![Maintainability](https://api.codeclimate.com/v1/badges/996946131494b03f23ee/maintainability)](https://codeclimate.com/github/mattdini/sms-postcard/maintainability)


With the quaratine/lockdown in place my parents have been really missing seeing their granddaughters.  I built this as a way to send them pictures in the mail with the least amount of resistance.  No apps to download, no software, just send a text message to a twilio number and a postcard will be mailed the next day!

![Alt text](docs/example.png?raw=true "Example Postcard")

## Requirements

- A Twilio Account (https://www.twilio.com/)
  - With a SMS enabled phone number
- A LOB account (https://lob.com/)
- An AWS account (https://aws.amazon.com/)
- Serverless (https://serverless.com/framework/docs/getting-started/)

## Stack

- API Gateway
- Lambda
- S3
- Secrets Manager

## Pre-Deploy Setup

Open `serverless.yml` and edit the TO and FROM addresses starting on line 7:

```
custom:
  bucket: ${self:service}-to-lob
  region: "us-west-2"
  ### TO ###
  ToName: "Papa & Nana"
  ToAddressLine1: "123 SW Fake Street"
  ToCity: "Portland"
  ToState: "OR"
  ToCountry: "US"
  ToZip: "97205"
  ### FROM ###
  FromName: "The Girls"
  FromAddressLine1: "456 SE Fake Street"
  FromCity: "Milwaukie"
  FromState: "OR"
  FromCountry: "US"
  FromZip: "97222"
  ### Sign Off Line ###
  FromLine: "The Girls"
```

## Pre-Deply Setup Secrets

In AWS setup your API keys/secrets by going to: Services > AWS Secrets Manager
Secrets > Click `Store a new secret` >  Click `Other type of secrets (e.g. API key)` and create 3 new keys:


![Alt text](docs/secrets.png?raw=true "Example Secrets Manager")

- Twilio API keys can be found right on your project dashboard 
- LOB API keys can be found by click on YOUR NAME > Settings > Secret API Keys

## Deploy

From command line in the project folder: `sls deploy -v`

## Post-Deploy Setup

Back in AWS get your API gateway URL by going to:
Services > API Gateway > `dev-sms-postcard` > Stages > Expand `Dev` > Click `/message/ POST`

Copy the Invoke URL that looks like: `https://1234abcdfg.execute-api.us-west-2.amazonaws.com/dev/message`

Head to Twilio and click on `All Products and Services` > `Phone Numbers` > Click on your Number > Scroll down to `Messaging` > and set `A Message Comes In` to your URL with `HTTP POST`:

![Alt text](docs/twiliosetup.png?raw=true "Twilio Example POST")

## Usage

Done!  Just send a photo to your Twilio phone number, you should get back a text saying "Thanks!"

You can vew your postcard in LOB by clicking on `Postcards` under `Postcards API` section, when you're happy with it, switch your LOB API key to the `live_` version and you'll be sending postcards in no time!
