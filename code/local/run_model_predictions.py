from song_transform_functions import inverse_mu_law, inverse_normalize_song, decode_onehot_random_note

from tensorflow.keras.models import model_from_json
from scipy.io import wavfile

import numpy as np
import pickle

version = "v5" 

output_data_path = "../../songs/generated/"
output_song_name = f"first_ever_song_{version}.wav"

model_path = "../../models/"
model_name = "basic_model_nf16_ns64"

song_length = 10 # Song length in seconds to predict for (WARNING 10s = approx 40mins)

# Seed sequence:
with open("../../songs/pickle/Dance/Song0_Nathaniel_Wyvern_-_01_-_Total_Eclipse.pkl", 'rb') as infile:
    seed_song_data = pickle.load(infile)

# Take a chunk of song starting from start
s_start = 300000
seed_song_data = seed_song_data[:,0]
seed_song_data = seed_song_data[s_start:s_start+1024]

# Load model
with open(f"{model_path}{model_name}.json", "r") as wavenet_file:
    wave_net_json = wavenet_file.read()

wavenet_model = model_from_json(wave_net_json)
wavenet_model.load_weights(f"{model_path}{model_name}.h5")
print("Model loading Complete")

# Make predictions
seed_vector = seed_song_data
#seed_vector = np.random.randint(0, 50, 1024) # Seed with random narrow band of notes
#seed_vector = np.full(1024, 250)

predicted_song = seed_vector

counter = 0 # To tell the song when to stop
while True:
    new_data = wavenet_model.predict(predicted_song[-1024:].reshape(1, 1024, 1))

    new_note = decode_onehot_random_note(new_data[0,:,:])
    # new_note = new_song_data[-1]
    predicted_song = np.append(predicted_song, new_note)

    counter += 1
    if counter % 2000 == 0:
        print(f"Finished {counter} samples")
        print(f"Most recent 20 samples: {predicted_song[-20:]}")
    if counter == (song_length * 8000):
        break

# Save raw output to check functions later
with open(f"{output_data_path}raw_song_{version}.pkl", 'wb') as outfile:
    pickle.dump(predicted_song, outfile)

# Convert back to sound
inv_mu_song = inverse_mu_law(predicted_song)
final_song = inverse_normalize_song(inv_mu_song)

final_song_stereo = np.stack([final_song, final_song], axis=1)

wavfile.write(f"{output_data_path}{output_song_name}", 8000, final_song_stereo)


