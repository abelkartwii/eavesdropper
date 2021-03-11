# Eavesdropper
## Overview
This project uses Python, PySpark, Kafka, and Cassandra to analyze and store the sentiments of a Twitter topic. Input the topic that you want to know the reception of, and receive the sentiment status of it!

## Configuration
The tools used in this project are:
* [Python](https://www.python.org/downloads/) 3.9.2
* [Apache Spark](https://spark.apache.org/downloads.html) 3.0.1 (namely PySpark and Spark Streaming)
* [Apache Kafka](https://kafka.apache.org/downloads) 2.7.0
* [Apache Cassandra](https://cassandra.apache.org/download/) 3.11
* [Twitter Stream API](https://developer.twitter.com/)

Required Python modules: `pykafka`, `tweepy`, `afinn`.

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

## Approach
This project is composed out of a few steps, with the tools being used in the headline. All steps are performed in Python!

**1. Ingest Twitter stream (Twitter Streams / PySpark / Kafka)**
Run `eavesdropper.py` in your Spark directory with your desired topic in quotes. This will fetch the data from the Twitter API for Rina Sawayama:
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
