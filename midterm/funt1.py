import boto3, os, sys, json
from urllib.parse import unquote_plus

s3 = boto3.resource('s3', verify=False)
sns = boto3.client('sns', verify=False)
sqs = boto3.client('sqs', verify=False)
sqs_res = boto3.resource('sqs', verify=False)
s3_client = boto3.client('s3', verify=False)


# List topics with ARNs
def get_topics():
    topics = sns.list_topics()
    arns = [t['TopicArn'] for t in topics['Topics']]
    names = [t.split(":")[-1] for t in arns]
    names2arns = dict(zip(names, arns))
	print("names2arns")
	print(names2arns)
    return names2arns 

# Returns 
def get_queues(prefix):
    qs = sqs.list_queues(QueueNamePrefix=prefix)
    if 'QueueUrls' in qs:
        urls = qs['QueueUrls']
        names = [q.split("/")[-1] for q in urls]
        names2urls = dict(zip(names, urls))
        return names2urls

# Format message for output
def format_message(data, quote, period, form):

	ar1 = []
	for line in data.splitlines(): 
		if line == '': continue
		msg = line.replace('"', '')[:-1]
		ar1.append(msg.split(','))
	
	quote_index = ar1[0].index(f'<{form}>')

	lamda_key = lambda x: (x[2], x[3])	
	ehh = sorted(ar1, key=lamda_key)

	ar1 = [ar1[0]]
	ar1[0].insert(2, '<AVG_TYPE>')
	ar1[0].insert(3, '<QUOTE>')
	ar1[0].insert(10, '<AVERAGE>')
	[ar1[0].remove(x) for x in ['<OPEN>', '<HIGH>', '<LOW>', '<CLOSE>', '<OPENINT>']]

	price_quote_data = 0
	for array in ehh[:-1]:
		n = (ehh.index(array)+1)
		price_quote_data += float(array[quote_index])
		array.insert(2, f'SMA{period}')
		array.insert(3, form)
		array.insert(10, str(round(price_quote_data/n, 2)))
		del array[6:10]
		del array[8]
		ar1.append(array)
	return ar1

        
# Read from queue
def read_from_queue(prefix, quote, period, form):
	topics = get_topics()
	queues = get_queues(prefix)
	for queue in queues:
		queue_url = (sqs.get_queue_url(QueueName=queue))['QueueUrl']
		strdata=""""""
		while True:
			try:
				data = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10, WaitTimeSeconds=3)['Messages']
				for message in data:
					handle = message['ReceiptHandle']
					msg = message['Body'].splitlines()[5].split(':')[1]
					sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=handle)
					print("4MSGINDATA: "+msg)
					strdata += msg
			except KeyError: 
				print("This queue is empty!")
				parsed = format_message(strdata, quote, period, form)
				break
	return parsed

def lambdaHandler(event, context):
	print("hihaisdahsdjasjdasjdh")
	for record in event['Records']:
		msg = record['Sns']['Message']
		msg = msg[1:-1]
		print ("msg")
		print(msg)
		print ("ar1")
		print(ar1)
		ar1 = []
		[ar1.append(x) for x in msg.split(',')]
		data = read_from_queue(ar1[0], ar1[1], ar1[2], ar1[3].strip())
		
		data = str(data).encode('utf-8')
		bucket = 'mffff-alice-results'
		filename = f'alice-{ar1[1]}-ma50'

		s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint':'us-east-1'})
		s3.Object(bucket, filename).put(Body=data)
		














