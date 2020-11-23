import boto3
from datetime import *

def dict_to_item(raw):
    if isinstance(raw, dict):
        return {
            'M': {
                k: dict_to_item(v)
                for k, v in raw.items()
            }
        }
    elif isinstance(raw, list):
        return {
            'L': [dict_to_item(v) for v in raw]
        }
    elif isinstance(raw, str):
        return {'S': raw}
    elif isinstance(raw, int):
        return {'N': str(raw)}

def put_patientdata(name, traumadate,  accidentdatetable,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table(accidentdatetable)
    response = table.put_item(
       Item={
            'name': name,
            'traumadate': traumadate           
        }
    )
    return response

def load_patientdatas(patientsJson, accidentdatetable,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table(accidentdatetable)     
    for patient in patientsJson:
        name =  patient['name']
        traumadate = patient['traumadate']
        dt_traumadate = datetime.strptime(traumadate, '%Y-%m-%d')        
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

def create_patientdata_table(accidentdatetable,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName=accidentdatetable,
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'traumadate',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'traumadate',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    return table

# Query field dates that match today 
def query_patientdata(date, accidentdatetable,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table(accidentdatetable)
    response = table.query(
        KeyConditionExpression=Key('year').eq(year)
    )
    return response['Items']

def dump_patientdata(accidentdatetable,dynamodb=None):
    results = []
    print (accidentdatetable)
    last_evaluated_key = None
    table = dynamodb.Table(accidentdatetable.lower())
    response = table.scan()
    print  (response)
    data = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return data
    print  (data)

# Usage

# do something with data 