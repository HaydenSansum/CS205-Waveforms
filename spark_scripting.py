from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql.types import *
import string
import sys
import re
import os
import re
from pydub import AudioSegment
from scipy.io import wavfile
from pydub import AudioSegment
import tempfile
import numpy as np
import pandas as pd

# conf = SparkConf().setMaster('local').setAppName('song_converter')
# sc = SparkContext(conf = conf)

from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local").appName("song_converter").getOrCreate()



# =========== PARAMETERS ============
# Bit rate (aka number of samples)
bit_rate= "1411k" # 1411 appears to be standard for wav 

# File Paths                                                            
input_song_dir = "songs/mp3/"
output_song_dir = "songs/wav/"


all_songs=[input_song_dir+song for song in os.listdir(input_song_dir)]

def process(song):
    # Ignore hidden files
    if not re.match(r'^[.].*', song):
        a_segment = AudioSegment.from_mp3(song)
        _, temp_path = tempfile.mkstemp()
        a_segment.export(temp_path, format="wav")
        rate, songdata = wavfile.read(temp_path)
        myout = songdata[:,0]
    return song,myout



rdd = spark.sparkContext.parallelize(all_songs,len(all_songs)).map(process)
# df.toPandas().to_csv('mycsv.csv')
# ee = rdd.toDF()
# ee.write.parquet("testerHEY.parquet")
# rdd = spark.sparkContext.parallelize(all_songs,len(all_songs)).map(lambda song:str(song)+", "+[str(a)+',' for a in process(song)])

rdd.coalesce(1).saveAsTextFile('newflatu.txt')





# schema = StructType([
#     StructField('Song', StringType(), True),
#     StructField('Data', ArrayType(IntegerType(),True),True)
# ])

# df = spark.createDataFrame(rdd,schema)
# df.write.parquet("tester.parquet")



# schemaString = "song data"
# fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
# schema = StructType(fields)

# sqlContext = SQLContext(sc)
# df = sqlContext.createDataFrame(rdd,schema)

# # spark = SparkSession(sc)
# # df = spark.createDataframe(rdd)
# # df.write.csv("/path/to/file.csv", sep=',', header=True)

# # Write CSV (I have HDFS storage)
# df.coalesce(1).write.format('com.databricks.spark.csv').options(header='true').save('mycsv')


# def toCSVLine(data):
#   return ','.join(str(d) for d in data)

# lines = df.map(toCSVLine)
# lines.saveAsTextFile('testout.csv')