from pprint import pprint
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table_name = "Campania"

print("Hi, this is the WeatherStation application.")
print("Enter the name of one or more cities you want to know the temperature")
cities = input("(cities must be separated by one space):\n")
cities = cities.split()
table = dynamodb.Table(table_name)
print("------------------------------------------------------------------------------------------------")
for city in cities:
	try:
		response = table.get_item(Key={'city': city})
	except ClientError as e:
		print(e.response['Error']['Message'])

	print("Average temperature in %s is %s" 
		% (response['Item']['city'], response['Item']['temperature']))
	print("-measured at %s" 
		% (response['Item']['measure_date']))
	print("--based on the following devices", response['Item']['device_id'])
	print("------------------------------------------------------------------------------------------------")
