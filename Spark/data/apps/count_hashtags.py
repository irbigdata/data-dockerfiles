#!/usr/bin/env python
# coding: utf-8

import sys
import time
import datetime

TOPIC_Step2_NAME="Sahamyab-Tweets2"
KAFKA_SERVER="kafka-broker:29092"


import os
# https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html
# https://mvnrepository.com/artifact/org.apache.spark/spark-sql-kafka-0-10_2.12
# setup arguments
os.environ['PYSPARK_SUBMIT_ARGS']='--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 pyspark-shell'

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


spark = SparkSession.builder\
         .master("spark://spark-master:7077")\
         .appName("Step2_04-Hashtag-Count-Console")\
         .config("spark.executor.memory", "500mb")\
         .config("spark.executor.cores","1")\
         .config("spark.cores.max", "1")\
         .config("spark.sql.session.timeZone", "Asia/Tehran")\
         .getOrCreate()    
    

spark.sparkContext.setLogLevel("ERROR")
schema = StructType([StructField("id", StringType(), True),\
                     StructField("content", StringType(), True),\
                     StructField("sendTime", StringType(), True), \
                     StructField("sendTimePersian", StringType(), True),\
                     StructField("senderName", StringType(), True),\
                     StructField("senderUsername", StringType(), True),\
                     StructField("type", StringType(), True),\
                     StructField("hashtags", ArrayType(StringType()), True)
                    ])

df = spark\
   .readStream\
   .format("kafka")\
   .option("kafka.bootstrap.servers", KAFKA_SERVER)\
   .option("subscribe", TOPIC_Step2_NAME)\
   .option("startingOffsets", "earliest")\
   .option("kafka.group.id", "step2_4-count-hashtags-console")\
   .load()


df.printSchema()


tweetsStringDF = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

tweetsDF = tweetsStringDF.select(from_json(col("value"), schema).alias("data")).select("data.*")
tweetsDF = tweetsDF.withColumn("timestamp", unix_timestamp("sendTime", "yyyy-MM-dd'T'HH:mm:ssz").cast('timestamp'))\
             .withColumn("persianYear", tweetsDF['sendTimePersian'].substr(0, 4))\
             .withColumn("persianMonth", tweetsDF['sendTimePersian'].substr(6, 2))\
             .withColumn("persianDay", tweetsDF['sendTimePersian'].substr(9, 2))

hashtagCounts = tweetsDF.select(explode("hashtags").alias("hashtag")) \
                      .groupBy("hashtag")\
                      .count()\
                      .orderBy("count", ascending=False)

query = hashtagCounts.writeStream\
                  .outputMode("complete")\
                  .format("console")\
                  .option("truncate", "false")\
                  .option("numRows","10")\
                  .start()\
                  .awaitTermination()
