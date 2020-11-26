import boto3
import pandas as pd 

from decimal import Decimal
import json
import boto3
import requests

from    datetime import * 


def load_movies(patients, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('appcranealpatientdates')
    for patient in patients:
        
        name =  patient['name']        
        traumadate = patient['traumadate']
        dt_traumadate = datetime.strptime(traumadate, '%Y-%m-%d')
        print (dt_traumadate)
        #Add 1 day.
        

        # 48 y  72h, 10, 180 y 365 dias
        traumadate_48h  = {"traumadate_48h" :   datetime.strftime(dt_traumadate + timedelta(days=2),'%Y-%m-%d')}
        patient.update(traumadate_48h)
        #y = {"pin":110096} 
        # YYYY-MM-DD
        traumadate_72h  = {"traumadate_72h" :   datetime.strftime(dt_traumadate + timedelta(days=3),'%Y-%m-%d')}
        patient.update(traumadate_72h)
        traumadate_10d  = {"traumadate_10d" :   datetime.strftime(dt_traumadate + timedelta(days=10),'%Y-%m-%d')}
        patient.update(traumadate_10d)
        traumadate_180d  = {"traumadate_180d" : datetime.strftime(dt_traumadate + timedelta(days=180),'%Y-%m-%d')}
        patient.update(traumadate_180d)
        traumadate_360d  = {"traumadate_360d" : datetime.strftime(dt_traumadate + timedelta(days=360),'%Y-%m-%d')}
        patient.update(traumadate_360d)
        #print (patient)
        table.put_item(Item=patient)



def dump_patientdata(accidentdatetable,dynamodb=None):
    results = []
    last_evaluated_key = None
    table = dynamodb.Table(accidentdatetable.lower())
    response = table.scan()
    #print  (response)
    data = response['Items']    
    listPatient = {}
    print  (response['Items'])    
    for patient in response['Items']:   

        today = date.today()
        formatted_today = date.today().strftime('%Y-%m-%d')             
        revision_message = ""
        founded = False
        if formatted_today == patient["traumadate_48h"]: 
            revision_message  = "Revision found for 48h" 
            founded = True
        if formatted_today == patient["traumadate_72h"]: 
            revision_message  = "Revision found for 72h" 
            founded = True
        if formatted_today == patient["traumadate_10d"]: 
            revision_message  = "Revision found for 10 days" 
            founded = True
        if formatted_today == patient["traumadate_180d"]: 
            revision_message  = "Revision found for 180 days" 
            founded = True
        if formatted_today == patient["traumadate_360d"]: 
            revision_message  = "Revision found for 360 days"                         
            founded = True
        if founded:                 
            listPatient[patient["name"]] = revision_message
    #response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        #data.extend(response['Items'])
    print  (listPatient)            

    return json.dumps(listPatient)    

def dump_patientdata2(accidentdatetable,dynamodb=None):
    dynamo_table = boto3.resource('dynamodb').Table(accidentdatetable)
    response = dynamo_table.scan()

    dictPatients = response # the response is in the form of a dictionary

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        dictPatients.update(response)

    listPatient = {}        
    for patient in dictPatients['Items']:   

        today = date.today()
        formatted_today = date.today().strftime('%Y-%m-%d')             
        revision_message = ""
        founded = False
        if formatted_today == patient["traumadate_48h"]: 
            revision_message  = "Revision found for 48h" 
            founded = True
        if formatted_today == patient["traumadate_72h"]: 
            revision_message  = "Revision found for 72h" 
            founded = True
        if formatted_today == patient["traumadate_10d"]: 
            revision_message  = "Revision found for 10 days" 
            founded = True
        if formatted_today == patient["traumadate_180d"]: 
            revision_message  = "Revision found for 180 days" 
            founded = True
        if formatted_today == patient["traumadate_360d"]: 
            revision_message  = "Revision found for 360 days"                         
            founded = True
        if founded:                 
            listPatient[patient["name"]] = revision_message
    print("listPatient:")
    print(listPatient)
    return listPatient

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')
    patiensData = dump_patientdata2("appcranealpatientdates",dynamodb)
    print (patiensData)
    if "name" in patiensData:        
        print ("exists")        
        print ("Sending SNS")
    else:
        patiensData  = '{"Message": "No new data found"}'         
    print (json.loads(json.dumps(patiensData)))
    

