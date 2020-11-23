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
        if name =="DNM" 
            and  name =="DNM":
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

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')
    #movie_table = create_movie_table(dynamodb)
    #print("Table status:", movie_table.table_status)
    df3 = pd.read_csv('Patientscsv.csv',delimiter=';', header=1, names=('name', 'traumadate'))  
    df2 = pd.read_csv('Patientscsv.csv',delimiter=';', header=1, names=('name', 'traumadate'))  
    js = df3.to_json(orient="records")
    print (json.loads(js))
    
    
    # movie_list2 = json.load(json_list)

    #with open("./patients.json") as json_file:
    #    movie_list = json.load(json_file, parse_float=Decimal)
    load_movies(json.loads(js),dynamodb)


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

#s3 = boto3.client('s3')        
#obj = s3.get_object(Bucket='appcranealpatientdates', Key='PatientsData.csv')
#df = pd.read_csv(obj['Body'])  
#df2 = pd.read_csv('Patientscsv.csv',delimiter=';', header=1, names=('Name', 'TraumaDate'))    
#print (df2.head())
#print(dict_to_item(df2.to_dict()))
#for index,patient in df2.iterrows():
#        name = patient['Name']
#        traumadate = patient['TraumaDate']  
#        print("Adding patient:", name, traumadate)
#        print(dict_to_item(patient.to_dict()))
