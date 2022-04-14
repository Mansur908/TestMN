import ast
import requests
from django.conf import settings

from django.core.management import BaseCommand
from kafka import KafkaConsumer


class Command(BaseCommand):
    help = "Kafka listener"

    def handle(self, *args, **options):
        consumer = KafkaConsumer('message', bootstrap_servers='kafka:9092')
        for msg in consumer:
            # Преобразование в обычный словарь
            dict_str = msg.value.decode("UTF-8")
            my_data = ast.literal_eval(dict_str)
            str_dictionary = repr(my_data)
            dictionary = eval(str_dictionary)

            key = list(dictionary.keys())[0]
            value = dictionary.get(key)

            string = value.lower()
            substring = "абракадабра"
            if string.find(substring) == -1:
                status = True
            else:
                status = False
            try:
                # Получаем JWT токен
                r = requests.post('http://localhost:8000/api/v1/jwt/', {"secret": settings.SECRET_KEY})
                token = eval(r.content).get('token')
                # Добавляем JWT токен в заголовок
                header = {'Authorization': token}
                requests.post(url='http://localhost:8000/api/v1/message_confirmation/', data={"message_id": key, "success": status}, headers=header)
            except Exception:
                print("error sending request")
