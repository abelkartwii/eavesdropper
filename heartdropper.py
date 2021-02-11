from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import json
import sys
from pyspark.sql.types import *

def heart(avg_sentiment):
    try:
        if avg_sentiment < 0:
            return 'Negative ):'
        elif avg_sentiment == 0:
            return 'Meh'
        else:
            return 'Positive :)'
    except TypeError:
        return 'It is a mystery...'

if __name__ == "__main__":
    schema = StructType([
        StructField("text", StringType())
        StructField("sentiment_val", DoubleType())
    ])

    spark = (SparkSession
        .builder
        .appName("Eavesdropper")
        .getOrCreate())

    # read streaming query from kafka, 
    # subscribe to topic "twitter"
    kafka_dframe = (spark
        .readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "twitter")
        .load())

    # turn to string
    kafka_dstring = (kafka_dframe
        .selectExpr("CAST(value AS STRING)"))

    tweets_table = (kafka_dstring
        .select(from_json(col("value"), schema)
        .alias("data")
        .select("data.*"))

    sum_table =  (tweets_table
        .select(avg('senti_val').alias('avg_sentiment')))

    # avg of sentiment value
    avg_df = (sum_table
        .withColumn("status", udf_avg_to_status("avg_sentiment")))

    # write to kafka
    query = (avg_df
        .writeStream
        .outputMode("complete")
        .format("console")
        .start())

    query.awaitTermination()