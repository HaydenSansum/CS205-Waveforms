from spark_model_building_functions import one_hot_encode_chunk, split_song_to_train
from wavenet import create_wavenet
from elephas.spark_model import SparkModel
from elephas.utils.rdd_utils import to_simple_rdd

import numpy as np
import keras

# =========== Parameters to Set ===========
song_directory = "part-00001"
model_save_out = "wavenet_big_t1"

num_nodes = 32
#n_data_partitions = 128
num_worker = 128
data_size = 4096
data_collect_stride = 16368

stack_layers = 10
num_stacks = 4

n_filter_list = [32, 128, 256, 512]
n_output_channels = 256

# Check data sizes and shapes match
assert (2**stack_layers)*num_stacks == data_size, "ERROR: Data size must match network size - (2^stack_layers) * num_stacks"  

# =========== SPARK CONFIG ===========
set_master_val = "local[" + str(num_nodes) + "]"

from pyspark import SparkContext, SparkConf
#conf = SparkConf().setAppName('TrainWavenet').set("spark.driver.maxResultSize", "2G")
conf = SparkConf().setMaster(set_master_val).setAppName('TrainWavenet').set("spark.driver.maxResultSize", "2G")
sc = SparkContext(conf=conf)


# ============ DATA SETUP ===========
# s3_song_directory = "s3://waveform-storage/input_data/song_processed/Pop/part-00000"

#, minPartitions=n_data_partitions) 
train_rdd = sc.pickleFile(song_directory) \
                .flatMap(lambda x: split_song_to_train(x, data_size, data_collect_stride)) \
                .map(lambda x: (x, one_hot_encode_chunk(x))) \
                .map(lambda x: (np.array(x[0]).reshape(data_size,1), np.array(x[1])))

print("Num Partitions: ", train_rdd.getNumPartitions())

# x_stack = []
# y_stack = []
# for _ in range(20):
#     x_stack.append(np.random.randint(0, 256, 8192))
#     y_stack.append(np.random.randint(0, 256, (8192, 256)))
    
# x_train = np.dstack(x_stack)
# y_train = np.dstack(y_stack)

# x_train = np.swapaxes(x_train, 0,2)
# y_train = np.swapaxes(y_train, 0,2)
# y_train = np.swapaxes(y_train, 1,2)


# print(x_train.shape)
# print(y_train.shape)

# train_rdd = to_simple_rdd(sc, x_train, y_train)
# print("Num Partitions: ", train_rdd.getNumPartitions())

# ============ MODEL SETUP ===========
from keras.optimizers import SGD

wavenet_model = create_wavenet(stack_layers, n_output_channels, n_filter_list, num_stacks, skip=False)
adam_opt = keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False)
wavenet_model.compile(optimizer=SGD(), loss='categorical_crossentropy')
print(wavenet_model.summary())


# ============ ELEPHAS TRAIN ===========
spark_model = SparkModel(wavenet_model, mode='hogwild', num_workers=128)
spark_model.fit(train_rdd, epochs=64, batch_size=64, verbose=1, validation_split=0.1)

print("Finished Training :)")

# =========== SAVE FITTED MDOEL ===========
# Save model and weights out to local
filename_out = model_save_out + "_weights.h5"
spark_model.save(filename_out)

wavenet_json = wavenet_model.to_json()
with open(model_save_out + ".json", "w") as save_model:
    save_model.write(wavenet_json)


x_test = np.array(train_rdd.map(lambda x: x[0]).take(1))
y_test = np.array(train_rdd.map(lambda x: x[1]).take(1))

print("Final Loss = ", spark_model.master_network.evaluate(x_test, y_test, verbose=2))

