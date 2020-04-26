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

## Deploy

From command line in the project folder: `sls deploy -v`

## Post-Deploy Setup

Log into AWS and get your API gateway URL by going to:
Services > API Gateway > `dev-sms-postcard` > Stages > Expand `Dev` > Click `/message/ POST`

Copy the Invoke URL that looks like: `https://1234abcdfg.execute-api.us-west-2.amazonaws.com/dev/message`

Head to Twilio and click on `All Products and Services` > `Phone Numbers` > Click on your Number > Scroll down to `Messaging` > and set `A Message Comes In` to your URL with `HTTP POST`:


## Secrets

## Usage
