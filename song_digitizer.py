import os
import re
import numpy as np
from scipy.io import wavfile

# ======= Parameters =======
n_output_channels = 256
overwrite_songs = True

# File Paths                                                            
input_song_dir = "songs/wav/"
output_song_dir = "songs/wav_digitized/"

# ======= Functions =======

def digitize_wav_song(song, n_out_channels = n_output_channels):

    new_data = data.copy()

    min_val = np.min(new_data[:,0])
    max_val = np.max(new_data[:,1])

    bin_cutoffs = np.linspace(min_val, max_val, 256)
    new_data[:,0] = np.digitize(new_data[:,0], bin_cutoffs)
    new_data[:,1] = np.digitize(new_data[:,1], bin_cutoffs)

    return(new_data)


# ======= Binning Code =======

all_folders = os.listdir(input_song_dir)
song_folders = []

# Drop folders starting with dot (hidden folders such as .DS_Store)
for folder in all_folders:
    if not re.match(r'^[.].*', folder):
        song_folders.append(folder)

        # Make new folder directories in the output folder
        if not os.path.exists(f'{output_song_dir}{folder}'):
            os.mkdir(f'{output_song_dir}{folder}')


# Run through and convert all songs
for folder in song_folders:
    all_songs = os.listdir(f'{input_song_dir}{folder}')

    for song in all_songs:
        # Ignore hidden files
        if not re.match(r'^[.].*', song):
            
            if overwrite_songs == False:
                # Check if song exists in output
                if not os.path.exists(f'{output_song_dir}{folder}/{song}'):
                    # Digitize
                    fs, data = wavfile.read(f'{input_song_dir}{folder}/{song}')
                    digit_data = digitize_wav_song(data)
                    wavfile.write(f'{output_song_dir}{folder}/{song}', 44100, digit_data)

            else:
                # Digitize
                fs, data = wavfile.read(f'{input_song_dir}{folder}/{song}')
                digit_data = digitize_wav_song(data)
                wavfile.write(f'{output_song_dir}{folder}/{song}', 44100, digit_data)




