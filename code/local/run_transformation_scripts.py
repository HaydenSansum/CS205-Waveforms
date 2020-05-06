from file_transformer import mp3_transformer
from song_transform_functions import song_digitizer, song_downsampler

# SAVE TO WAV
mpt = mp3_transformer('../../songs')
mpt.set_input_path('mp3')
mpt.set_output_path('wav')
mpt.set_overwrite(True)

mpt.transform_song([song_downsampler, song_digitizer], mpt._input_folders, 'wav', 8000)
print("Completed transformation of songs to WAV")


# SAVE TO PICKLE
mpt = mp3_transformer('../../songs')
mpt.set_input_path('mp3')
mpt.set_output_path('pickle')
mpt.set_overwrite(True)

mpt.transform_song([song_downsampler, song_digitizer], mpt._input_folders, 'pkl')
print("Completed transformation of songs to PICKLE")


