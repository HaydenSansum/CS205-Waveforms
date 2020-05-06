import numpy as np
import pandas as pd
import pickle
import os
import re
import random

def gen_songs_from_pickle(data_path, genres_to_train=None, shuffle=True, seed=None):
    '''

    '''
    all_folders = [folder for folder in os.listdir(data_path) if os.path.isdir(data_path + folder)]

    if seed:
        random.seed(seed)

    available_song_paths = []

    # Generate a clean list of available songs to train on from within Genres
    for folder in all_folders:
        if genres_to_train == None or folder in genres_to_train: # Otherwise don't include
            
            all_songs = get_all_songs(path=(data_path + folder), filetype='pkl')
            for song in all_songs:
                available_song_paths.append(data_path + folder + '/' + song)

    if shuffle==True:
        random.shuffle(available_song_paths)

    # For each of the available songs pass out one at a time when requested
    for song_path in available_song_paths:
        with open(song_path, 'rb') as pickfile:
            song_pickle_data = pickle.load(pickfile)
            yield song_pickle_data


def get_all_songs(path, filetype):
    '''
    Ported over from the file transformer object - allows for an easy way to detect
    all files of a specific type in a folder
    '''
    all_files = os.listdir(path)

    # Test for filetype:
    expr = f".*\.{filetype}"
    specific_files = [re.match(expr, cur_file) for cur_file in all_files]

    clean_files = []
    for cur_file in specific_files:
        if cur_file:
            clean_files.append(cur_file.string)

    return(clean_files)

def get_available_genres(data_path):
    '''
    Helper function to return a list of the available Genre folders which exist and 
    contain clean songs in correct format
    '''
    all_folders = [folder for folder in os.listdir(data_path) if os.path.isdir(data_path + folder)]
    return(all_folders)
