import boto3

# Create an SNS client
sns = boto3.client('sns')

def create_sns_topic(Name):
    response = sns.create_topic(Name)

def exists_sns_topic(SNSArn):
    response = sns.list_topics()    
    # Get a list of all topic ARNs from the response
    for topic in response['Topics']:
        if item['TopicArn'] == SNSArn:
            return True
    return False

def publish_sns_topic(SNSArn, SNSMessage):
    response = sns.publish(
        TopicArn=SNSArn,    
        Message=SNSMessage
    )



# Publish a simple message to the specified SNS topic
#response = sns.publish(
#    TopicArn='arn:aws:sns:region:0123456789:my-topic-arn',    
#    Message='Hello World!',    
#)

# Print out the response
#sns = boto3.client('sns')

#response = sns.list_topics()
#for item in response['Topics']:
#    print(item['TopicArn'])
#    print(sns.get_topic_attributes(TopicArn=item['TopicArn']))
#    suscription = sns.get_topic_attributes(TopicArn=item['TopicArn'])
#    #suscription["Attributes"][]


#publish_sns_topic('arn:aws:sns:eu-central-1:291573578422:appcranealpatientdates', 'hELLO')    