import sys
import json
import afinn
import tweepy
import time
import kafkaProducer
# from pykafka import KafkaClient, Producer, Cluster, Broker
from tweepy import OAuthHandler, Stream, StreamListener
from geopy.geocoders import Nominatim
from country_bounding_boxes import country_subunits_containing_point

# geolocator object to find locations
geolocator = Nominatim(user_agent = "eavesdropper")

class Eavesdropper(StreamListener):
    def __init__(self, topic, location):
        """
        Initializes coordinates and bounding boxes for the specified 
        location, as well as creating a Kafka producer.
        """

        self.topic = topic
        print(f"Creating a Kafka topic for {topic}...")
        self.producer = kafkaProducer

        # finds lat/long of location
        self.location = geolocator.geocode(str(location))
        self.longitude = self.location.longitude
        self.latitude = self.location.latitude

        # finds country and bounding box of location based on long/lat
        self.country = [c.name for c in country_subunits_containing_point(self.longitude, self.latitude)][0] # returns a string "Country"
        self.countrybox = [c.bbox for c in country_subunits_containing_point(self.longitude, self.latitude)] # returns tuple with bounds

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

        # coordinates
        try json_data.get['coordinates']:
            self.producer.send("eavesdropper_coordinates", json_data.encode('utf-8'))
            # tweet_data = {'created_at' : json_data['created_at'],
            #              'expanded_url' : json_data['entities']['urls'][0]['expanded_url']}
            # data = json.dumps(tweet_data)
            # self.producer.produce(bytes(data, "ascii"))
            print(data)
            return True

        except KeyError:
            print("Key error -- no coordinates were detected")
            return False

        except Exception:
            print("No data detected -- try again")
            return False
    
    def on_status(self, status):
        print(status.text)
        return True

    def on_limit(self, status):
        """
        Once requests exceed the limit set by the Twitter API,
        pauses the app for a minute before resuming.
        """
        print("Rate limit exceeded!")
        print("Waiting for a minute...")
        time.sleep(60)
        print("Resuming!")
        return True

    def on_error(self, status):
        if status == 420:
            print("Too many attempts - please wait")
        return False # disconnects stream

    def on_exception(self, status):
        print(status)
        return True