# Make a new folder and get a sample of raw songs from S3
mkdir input_songs

# Grab songs
aws s3 sync s3://waveform-storage/input_data/song_mp3/Pop/sample_100 input_songs

# Put into HDFS for processing
hadoop fs -put input_songs

# Run the processing code
spark-submit spark_preprocessing.py

# Read back from HDFS
hadoop fs -get processed_songs
