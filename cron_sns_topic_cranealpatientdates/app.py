
import boto3
import pandas as pd 
import os
import json

from  common.sns_wrapper import *
from  common.dynamob_wrapper import *

# https://github.com/aws-cloudformation/custom-resource-helper



# https://www.sqlshack.com/set-up-a-local-serverless-environment-using-the-aws-sam-cli/
# 1. sam build --use-container 
# 2.sam local invoke "AppCranealPatientDatesFunction" --debug --env-vars resources/env.json
#   ó
#   sam local invoke 
# 3. pip freeze > requirements.txt NO HACER, METE MODULOS QUE NO SE PUEDEN INCLUIR DINAMICAMENTE POR LAMBDA 
#       pip install --target ./package csv CSV ES LA LIBRERIA A METER EN EL DIRECTORIO PACKAGE 
#       4. requirements.txt SOLO CON LOS MODULOS QUE SE IMPORTAN
# 5. Variables entorno en el yaml template declaradas 
# 6. sam local start-api
# 7. Accesible by clicking http://127.0.0.1:3000/app_cranealpatientdates
# 8. sam package  --s3-bucket  cranealpatientdates
# 9. sam deploy  --stack-name cranealpatientdates --capabilities CAPABILITY_IAM 
#   ó
# sam deploy  --s3-bucket cranealpatientdates --stack-name cranealpatientdates --capabilities CAPABILITY_IAM
# ó 

# 9. sam deploy --guided
# 10 aws cloudformation delete-stack --stack-name cranealpatientdates


#{
#  "Records": [
#    {
#      "eventVersion": "2.1",
#      "eventSource": "aws:s3",
#      "awsRegion": "us-east-2",
#      "eventTime": "2019-09-03T19:37:27.192Z",
#      "eventName": "ObjectCreated:Put",
#      "userIdentity": {
#        "principalId": "AWS:AIDAINPONIXQXHT3IKHL2"
#      },
#      "requestParameters": {
#        "sourceIPAddress": "205.255.255.255"
#      },
#      "responseElements": {
#        "x-amz-request-id": "D82B88E5F771F645",
#        "x-amz-id-2": "vlR7PnpV2Ce81l0PRw6jlUpck7Jo5ZsQjryTjKlc5aLWGVHPZLj5NeC6qMa0emYBDXOo6QBU0Wo="
#      },
#      "s3": {
#        "s3SchemaVersion": "1.0",
#        "configurationId": "828aa6fc-f7b5-4305-8584-487c791949c1",
#        "bucket": {
#          "name": "lambda-artifacts-deafc19498e3f2df",
#          "ownerIdentity": {
#            "principalId": "A3I5XTEXAMAI3E"
#          },
#          "arn": "arn:aws:s3:::lambda-artifacts-deafc19498e3f2df"
#        },
#        "object": {
#          "key": "b21b84d653bb07b05b1e6b33684dc11b",
#          "size": 1305107,
#          "eTag": "b21b84d653bb07b05b1e6b33684dc11b",
#          "sequencer": "0C0F6F405D6ED209E1"
#        }
#      }
#    }
#  ]
#}

#2020-11-18T14:35:13.483+01:00	Received event: {

#2020-11-18T14:35:13.483+01:00	"Records": [

#2020-11-18T14:35:13.483+01:00	{

#2020-11-18T14:35:13.483+01:00	"eventVersion": "2.1",

#2020-11-18T14:35:13.483+01:00	"eventSource": "aws:s3",

#2020-11-18T14:35:13.483+01:00	"awsRegion": "eu-central-1",

#2020-11-18T14:35:13.483+01:00	"eventTime": "2020-11-18T13:34:56.155Z",

#2020-11-18T14:35:13.483+01:00	"eventName": "ObjectCreated:Put",

#2020-11-18T14:35:13.483+01:00	"userIdentity": {

#2020-11-18T14:35:13.483+01:00	"principalId": "A20AGLL49R09W5"

#2020-11-18T14:35:13.483+01:00	},

#2020-11-18T14:35:13.483+01:00	"requestParameters": {

#2020-11-18T14:35:13.483+01:00	"sourceIPAddress": "83.38.61.33"

