import boto3
import datetime
import json

def lambda_handler(event, context):
	sqs = boto3.resource('sqs', endpoint_url='http://localhost:4566')
	dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

	table = dynamodb.Table('Campania')

	cities = ['Salerno', 'Caserta', 'Napoli', 'Benevento', 'Avellino']

	for city in cities:
		queue = sqs.get_queue_by_name(QueueName=city)
		messages = []
		while True:
			response = queue.receive_messages(MaxNumberOfMessages=10, VisibilityTimeout=10, WaitTimeSeconds=10)
			if response:
				messages.extend(response)
				device_ids = ""
				avg_temperature = 0
				last_measured_data = datetime.datetime.combine(datetime.date.min, datetime.datetime.min.time())
				for message in messages:
					content = json.loads(message.body)
					device_ids = device_ids + content["device_id"] + " "

					measure_data = datetime.datetime.strptime(content["measure_date"], "%Y-%m-%d %H:%M:%S")
					if measure_data > last_measured_data:
						last_measured_data = measure_data

					avg_temperature += float(content["temperature"])
					message.delete()

				avg_temperature = round(avg_temperature / len(messages), 2)
				item = {
					'city': city,
					'measure_date': str(last_measured_data), 
					'temperature': str(avg_temperature),
					'device_id': device_ids
				}
				table.put_item(Item=item)
			else:
				break	