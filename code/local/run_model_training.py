from modelling_functions import gen_songs_from_pickle
from wavenet import create_wavenet

import numpy as np

data_path = "../../songs/pickle/"

song_train_data_generator = gen_songs_from_pickle(data_path, data_size=1024, n_stride=256, n_channels=256, batch_size=128, genres_to_train=['Jazz'], shuffle=True, seed=205)

wavenet_model = create_wavenet(1024, 256, [32, 32, 64, 128])
  
wavenet_model.compile(optimizer='adam', loss='categorical_crossentropy')

wavenet_model.fit_generator(song_train_data_generator, epochs=1)

print("finished")