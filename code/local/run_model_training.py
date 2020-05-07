from modelling_functions import gen_songs_from_pickle
from wavenet import create_wavenet

import numpy as np

data_path = "../../songs/pickle/"

song_train_data_generator = gen_songs_from_pickle(data_path, data_size=1024, n_stride=256, n_channels=256, onehot=True, genres_to_train=['Jazz'], shuffle=True, seed=205)

i = 0
for song_chunk in song_train_data_generator:
    final_chunk = song_chunk
    i += 1

print(i)
print(final_chunk[0,:])
print(len(final_chunk[0,:]))
print(np.argmax(final_chunk[0,:]))



# wavenet_model = create_wavenet(1024, 256, [32, 32, 64, 128])
  
# print(wavenet_model.summary())