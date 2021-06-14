import os
import sys
import json
import requests
from kafkaProducer import producer
from eavesdropper import Eavesdropper
from textblob import TextBlob
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

COORDS = Eavesdropper.location
COUNTRYBOX = Eavesdropper.countrybox

def clean_text(tweet):
    """
    Deals with non-ASCII characters in tweet text, and 
    returns the cleaned text in UTF-8 format.
    """
    clean = re.sub(r'[^\x00-\x7f]', r'', tweet_text)
    returned clean.encode('utf-8')

def sentiment(tweet):
    """
    Uses the TextBlob module to calculate the sentiment of
    the tweet. If a tweet falls within a certain range,
    this method returns the actual sentiment score with
    the classifier.
    e.g. (-0.758, 'very negative')
    """
    polarity = TextBlob(tweet).sentiment.polarity
    if polarity > 0.25:
        return (polarity, "positive")
    elif polarity < -0.25:
        return (polarity, "negative")
    else:
        return (polarity, "neutral")

def kafka_sender(messages):
    """
    Uses the Kafka producer setup in kafkaProducer.py to receive
    messages sent from the twitter sentiment stream.???
    """
    for message in messages:
        producer.send("twitter_sentiment_stream", bytes(message))
    producer.flush()

topic = "Eavesdropper"
spark_conf = SparkConf().setAppName(topic).setMaster("local[1]") # configures spark app as "Eavesdropper", runs locally with 1 core

# spark context
spark_context = SparkContext(conf = spark_conf) # connects to a Spark cluster
spark_context.setLogLevel("WARN") # logs config as WARN

spark_streaming = StreamingContext(spark_context, interval = 5) # picks up new tweets from stream every 5 seconds

##### this is for stream without coordinates
kafka_stream = KafkaUtils.createDirectStream(
    spark_streaming, topic, {
    "bootstrap.servers" : "localhost:9092",
    "group.id" : "twitter",
    "fetch.message.max.bytes" : "15728640",
    "auto.offset.rest" : "largest"
})

tweets = kafkaStream. \
    map(lambda (k, v): json.loads(v)). \
    map(lambda json_object: (json_object["user"]["screen_name"],
                             COUNTRYBOX,
                             clean_text(json_object["text"]), 
                             tweet_sentiment(clean_text(json_object["text"]))))

# prints tweets to console
tweets.pprint(10)
tweets.persist(StorageLevel.MEMORY_AND_DISK)

##### for the noes with coordinates
kafka_coords_stream = KafkaUtils.createDirectStream(
    spark_streaming, topic, {
        "bootstrap.servers" : "localhost:9092",
        "group.id" : "twitter",
        "fetch.message.max.bytes" : "15728640",
        "auto.offset.rest" : "largest"
    }
)
tweets_coords = kafka_coords_stream. \
    map(lambda (k, v) : json.loads(v)). \
    map(lambda json_object: (json_object["user"]["screen_name"],
                             json_object["coordinates"]["coordinates"],
                             clean_text(json_object["text"]), 
                             tweet_sentiment(clean_text(json_object["text"]))))

tweet_coords.pprint(10)
tweet_coords.persist(StorageLevel.MEMORY_AND_DISK)

