#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder\
     .master("spark://spark-master:7077")\
     .appName("Step1_2-CSV-Append-Mode-Console")\
     .config("spark.executor.memory", "512mb")\
     .config("spark.executor.cores","1")\
     .config("spark.cores.max", "1")\
     .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")


schema = StructType([StructField("lsoa_code", StringType(), True),\
                     StructField("borough", StringType(), True),\
                     StructField("major_category", StringType(), True),\
                     StructField("minor_category", StringType(), True),\
                     StructField("value", StringType(), True),\
                     StructField("year", StringType(), True),\
                     StructField("month", StringType(), True)])



fileStreamDF = spark.readStream\
               .option("header", "false")\
               .schema(schema)\
               .option("maxFilesPerTrigger", 1)\
               .csv("/opt/spark-data/datasets/droplocation")


# Check whether input data is streaming or not
print(" ")
print("Is the stream ready?")
print(fileStreamDF.isStreaming)

print("Schema of the input stream: ")
fileStreamDF.printSchema()



# Create a trimmed version of the input dataframe with specific columns
# We cannot sort a DataFrame unless aggregate is used, so no sorting here
trimmedDF = fileStreamDF.select(
                                  fileStreamDF.borough,
                                  fileStreamDF.year,
                                  fileStreamDF.month,
                                  fileStreamDF.value
                                  )\
                         .withColumnRenamed(
                                  "value",
                                  "convictions"
                                  )


# In[ ]:


query = trimmedDF.writeStream\
                 .outputMode("append")\
                 .format("console")\
                 .option("truncate", "false")\
                 .option("numRows", 30)\
                 .trigger(processingTime = "5 seconds")\
                 .start()\
                 .awaitTermination()

