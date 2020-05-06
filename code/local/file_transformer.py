import os
import re
import tempfile
from scipy.io import wavfile
from pydub import AudioSegment

class mp3_transformer:
    '''
    mp3 transformer object which applies a specified transformation to 
    a specific folder of mp3 files and writes out either wav file or csv data

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
        self._song_object = None

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

    def _read_mp3(self, input_file, bit_rate="1411k"):
        '''
        Convert input MP3 file into output WAV file and then read back into numpy array
        '''
        wav_song = AudioSegment.from_mp3(input_file)
        _, tmp_file = tempfile.mkstemp()
        wav_song.export(tmp_file, bitrate=bit_rate, format="wav")
        fs, wav_data = wavfile.read(tmp_file)
        return wav_data

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

    def transform_song(self, transformations, list_of_input_folders, filetype_in, filetype_out, out_freq = None):
        '''
        Apply the specified function to a list of input folders

        Must specify a specific file type to apply to (only one allowed)

        Output filetype should match the operation being applied

        Functions should perform operations in place on the input file - aka they should perform the saving
        to output path - MUST have two inputs - input file and output path
        '''
        assert filetype_out == 'csv' or filetype_out == 'wav', "ERROR: File out must be wav or csv"
        if filetype_out == 'wav':
            assert out_freq != None, "Error, for wav output type must specify an out_freq"

        for data_in_folder in self._input_folders:

            # Only apply if in the designated list
            if data_in_folder in list_of_input_folders:

                # Make output folder if required
                if not os.path.exists(self._output_path + data_in_folder):
                    os.mkdir(self._output_path + data_in_folder)

                # Get all songs
                all_songs = self._get_all_songs(self._input_path + data_in_folder, filetype_in)

                # For each song
                for cur_song in all_songs:

                    output_name = cur_song.replace(filetype_in, filetype_out)

                    if self._overwrite == False:
                         if not os.path.exists(self._output_path + data_in_folder + '/' + output_name):
                                                   
                            # Apply the functions to the file
                            input_file = self._input_path + data_in_folder + '/' + cur_song
                            output_path = self._output_path + data_in_folder + '/' + output_name

                            # Read in
                            self._song_object = self._read_mp3(input_file)

                            for sub_function in transformations:
                                self._song_object = sub_function(self._song_object)

                            if filetype_out == 'wav':
                                wavfile.write(output_path, out_freq, self._song_object)

                            if filetype_out == 'csv':
                                self._song_object.to_csv(output_path)

                    else:
                        # Apply the functions to the file
                        input_file = self._input_path + data_in_folder + '/' + cur_song
                        output_path = self._output_path + data_in_folder + '/' + output_name

                        # Read in
                        self._song_object = self._read_mp3(input_file)

                        for sub_function in transformations:
                            self._song_object = sub_function(self._song_object)

                        if filetype_out == 'wav':
                            wavfile.write(output_path, out_freq, self._song_object)

                        if filetype_out == 'csv':
                            self._song_object.to_csv(output_path)

