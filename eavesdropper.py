import tweepy
import json
import pykafka
import sys
import afinn

class Eavesdropper:
    def __init__(self):
        self.client = pykafka.KafkaClient("localhost:9092")
        self.producer = self.client.topics[bytes('twitter', 'ascii')].get_producer()

    def on_data(self, data):
        try:
            json_data = json.loads(data)
            send_data = '{}'
        except KeyError:
            return True
    
    def on_error(self, status):
        print(status)
        return True

if __name__ == "__main__":
    word = sys.argv[1]

    # afinn object for sentiment analysis
    afinn = Afinn()

    twitter_stream = tweepy.Stream(auth, Eavesdropper())
    twitter_stream.filter(languages = ['en'], track = [word])