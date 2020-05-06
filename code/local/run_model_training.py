from modelling_functions import gen_songs_from_pickle

data_path = "../../songs/pickle/"

song_train_data_generator = gen_songs_from_pickle(data_path, genres_to_train=None, shuffle=True, seed=205)

for song in song_train_data_generator:
    print(song)
  