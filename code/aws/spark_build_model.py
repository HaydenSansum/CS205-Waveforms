from spark_model_building_functions import one_hot_encode_chunk, split_song_to_train
from wavenet import create_wavenet
from elephas.spark_model import SparkModel
import numpy as np
import keras


# =========== SPARK CONFIG ===========
from pyspark import SparkContext, SparkConf
conf = SparkConf().setMaster('local[4]').setAppName('Test')
sc = SparkContext(conf=conf)

song_directory = "songs_binary/part-00000"
s3_song_directory = "s3://waveform-storage/input_data/song_processed/Pop/part-00000"

train_rdd = sc.pickleFile(song_directory) \
                .flatMap(lambda x: split_song_to_train(x[1])) \
                .map(lambda x: (x,x))
                #.map(lambda x: (x,one_hot_encode_chunk(x)))


wavenet_model = create_wavenet(10, 256, [32, 128, 256, 512], 4)
adam_opt = keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False)
wavenet_model.compile(optimizer=adam_opt, loss='categorical_crossentropy')


# wavenet_model = create_wavenet(10, 256, [32, 128, 256, 512], 4)
# adam_opt = keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False)
# wavenet_model.compile(optimizer=adam_opt, loss='categorical_crossentropy')

spark_model = SparkModel(wavenet_model, frequency='epoch', mode='asynchronous')
spark_model.fit(train_rdd, epochs=20, batch_size=32, verbose=0, validation_split=0.1)





