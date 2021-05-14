import sys
import json
import afinn
import tweepy
import kafkaProducer
# from pykafka import KafkaClient, Producer, Cluster, Broker
from tweepy import OAuthHandler, Stream, StreamListener

class Eavesdropper(StreamListener):
    def __init__(self, topic):
        self.topic = topic
        print(f"Creating a Kafka topic for {topic}...")
        self.producer = kafkaProducer

    """
    def __init__(self, topic):
        self.topic = topic
        print(f"Publishing data to topic: {topic}")
        self.broker = Broker(id_ = 1, host = "localhost", port = 9092, handler = "RequestHandler", socket_timeout_ms = 10000, offsets_channel_socket_timeout_ms = 10000)
        self.client = KafkaClient("localhost:9092")
        self.cluster = Cluster(hosts = "localhost:9092", handler = "RequestHandler")
        self.producer = Producer(cluster = cluster, topic = topic)
        # self.client.topics[bytes('twitter', 'ascii')].get_producer()
    """

    def on_data(self, data):
        print("Loading data...")
        json_data = json.loads(data)
        print(json_data['text'])
        if json_data['text']:
            tweet_data = {'created_at' : json_data['created_at'],
                          'expanded_url' : json_data['entities']['urls'][0]['expanded_url']}
            data = json.dumps(tweet_data)
            self.producer.produce(bytes(data, "ascii"))
            print(data)
            return True

        if KeyError:
            print("Key error -- no data detected")
            return False

        if Exception:
            print("No data detected -- try again")
            return False
    
    def on_status(self, status):
        print(status.text)

    def on_error(self, status):
        if status == 420:
            print("Too many attempts - please wait")
        return False # disconnects stream

    def on_exception(self, status):
        print(status)
        return True

"""
    def on_connect(self):
        print("Connected to Twitter!")
"""