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
    return song,myout.tolist()



rdd = spark.sparkContext.parallelize(all_songs,len(all_songs)).map(process)
rdd.saveAsPickleFile('file:/home/hadoop/nathaniel.pkl')
# rdd.coalesce(1).saveAsTextFile("file:/home/hadoop/nathaniel.txt")