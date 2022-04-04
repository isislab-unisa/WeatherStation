import boto3
import datetime
import random

sqs = boto3.resource('sqs', endpoint_url='http://localhost:4566')

cities = [('Salerno', 5), ('Caserta', 3), ('Napoli', 6), ('Benevento', 2), ('Avellino', 3)]

for city, device_id in cities:
	queue = sqs.get_queue_by_name(QueueName=city)
	measure_date = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	for i in range(device_id):
		if random.random() < 0.10:
			error_queue = sqs.get_queue_by_name(QueueName="Errors")
			error_msg = '{"device_id": "%s_%s","error_date": "%s"}' % (city, str(i), measure_date)
			print(error_msg)
			error_queue.send_message(MessageBody=error_msg)
		else: 
			temperature = round(random.uniform(2.0, 25.0), 2)
			msg_body = '{"device_id": "%s_%s","measure_date": "%s","city": "%s","temperature": "%s"}' \
				% (city, str(i), measure_date, city, str(temperature))
			print(msg_body)
			queue.send_message(MessageBody=msg_body)