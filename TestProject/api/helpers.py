import json

from kafka import KafkaProducer


producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send_to_kafka(message_id, message):
    producer.send('message', {message_id: message})
    producer.flush()