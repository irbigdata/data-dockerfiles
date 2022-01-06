#!/usr/bin/env python
# coding: utf-8

import sys
import time
import datetime


TOPIC_Step2_NAME="Sahamyab-Tweets2"
KAFKA_SERVER="kafka-broker:29092"



import os
# https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html

# setup arguments
os.environ['PYSPARK_SUBMIT_ARGS']='--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 pyspark-shell'

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


spark = SparkSession.builder\
        .master("spark://spark-master:7077")\
        .appName("Step2_7-Memory-Sink-Console")\
        .config("spark.executor.memory", "1024mb")\
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
   .option("kafka.group.id", "step2_7-Memory-Sink-Console")\
   .load()
# In[7]:


tweetsStringDF = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

tweetsDF = tweetsStringDF.select(from_json(col("value"), schema).alias("data")).select("data.*")
tweetsDF = tweetsDF.withColumn("timestamp", unix_timestamp("sendTime", "yyyy-MM-dd'T'HH:mm:ssz").cast('timestamp'))\
             .withColumn("persian_timestamp", from_utc_timestamp("timestamp", "Asia/Tehran").cast('timestamp')) \
             .withColumn("persianYear", tweetsDF['sendTimePersian'].substr(0, 4))\
             .withColumn("persianMonth", tweetsDF['sendTimePersian'].substr(6, 2))\
             .withColumn("persianDay", tweetsDF['sendTimePersian'].substr(9, 2))

user_activity_count = tweetsDF\
    .withWatermark("persian_timestamp", "10 minutes") \
    .groupBy(
        window(col("persian_timestamp"), "1 hours", "1 hours"), # 10 minute window, updating every 10 minutes
        col("senderUsername"))\
    .count()

# Create query stream with memory sink
queryStream = user_activity_count\
 .writeStream\
 .format("memory")\
 .queryName("user_activity")\
 .outputMode("update")\
 .start()

from time import sleep
cnt=1
while True : 
    print("-=-"*20)
    print(f"Round :#{cnt:4}")
    cnt+=1
    top10_last_housr_df = spark.sql(
        """
            select
                window.start
                ,window.end
                ,senderUsername
                ,sum(count) as count
            from
                user_activity
            where
                window.start = (select max(window.start) from user_activity)
            group by
                window.start
                ,window.end
                ,senderUsername
            order by
                4 desc
            limit 10
        """
    )
    top10_last_housr_df.show()
    sleep(20)
