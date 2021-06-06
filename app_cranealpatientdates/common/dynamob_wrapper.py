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

def validate_patientdatas(patientsJson):
    try:    
        returnMessage = ""
        for patient in patientsJson:
            
            # check if all fields are there 
            # if not ('name' in patient and  'traumadate' in patient and  'sampletype' in patient and  'type' in patient and  'hnumber' in patient):                
            #    print("Some of the required fields are missing")
            #    return "Some of the required fields are missing"; 

            # name =  patient['name']
            traumadate = patient['traumadate']
            sampletype = patient['sampletype']
            type_d = patient['type']
            history_number = patient['hnumber']
            dt_traumadate = datetime.strptime(traumadate, '%Y-%m-%d')        
            #Add 1 day.        
            # 48 y  72h, 10, 180 y 365 dias
            traumadate_48h  = {"traumadate_48h" :   datetime.strftime(dt_traumadate + timedelta(days=2),'%Y-%m-%d')}
            patient.update(traumadate_48h)
            #y = {"pin":110096} 
            # YYYY-MM-DD
            history_number  = {"hnumber" :   patient['hnumber']}
            patient.update(history_number)
            sampletype  = {"sampletype" :   patient['sampletype']}
            patient.update(sampletype)
            type_d  = {"type_d" :   patient['type_d']}
            patient.update(type_d)
            traumadate_72h  = {"traumadate_72h" :   datetime.strftime(dt_traumadate + timedelta(days=3),'%Y-%m-%d')}
            patient.update(traumadate_72h)
            traumadate_10d  = {"traumadate_10d" :   datetime.strftime(dt_traumadate + timedelta(days=10),'%Y-%m-%d')}
            patient.update(traumadate_10d)
            traumadate_180d  = {"traumadate_180d" : datetime.strftime(dt_traumadate + timedelta(days=180),'%Y-%m-%d')}
            patient.update(traumadate_180d)
            traumadate_360d  = {"traumadate_360d" : datetime.strftime(dt_traumadate + timedelta(days=360),'%Y-%m-%d')}
            patient.update(traumadate_360d)    

        return returnMessage
    except Exception as e:        
        print('Failed to process:', e)
        #responseStatus = '{"MessageError": "' + str(e) + '"}' 
        #print(json.loads(responseStatus))    
        #responseData = {'Failure': 'Something bad happened.'}

def load_patientdatas(patients, accidentdatetable,dynamodb=None):
    #if not dynamodb:
    #   table  = create_patientdata_table(accidentdatetable)
        # dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table(accidentdatetable)    
    scan = table.scan()
    with table.batch_writer() as batch:
        for each in scan['Items']:
            
            print ("Deleting : ",each['name'])
            
            batch.delete_item(
                Key={
                    'name': each['name'],
                    'traumadate': each['traumadate']
                }
            )
    
    table = dynamodb.Table(accidentdatetable)    
    # for patient in patientsJson:
    for index, patient in patients.iterrows():  
        # name =  patient['name']

        jsondata = {}
        dt_traumadate   = datetime.strptime(patient['traumadate'], '%Y-%m-%d')    
        traumadate      = datetime.strftime(dt_traumadate,'%Y-%m-%d')   
        traumadate_48h  = datetime.strftime (dt_traumadate + timedelta(days=2),'%Y-%m-%d')   
        traumadate_72h  = datetime.strftime (dt_traumadate + timedelta(days=3),'%Y-%m-%d')
        traumadate_10d  = datetime.strftime (dt_traumadate + timedelta(days=10),'%Y-%m-%d')
        traumadate_180d = datetime.strftime (dt_traumadate + timedelta(days=180),'%Y-%m-%d')
        traumadate_360d = datetime.strftime (dt_traumadate + timedelta(days=360),'%Y-%m-%d')
        
        
        jsondata['name']     = patient['name']
        jsondata['traumadate']     = traumadate
        jsondata['sampletype']     = patient['sampletype']
        jsondata['type_d']         = patient['type_d']        
        jsondata['hnumber']        = patient['hnumber']
        jsondata['traumadate_48h'] = traumadate_48h
        jsondata['traumadate_72h'] = traumadate_72h
        jsondata['traumadate_10d'] = traumadate_10d
        jsondata['traumadate_180d'] = traumadate_180d
        jsondata['traumadate_360d'] = traumadate_360d
        
        table.put_item(Item=jsondata)

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
                'AttributeType': 'S '
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