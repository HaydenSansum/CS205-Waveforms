from spark_model_building_functions import one_hot_encode_chunk, split_song_to_train
from wavenet import create_wavenet
from elephas.spark_model import SparkModel
from elephas.utils.rdd_utils import to_simple_rdd

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
                .map(lambda x: (x, one_hot_encode_chunk(x))) \
                .map(lambda x: (np.array(x[0]).reshape(4096,1), np.array(x[1])))

X_train = np.random.random((100,200))
Y_train = np.random.random((100,10))

rdd = to_simple_rdd(sc, X_train, Y_train)

for xs in rdd.take(5):
    print(xs[0].shape)
    print(xs[1].shape)

for xs in train_rdd.take(5):
    print(xs[0].shape)
    print(xs[1].shape)

from keras import Model
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers import Conv1D, Input
from keras.optimizers import SGD

model_input = Input(shape=(4096, 1))
layer1 = Conv1D(filters=256, kernel_size=1, padding='same', activation='relu')(model_input)
layer2 = Conv1D(filters=256, kernel_size=1, padding='same', activation='relu')(layer1)
layer3 = Conv1D(filters=256, kernel_size=1, padding='same', activation='softmax')(layer2)
model = Model(model_input, layer3)
model.compile(loss='categorical_crossentropy', optimizer=SGD())

print(model.summary())
wavenet_model = create_wavenet(10, 256, [32, 128, 256, 512], 4)
# # adam_opt = keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False)
# # wavenet_model.compile(optimizer=adam_opt, loss='categorical_crossentropy')
print(model.summary())
print(wavenet_model.summary())

spark_model = SparkModel(wavenet_model, frequency='epoch', mode='asynchronous')
spark_model.fit(train_rdd, epochs=1, batch_size=32, verbose=1, validation_split=0.1)





