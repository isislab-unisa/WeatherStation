import boto3
import datetime
import random

dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")

table = dynamodb.Table('Campania')

cities = [('Salerno', 5), ('Caserta', 3), ('Napoli', 6), ('Benevento', 2), ('Avellino', 3)]

device_ids = []

for city, device_id in cities:
    city_devices = ""
    for i in range(device_id):
        city_devices = city_devices + ("%s_%s") % (city, str(i)) + " "
    device_ids.append(city_devices)

for i in range(len(cities)):
    measure_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperature = round(random.uniform(2.0, 25.0), 2)
    item = {
        'city': cities[i][0],
        'measure_date': str(measure_date), 
        'temperature': str(temperature),
        'device_id': device_ids[i]
    }
    table.put_item(Item=item)

    print("Stored item", item)
