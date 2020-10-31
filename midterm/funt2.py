import boto3, os, sys
from urllib.parse import unquote_plus

s3 = boto3.resource('s3', verify=False)
sns = boto3.client('sns', verify=False)
sqs = boto3.client('sqs', verify=False)
sqs_res = boto3.resource('sqs', verify=False)
s3_client = boto3.client('s3', verify=False)

#### FUNCTIONS ####

# Create a topic
def create_topic( name ):
    print("sns.create_topic(): ", name, end=' >> ')
    topic = sns.create_topic( Name=name )
    print( topic['TopicArn'] )
    return topic

# Create a queue
def create_queue( name ):
    print("sns.create_queue(): ", name, end=' >> ')
    q = sqs.create_queue(QueueName=name)
    print( q['QueueUrl'] )
    return q


# Produces a policy that allows SNS to send message to an SQS queue
def policy_allow_sns_to_sqs(topic_arn, queue_arn):
    policy = """{{
    "Version":"2012-10-17",
        "Statement":[
            {{
            "Sid":"AllowSNStoSQS",
            "Effect":"Allow",
            "Principal" : {{"AWS" : "*"}},
            "Action":"SQS:SendMessage",
            "Resource": "{}",
            "Condition":{{
                "ArnEquals":{{
                "aws:SourceArn": "{}"
                }}
                }}
            }}
        ]
        }}""".format(queue_arn, topic_arn)
    return policy


# Create topic and queue by the same name and subscribe q to topic
def setup_sns_sqs( name ):
    topic = create_topic(name)
    create_queue(name)
    q = sqs_res.get_queue_by_name(QueueName=name)
    q_attr = q.attributes

    res = sqs.set_queue_attributes( 
        QueueUrl = sqs.get_queue_url( QueueName=name)['QueueUrl'],
        Attributes = {
            'Policy' : policy_allow_sns_to_sqs( topic['TopicArn'], q_attr['QueueArn'])
        }
    )
    print("subscribe(sns->sqs): ", name, end=' >> ')
    sub = sns.subscribe( TopicArn=topic['TopicArn'], Protocol='sqs', Endpoint=q_attr['QueueArn'], ReturnSubscriptionArn=True )
    print( sub['SubscriptionArn'] )
    return sub


# 
def datasorter(file_data, file_name):
	sub = setup_sns_sqs('alice-'+file_name)
	for row in file_data.splitlines():
		if row == '': continue
		else: sending = sns.publish(TopicArn=sub[1], Message=str(row), Subject='Data')


def lambdaHandler(event, context):
	for record in event['Records']:
		bucket = record['s3']['bucket']['name']
		key = unquote_plus(record['s3']['object']['key'])
		data_obj = s3_client.get_object(Bucket=bucket, Key=key)
		data = data_obj['Body'].read().decode()
		datasorter(data, key.split('-')[1])

