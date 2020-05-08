from spark_preprocessing_functions import normalize_song, mu_law, song_digitizer, song_downsampler, mp3_to_wavdata 
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import os

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
            .map(song_downsampler) \
            .map(song_digitizer) \
            .map(x.tolist())

rdd.coalesce(1).saveAsPickleFile('file:/home/hadoop/testpickle')