from modelling_functions import gen_songs_from_pickle
from wavenet import create_wavenet

import numpy as np

data_path = "../../songs/pickle/"

song_train_data_generator = gen_songs_from_pickle(data_path, data_size=1024, n_stride=256, n_channels=256, batch_size=128, genres_to_train=['Jazz'], shuffle=True, seed=205)

x, y = song_train_data_generator.__next__()
# x2, y2 = song_train_data_generator.__next__()
# x3, y3 = song_train_data_generator.__next__()

# x5 = x.reshape(-1, x.shape[0], x.shape[1])


# # # Bug fixing
# print(x.shape)
# print(y.shape)

# x_train = np.dstack([x,x2,x3])
# y_train = np.dstack([y,y2,y3])

# x_train = np.swapaxes(x_train, 0, 2)
# x_train = np.swapaxes(x_train, 1, 2)
# y_train = np.swapaxes(y_train, 0, 2)
# y_train = np.swapaxes(y_train, 1, 2)

# print(x_train.shape)
# print(y_train.shape)





# # Test code for demoing the generator
# i = 0
# for song_chunk in song_train_data_generator:
#     final_chunk = song_chunk
#     i += 1

# print(i)
# print(final_chunk[0,:])
# print(len(final_chunk[0,:]))
# print(np.argmax(final_chunk[0,:]))


wavenet_model = create_wavenet(1024, 256, [32, 32, 64, 128])
  
wavenet_model.compile(optimizer='adam', loss='categorical_crossentropy')

wavenet_model.fit_generator(song_train_data_generator, epochs=1)

print("finished")