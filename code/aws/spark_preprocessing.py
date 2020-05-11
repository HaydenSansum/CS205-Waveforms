from spark_preprocessing_functions import normalize_song, mu_law, song_digitizer, song_downsampler, mp3_to_wavdata 
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import os
import time

# # Old version
conf = SparkConf().setMaster('local[1]').setAppName('song_converter')
sc=SparkContext(conf=conf)

# # New Spark
# spark = SparkSession.builder.master("local").appName("song_converter").getOrCreate()

# Parameters
n_partitions = 32

# File Paths                                                            
input_song_dir = "input_songs/"

# # Which songs to pull in
all_songs=[input_song_dir+song for song in os.listdir(input_song_dir)]
# all_songs = all_songs[0:100]
# all_songs = ['s3://waveform-storage/input_data/song_mp3/Pop/batch01/Song313_A_A_Aalto_-_Zebra.mp3']


start = time.time()
rdd = sc.parallelize(all_songs) \
            .map(mp3_to_wavdata) \
            .map(song_downsampler) \
            .map(song_digitizer) \
            .map(lambda x: x.tolist())

print("MyPartitions", rdd.getNumPartitions())

rdd.saveAsPickleFile('processed_songs')