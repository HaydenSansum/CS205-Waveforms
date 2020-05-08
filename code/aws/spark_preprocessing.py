from spark_song_transform_functions import normalize_song, mu_law, song_digitizer, song_downsampler, mp3_to_wavdata 
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql.types import *
import string
import sys
import re
import os
from pydub import AudioSegment
from scipy.io import wavfile
from pydub import AudioSegment
import tempfile
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
import resampy


# # Old version
# conf = SparkConf().setMaster('local').setAppName('song_converter')
# sc=SparkContext(conf=conf)

# Parameters
n_partitions = 32

# File Paths                                                            
input_song_dir = "batch1spark/"

# # Which songs to pull in
# all_songs=[input_song_dir+song for song in os.listdir(input_song_dir)]
# all_songs = all_songs[0:224]
all_songs = ['Song324_opo_-_37_-_Triste_Triste_XXVII.mp3']

# Spark
spark = SparkSession.builder.master("local").appName("song_converter").getOrCreate()
rdd = spark.sparkContext.parallelize(all_songs,n_partitions) \
            .map(mp3_to_wavdata) \
            .map(lambda x: (x[0],song_downsampler(x[1]))) \
            .map(lambda x: (x[0],song_digitizer(x[1]))) \
            .map(lambda x: (x[0],x[1].tolist()) )
rdd.coalesce(1).saveAsPickleFile('file:/home/hadoop/testpickle')
# rdd.coalesce(1).saveAsTextFile("file:/home/hadoop/testtxt")