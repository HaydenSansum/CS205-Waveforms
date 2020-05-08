from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql import SparkSession
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
import resampy


def normalize_song(song):
    '''
    Given a song with arbitary continous values, rescale to be between -1 and 1
    '''
    new_song = song
    
    max_ch = np.max(abs(new_song))
    
    overall_max = np.max(max_ch)
    
    # Convert to float
    normalized_song = new_song / overall_max

    normalized_song = normalized_song.transpose()
    
    return normalized_song


def mu_law(song, mu=255):
    '''
    Apply the mu law as described in Wavenet paper
    This is a more realistic compression of audio space than simple linear interpretation
    '''
    new_song = song
    scaled_song = np.sign(new_song) * (np.log(1 + mu * abs(new_song)) / np.log(1 + mu))
    
    return scaled_song


def song_digitizer(input_song, n_out_channels = 256):
    '''
    Convert continuous values to bins with n_channels (generally used on data normalized)
    between -1 and 1
    '''
    song_data = input_song

    song_data = normalize_song(song_data)
    song_data = mu_law(song_data)

    min_val = np.min(song_data)
    max_val = np.max(song_data)

    bin_cutoffs = np.linspace(min_val, max_val, n_out_channels)
    new_ch = np.digitize(song_data, bin_cutoffs)

    # Change back to int
    final_song = new_ch.astype('int16')

    final_song = final_song.transpose()

    return final_song


def song_downsampler(input_song, n_out_channels = 256, input_freq = 44100, output_freq=8000):
    '''
    Uses resampys downsampler to convert to lower number of data points without ruining the
    audio file
    '''

    ds_ch = resampy.resample(input_song.astype(np.float), input_freq, output_freq)

    ds_song = ds_ch.transpose()

    return ds_song

def mp3_to_wavdata(song_file):
    '''
    reads in mp3 files, uses pydub,ffmpeg to convert them into wav
    wav file is exported to a temp path, and read back into data with scipy wavfile
    '''
    #Ignore hidden files
    if not re.match(r'^[.].*', song_file):
        # Read from mp3 and save to tempfile as wav
        a_segment = AudioSegment.from_mp3(song_file)
        _, temp_path = tempfile.mkstemp()
        a_segment.export(temp_path, format="wav")

        # read in wav tempfile and extract data
        rate, songdata = wavfile.read(temp_path)
        myout = songdata[:,0]
    return song_file, myout

    # if not re.match(r'^[.].*', song_file):
    #     # Read from mp3 and save to tempfile as wav
    #     a_segment = AudioSegment.from_mp3(song_file)
    #     songdata = np.array(a_segment.get_array_of_samples()).reshape((-1, 2))[:,0]
    # return song_file,songdata.tolist()



# spark = SparkSession.builder.master("local").appName("song_converter").getOrCreate()



# =========== PARAMETERS ============
# Bit rate (aka number of samples)
bit_rate= "1411k" # 1411 appears to be standard for wav 

# File Paths                                                            
# input_song_dir = "s3://waveform-storage/input_data/song_mp3/Jazz/"

os.environ['PYSPARK_SUBMIT_ARGS'] = 'pyspark --packages=com.amazonaws:aws-java-sdk:1.11.7755,org.apache.hadoop:hadoop-aws:3.2.1'

accesskey = "AKIA6FQHF5S6KQDWI5NT"
secretkey = "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"

conf = SparkConf().set("spark.executor.extraJavaOptions","-Dcom.amazonaws.services.s3a.enableV4=true") \
                    .set("spark.driver.extraJavaOptions","-Dcom.amazonaws.services.s3a.enableV4=true") \
                    .set('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:2.7.2') \
                    .setMaster('local').setAppName('song_converter')

sc=SparkContext(conf=conf)
sc.setSystemProperty("com.amazonaws.services.s3.enableV4", "true")
hadoopConf = sc._jsc.hadoopConfiguration()
hadoopConf.set("fs.s3a.awsAccessKeyId", accesskey)
hadoopConf.set("fs.s3a.awsSecretAccessKey", secretkey)
hadoopConf.set('fs.s3a.endpoint', 's3-us-east-2.amazonaws.com')
hadoopConf.set("com.amazonaws.services.s3a.enableV4", "true")
hadoopConf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")


input_song_dir = "s3a://waveform-storage/input_data/song_mp3/Jazz/"

# all_songs=[input_song_dir+song for song in os.listdir(input_song_dir)]

# all_songs= ["s3a://waveform-storage/input_data/song_mp3/Jazz/Song0_KieLoKaz_-_02_-_Trip_to_Ganymed_Kielokaz_ID_363.mp3"]
all_songs = ["s3a://emr-example-python-nv/Dance/Song19_Loyalty_Freak_Music_-_01_-_Roller_Fever.mp3"]

text = sc.textFile('s3a://emr-example-python-nv/input.txt')
text.take(2).foreach(println)

# rdd = sc.parallelize(all_songs,len(all_songs)) \
#             .map(mp3_to_wavdata) \
#             .map(lambda x: (x[0],song_downsampler(x[1]))) \
#             .map(lambda x: (x[0],song_digitizer(x[1]))) \
#             .map(lambda x: (x[0],x[1].tolist()) )
# rdd.saveAsPickleFile('file:/home/hadoop/nathanielFUNC4.pkl')
# rdd.coalesce(1).saveAsTextFile("file:/home/hadoop/nathanielFunc3.txt")