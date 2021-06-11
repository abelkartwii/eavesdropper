import os
import sys
import json
import requests
from kafkaProducer import producer
from textblob import TextBlob
from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

def text_sentiment(tweet):
    polarity = TextBlob(tweet).sentiment.polarity
    if polarity > 0.10:
        return (polarity, "positive")
    elif polarity < -0.10:
        return (polarity, "negative")
    else:
        return (polarity, "neutral")

def kafka_sender(messages):
    for message in messages:
        producer.send("twitter_sentiment_stream", bytes(message))
    producer.flush()

topic = "Eavesdropper"
spark_conf = SparkConf().setAppName("Eavesdropper")
spark_context = SparkContext(conf = spark_conf)
spark_streaming = StreamingContext(spark_context, interval = 5) # picks up new tweets from stream every 5 seconds

kafka_stream = KafkaUtils.createDirectStream(spark_streaming, topic, {
    "bootstrap.servers" : "localhost:9092",
    "group.id" : "twitter",
})

tweets = kafkaStream. \
    map(lambda (key, value): json.loads(value)). \
    map(lambda json_object: (json_object["user"]["screen_name"],
                             bounding_box(json_object["place"]["bounding_box"]["coordinates"]),
                             clean_text(json_object["text"]), 
                             tweet_sentiment(clean_text(json_object["text"]))))