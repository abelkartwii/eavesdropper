from kafka import KafkaProducer
from configparser import ConfigParser
from pathlib import Path
from json import dumps

config = ConfigParser()
config.read_file(open(f"{Path(__file__).parents[0]}/config.cfg"))

kafka_config = config["kafka"]
kafka_topic = config["kafka"]["topic"]
# kafka-python installed is 2.0.2, so pass that to api_version

producer = KafkaProducer(bootstrap_servers = kafka_config["bootstrap_servers"],
                         value_serializer = lambda x: dumps(x).encode('utf-8'),
                         api_version = (2,0,2))