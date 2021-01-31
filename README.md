## Overview
This project uses Python, PySpark, and Kafka to analyze the sentiments of a Twitter topic. Input the topic that you want to know the reception of, and receive the sentiment status of it!

## Configuration
Required modules: `pykafka`, `tweepy`, `afinn`.

To run, first create a Twitter API account [here](https://developer.twitter.com/en/apply-for-access), obtain the necessary keys, and place them in `config.cfg` as below.

```
consumer_key = <insert your consumer key here>
consumer_secret = <insert your consumer secret here>
access_token = <insert your access token here>
access_secret = <insert your access secret here>
```

You will need to start an Apache Kafka server. Download the latest version [here](https://kafka.apache.org/downloads). On the command line, run the following to start the server:
```
/bin/kafka-server-start.sh /config/server.properties
```

Then, run `eavesdropper.py` in your Spark directory with your desired topic in quotes. This will fetch the data from the Twitter API:
```
python bin/spark-submit eavesdropper.py "Rina Sawayama"
```

And finally, run `heartdropper.py`.

```
python heartdropper.py
```

## To-do
* add an option to view sentiments per country/location