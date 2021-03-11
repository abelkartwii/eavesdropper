import sys
import pykafka
import json
import afinn
import tweepy
from afinn import Afinn
from tweepy import OAuthHandler, Stream, StreamListener

class Eavesdropper:
    def __init__(self):
        print("Publishing data to topic: " + topic)
        self.client = pykafka.KafkaClient("localhost:9092")
        self.producer = self.client.topics[bytes('twitter', 'ascii')].get_producer()

    def on_data(self, data):
        try:
            json_data = json.loads(data)
            send_data = '{}'
            json_send_data = json.loads(send_data)
            json_send_data['text'] = json_data['text']
            json_send_data['senti_val'] = afinn.score(json_data['text'])

            print(json_send_data['text'], ">>>", json_send_data['senti_val'])

            self.producer.produce(bytes(json.dumps(json_send_data), 'ascii'))

            return True

        except KeyError:
            return True
    
    def on_error(self, status):
        print(status)
        return True

    def on_exception(self, status):
        print(status)
        return True

    def on_connect(self):
        print("Connected to Twitter!")
        return True