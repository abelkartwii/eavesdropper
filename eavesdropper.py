import sys
import pykafka
import json
from afinn import Afinn
from tweepy import OAuthHandler, Stream, StreamListener

class Eavesdropper:
    def __init__(self):
        self.client = pykafka.KafkaClient("localhost:9092")
        self.producer = self.client.topics[bytes('twitter', 'ascii')].get_producer()

    def on_data(self, data):
        try:
            json_data = json.loads(data)
            send_data = '{}'
            json_send_data = json.loads(send_data)
        except KeyError:
            return True
    
    def on_error(self, status):
        print(status)
        return True
