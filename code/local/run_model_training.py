from modelling_functions import gen_songs_from_pickle
from wavenet import create_wavenet


data_path = "../../songs/pickle/"

song_train_data_generator = gen_songs_from_pickle(data_path, genres_to_train=None, shuffle=True, seed=205)

# for song in song_train_data_generator:
#     print(song)

wavenet_model = create_wavenet(1024, 256, [32, 32, 64, 128])
  
print(wavenet_model.summary())