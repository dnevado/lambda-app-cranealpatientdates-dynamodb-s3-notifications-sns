import boto3
import os
import json
from crhelper import CfnResource
from  common.dynamob_wrapper import *

#https://aws.amazon.com/es/blogs/infrastructure-and-automation/conditionally-launch-aws-cloudformation-resources-based-on-user-input/
#https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html 
print('Loading function')

dynamodb = boto3.resource('dynamodb')

helper = CfnResource()

@helper.create
@helper.update
def exists_dynamodb_table(event, context):

    TablePatientsData_EnvVar = os.environ['PatientsDynamoTable']     
    if not TablePatientsData_EnvVar:
        TablePatientsData_EnvVar = "appcranealpatientdates" # local mode             
    print (TablePatientsData_EnvVar)         

    helper.Data['DynamoDBExists'] = "TEST DYNAMODB VALIDATION"

@helper.delete
def no_op(_, __):
    pass

def handler(event, context):    
    helper(event, context)

