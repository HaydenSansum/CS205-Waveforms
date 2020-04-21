import os
import re
from pydub import AudioSegment

# =========== PARAMETERS ============
# Bit rate (aka number of samples)
bit_rate= "1411k" # 1411 appears to be standard for wav 
overwrite_songs = True

# ========== Folder and File Setups =========
# File Paths                                                            
input_song_dir = "songs/mp3/"
output_song_dir = "songs/wav/"

all_folders = os.listdir(input_song_dir)
song_folders = []

# Drop folders starting with dot (hidden folders such as .DS_Store)
for folder in all_folders:
    if not re.match(r'^[.].*', folder):
        song_folders.append(folder)

        # Make new folder directories in the wav folder
        if not os.path.exists(f'{output_song_dir}{folder}'):
            os.mkdir(f'{output_song_dir}{folder}')


# ========== Song Conversion Step =========
# Run through and convert all songs
for folder in song_folders:
    all_songs = os.listdir(f'{input_song_dir}{folder}')

    for song in all_songs:
        # Ignore hidden files
        if not re.match(r'^[.].*', song):
            
            # Create output song naming
            song_base_name = song[:-4]
            song_out_name = song_base_name + '.wav'

            if overwrite_songs == False:
                # Check if song exists in output
                if not os.path.exists(f'{output_song_dir}{folder}/{song_out_name}'):
                    # Convert song
                    wav_song = AudioSegment.from_mp3(f'{input_song_dir}{folder}/{song}')
                    wav_song.export(f'{output_song_dir}{folder}/{song_out_name}', bitrate=bit_rate, format="wav")
            
            else:
                # Convert song
                wav_song = AudioSegment.from_mp3(f'{input_song_dir}{folder}/{song}')
                wav_song.export(f'{output_song_dir}{folder}/{song_out_name}', bitrate=bit_rate, format="wav")

