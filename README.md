# Eavesdropper
## Overview
This project uses Kafka, Spark, and Flask to analyze and store the sentiments of a Twitter trend in a certain location. Input your location, and receive the sentiment status of the trending topics in your area, as well as the sentiment of it globally!

(For developing purposes, I will use Jakarta as my location)

## Workflow
**1. Ingest Twitter stream (Twitter Streams / Kafka)**
Using the `tweepy` Python module, tweets from the selected location will be pulled as JSON objects and inserted into an event stream that will be the input to three separate Kafka topics, which are:

1. a topic containing all tweets about the trend made in a certain location that are *geotagged* with precise coordinates (where the user has tweeted with GPS enabled)
2. a topic containing all tweets about the trend made in a certain location
3. a topic containing all tweets about the trend in the location's country, which is used to compare the differences in sentiment between locations. 

**2. Process Kafka topics (Kafka / Spark)**
The three Kafka topics in the first stage are then processed in this stage using Spark to create dataframes with a running total of tweets. Using the `textblob` Python module, this stage will create a new Kafka event stream (topic) of coordinates and sentiment levels, which will be published to the frontend at 15-second intervals.

**3. Front-end visualization (to-do)**
This stage uses Flask to consume data from Spark and the Kafka sentiment event stream.

## Configuration and Setup
This project utilizes [Docker](https://docs.docker.com/get-docker/) to create a consistent environment that can deploy the application easily. 

This project uses both a Dockerfile and Docker Compose. The Dockerfile is an image started from an Alpine image that is used to install Python and Java -- two environments required to run the project's requirements. To build a container, use
```
docker build -t eavesdropper .
``` 
and then run the built image:
```
docker run -d -p 8080:8080 eavesdropper:latest
```

In order to install the frameworks needed in this project, we will need to use docker-compose to build local images. To do so, run
```
docker-compose up
```
Kafka (and Zookeeper) and Spark will be installed in the container's root directory through this process.

## License
This theme uses the [MIT license](https://choosealicense.com/licenses/mit/).



'''
<!-- Run `eavesdropper.py` in your Spark directory with your desired topic in quotes. This will fetch the data from the Twitter API for Rina Sawayama:
```
python bin/spark-submit eavesdropper.py "Rina Sawayama"
```

This filter will select tweets that mention Rina Sawayama, and the data will be ingested to a Kafka producer. By default, the filter will only search for tweets in English; to change this, change `languages` under `main()` in `main.py` to the language of your choice.

**2. Analyze sentiments (PySpark / Kafka)**
Run `heartdropper.py`, which will run a sentiment analysis on our selected topic.

```
python heartdropper.py
```

**3. Storage (Cassandra)**
to-do...

**4. Visualization**
to-do...

##



## Configuration
The tools used in this project are:
* [Python](https://www.python.org/downloads/) 3.9.2
* [Apache Spark](https://spark.apache.org/downloads.html) 3.0.1 (namely PySpark and Spark Streaming)
* [Apache Kafka](https://kafka.apache.org/downloads) 2.7.0
* [Apache Cassandra](https://cassandra.apache.org/download/) 3.11
* [Twitter Stream API](https://developer.twitter.com/)

The required Python

Required Python modules: `pykafka`, `tweepy`, `textblob`.

To access Twitter data, create a Twitter API account [here](https://developer.twitter.com/en/apply-for-access) first, obtain the necessary keys, and place them in `config.cfg` as below.

```
consumer_key = <insert your consumer key here>
consumer_secret = <insert your consumer secret here>
access_token = <insert your access token here>
access_secret = <insert your access secret here>
```

You will need to start a Kafka server. On the Windows command line, run the following code in your Kafka directory to start the Kafka and Zookeeper servers, and to create the corresponding Kafka `eavesdropper` topic :
```
.\bin\windows\kafka-server-start.bat .\config\server\properties
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
.\bin\windows\kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic <eavesdropper>
```

You will also need to start Cassandra, which can be done by running the following code on the command line in your Cassandra directory:
```
.\bin\cassandra -f
```

## Approach -->
'''
