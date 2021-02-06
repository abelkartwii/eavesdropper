from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import json
import sys
from pyspark.sql.types import *

def heart(avg_senti_val):
    try:
        if avg_senti_val < 0:
            return 'Negative ):'
        elif avg_senti_val == 0:
            return 'Meh'
        else:
            return 'Positive :)'
    except TypeError:
        return 'Meh'

if __name__ == "__main__":
    schema = StructType([
        StructField("text", StringType(), True)
        StructField("sentiment_val", DoubleType(), True)
    ])

    spark = SparkSession.builder.appName("Eavesdropper").getOrCreate()
    kafka_df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("subscribe", "twitter").load()