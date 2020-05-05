import os
import re

class file_transformer:
    '''
    File transformer object which applies a specified transformation to 
    a specific folder of files

    inputs:
        root_filepath - string
        The filepath value (relative or absolute) to the base of the waveform repository, within this folder
        should be all the code and various data folders
 
    '''
    def __init__(self, root_filepath, overwrite = False):

        self._root_path = root_filepath
        self._input_path = None
        self._output_path = None
        self._input_folders = None
        self._output_folders = None
        self._overwrite = overwrite
        self._function_to_apply = None

    def _get_all_songs(self, path, filetype):
        all_files = os.listdir(path)

        # Test for filetype:
        expr = f".*\.{filetype}"
        specific_files = [re.match(expr, cur_file) for cur_file in all_files]

        clean_files = []
        for cur_file in specific_files:
            if cur_file:
                clean_files.append(cur_file.string)

        return(clean_files)

    def set_input_path(self, path):
        self._input_path = self._root_path + '/' + path + '/'

        # Get all input folders
        all_files = os.listdir(self._input_path)
        all_folders = [folder for folder in all_files if os.path.isdir(self._input_path + folder)]
        self._input_folders = all_folders

    def set_output_path(self, path):
        self._output_path = self._root_path + '/' + path + '/'

        # Create output path if it doesn't exist
        if not os.path.exists(self._output_path):
            os.mkdir(self._output_path)

        # Get all existing output folders
        all_files = os.listdir(self._output_path)
        all_folders = [folder for folder in all_files if os.path.isdir(self._output_path + folder)]
        self._output_folders = all_folders

    def set_overwrite(self, value):
        assert value == True or value == False, "Overwrite must be either True or False"
        self._overwrite = value

    def set_operation(self, input_function):
        self._function_to_apply = input_function

    def apply_operation(self, list_of_input_folders):
        assert self._function_to_apply != None, "Error: must set_operation before applying"

        for data_in_folder in self._input_folders:

            # Only apply if in the designated list
            if data_in_folder in list_of_input_folders:

                # Make output folder if required
                if not os.path.exists(self._output_path + data_in_folder):
                    os.mkdir(self._output_path + data_in_folder)



    







# # File Paths                                                            
# input_song_dir = "songs/mp3/"
# output_song_dir = "songs/wav/"

# all_folders = os.listdir(input_song_dir)
# song_folders = []

# # Drop folders starting with dot (hidden folders such as .DS_Store)
# for folder in all_folders:
#     if not re.match(r'^[.].*', folder):
#         song_folders.append(folder)

#         # Make new folder directories in the wav folder
#         if not os.path.exists(f'{output_song_dir}{folder}'):
#             os.mkdir(f'{output_song_dir}{folder}')


# # ========== Song Conversion Step =========
# # Run through and convert all songs
# for folder in song_folders:
#     all_songs = os.listdir(f'{input_song_dir}{folder}')

#     for song in all_songs:
#         # Ignore hidden files
#         if not re.match(r'^[.].*', song):
            
#             # Create output song naming
#             song_base_name = song[:-4]
#             song_out_name = song_base_name + '.wav'

#             if overwrite_songs == False:
#                 # Check if song exists in output
#                 if not os.path.exists(f'{output_song_dir}{folder}/{song_out_name}'):
#                     # Convert song
#                     wav_song = AudioSegment.from_mp3(f'{input_song_dir}{folder}/{song}')
#                     wav_song.export(f'{output_song_dir}{folder}/{song_out_name}', bitrate=bit_rate, format="wav")
            
#             else:
#                 # Convert song
#                 wav_song = AudioSegment.from_mp3(f'{input_song_dir}{folder}/{song}')
#                 wav_song.export(f'{output_song_dir}{folder}/{song_out_name}', bitrate=bit_rate, format="wav")


