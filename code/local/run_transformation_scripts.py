from file_transformer import mp3_transformer
from song_transform_functions import song_digitizer

mpt = mp3_transformer('../../songs')
mpt.set_input_path('mp3')
mpt.set_output_path('test2')
mpt.set_overwrite(True)

mpt.transform_song([song_digitizer], mpt._input_folders, 'mp3', 'wav', 44100)
print("Completed transformation of songs to WAV")