#2020-11-18T14:35:13.483+01:00	},

#2020-11-18T14:35:13.483+01:00	"responseElements": {

#2020-11-18T14:35:13.483+01:00	"x-amz-request-id": "76C3BED81A4A7575",

#2020-11-18T14:35:13.483+01:00	"x-amz-id-2": "t5Z4l8kFxNdi8cRTMy0ckgy1+ygFF/6McxMD4znvhUiL6WufY8PaWOO5dtTOSOlRrOHRdEcwS3LnB5kgo6MZjuyY7uGf/raD"

#2020-11-18T14:35:13.483+01:00	},

#2020-11-18T14:35:13.483+01:00	"s3": {

#2020-11-18T14:35:13.483+01:00	"s3SchemaVersion": "1.0",

#2020-11-18T14:35:13.483+01:00	"configurationId": "20315740-5535-47f7-b66e-d945ab72e777",

#2020-11-18T14:35:13.483+01:00	"bucket": {

#2020-11-18T14:35:13.483+01:00	"name": "appcranealpatientdates",

#2020-11-18T14:35:13.483+01:00	"ownerIdentity": {

#2020-11-18T14:35:13.483+01:00	"principalId": "A20AGLL49R09W5"
#
#2020-11-18T14:35:13.483+01:00	},
#
#2020-11-18T14:35:13.483+01:00	"arn": "arn:aws:s3:::appcranealpatientdates"

#2020-11-18T14:35:13.483+01:00	},

#2020-11-18T14:35:13.483+01:00	"object": {

#2020-11-18T14:35:13.483+01:00	"key": "CoverLetter_DAVID_NEVADO.pdf",

#2020-11-18T14:35:13.483+01:00	"size": 266308,

#2020-11-18T14:35:13.483+01:00	"eTag": "6ef3b7ef44b22f77d356d4569f9c839d",

#2020-11-18T14:35:13.483+01:00	"sequencer": "005FB52301029DF3EB"

#2020-11-18T14:35:13.483+01:00	}

#2020-11-18T14:35:13.483+01:00	}

#2020-11-18T14:35:13.483+01:00	}

#2020-11-18T14:35:13.483+01:00	]

#2020-11-18T14:35:13.483+01:00	}


print('Loading function')

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    """Sample pure Lambda function
    
    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    print ("Loading function ")
    # ,
    # "MB": context.memory_limit_in_mb,
    #         "log_stream_name": context.log_stream_name
    TargetBucket_EnvVar = os.environ['TargetBucket'] 
    SnsTopicARN =  os.environ['TopicArn'] 
    TablePatientsData_EnvVar = os.environ['PatientsDynamoTable'] 
    if not TargetBucket_EnvVar:
        TargetBucket_EnvVar = "appcranealpatientdates"
    if not SnsTopicARN or not SnsTopicARN in  "arn":
        SnsTopicARN = "arn:aws:sns:eu-central-1:291573578422:AppCranealPatientDatesSNSTopic" # local mode     
    if not TablePatientsData_EnvVar:
        TablePatientsData_EnvVar = "appcranealpatientdates" # local mode             
    print ("Sending message to SNS ARN:" + SnsTopicARN)           
    # Return a dict object 
    patiensData = dump_patientdata(TablePatientsData_EnvVar,dynamodb)    
    strData = json.dumps(patiensData)
    print(strData)   
    # https://s3.console.aws.amazon.com/s3/buckets/appcranealpatientdates?region=eu-central-1&tab=objects 
    urlBucketToLogin = "https://s3.console.aws.amazon.com/s3/buckets/" +  TargetBucket_EnvVar + "?region=eu-central-1&tab=objects"
    # json no empty , to improve 
    if len(strData)>4:            
        publish_sns_topic(SnsTopicARN, strData)        
    else:
        patiensData  = '{"Message": "No new data found  to be processed. <br> Upload a CSV file with headers name;traumadate ex.  DNM2;2020-01-01 to ' + urlBucketToLogin  + '"}'  
        strData   =  json.loads(patiensData)
    return {
        "statusCode": 200,
        'headers': { 'Content-Type': 'application/json' },
        "body": strData
    }
