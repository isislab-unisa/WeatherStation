import requests
import boto3
import datetime
import json

def lambda_handler(event, context):
	key = "<insert-your-IFTT-key-here"
	url = "https://maker.ifttt.com/trigger/email_error/with/key/"+key
	for record in event['Records']:
		payload = record['body']
		payload = json.loads(str(payload))
		device_id = payload['device_id']
		error_date = payload['error_date']
		req = requests.post(url, json={"value1": device_id, "value2": error_date})
