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

    def apply_operation(self, selected_function, list_of_input_folders, filetype_in, filetype_out):
        '''
        Apply the specified function to a list of input folders

        Must specify a specific file type to apply to (only one allowed)

        Output filetype should match the operation being applied

        Functions should perform operations in place on the input file - aka they should perform the saving
        to output path - MUST have two inputs - input file and output path
        '''
        
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
                             print('got in here')

                             # Apply the function to the file
                             input_file = self._input_path + data_in_folder + '/' + cur_song
                             output_path = self._output_path + data_in_folder + '/' + output_name
                             selected_function(input_file, output_path)
