#!/usr/bin/env python
# coding: utf-8

import sys
import time
import datetime


TOPIC_Step3_NAME="User-Raw-Data"
KAFKA_SERVER="kafka-broker:29092"


# In[3]:


import os
# https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html

# setup arguments
os.environ['PYSPARK_SUBMIT_ARGS']='--packages  org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 pyspark-shell'
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder\
     .master("spark://spark-master:7077")\
     .appName("Step2_03-Count-Provinces-Console")\
     .config("spark.executor.memory", "500mb")\
     .config("spark.executor.cores","1")\
     .config("spark.cores.max", "1")\
     .config("spark.sql.session.timeZone", "Asia/Tehran")\
     .getOrCreate()    
    

spark.sparkContext.setLogLevel("ERROR")

df = spark\
   .readStream\
   .format("kafka")\
   .option("kafka.bootstrap.servers", KAFKA_SERVER)\
   .option("subscribe", TOPIC_Step3_NAME)\
   .option("startingOffsets", "earliest")\
   .load()


# sample json must be in jsonl format
# cat user.json | jq -c
df2 = spark.read.json("/opt/spark-data/user.json")
user_schema = df2.schema

userStringDF = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

userDF = userStringDF.select(from_json(col("value"), user_schema).alias("data")).select("data.*")

# The User Defined Function (UDF)
# Create a timestamp from the current time and return it
import jdatetime
def add_timestamp():
         ts = time.time()
         timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
         return timestamp
def add_persian_timestamp():
         persian_timestamp = jdatetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
         return persian_timestamp

# Register the UDF
# Set the return type to be a String
# A name is assigned to the registered function 
add_timestamp_udf = udf(add_timestamp, StringType())
add_persian_timestamp_udf = udf(add_persian_timestamp, StringType())


userDF = userDF.withColumn("timestamp", add_timestamp_udf())
userDF = userDF.withColumn("persian_timestamp", add_persian_timestamp_udf())

windowedStateCounts = userDF.select("persian_timestamp","location.state")\
                                     .groupBy(\
                                            window(userDF.persian_timestamp, \
                                                    "1 hours", \
                                                    "30 minutes"),\
                                            "state")\
                                     .count()\
                                     .orderBy([col("window").desc(),col("count").desc() ])
                                     # .orderBy(col("count").desc())

#                                      .filter(col('count')>2) \
#                                      
                                     

query = windowedStateCounts\
        .writeStream\
        .outputMode("complete")\
        .format("console")\
        .option("truncate", "false")\
        .option("checkpointLocation", "/opt/spark/spark-apps/")\
        .option("numRows", 30)\
        .start()\
        .awaitTermination()
