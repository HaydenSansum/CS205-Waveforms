import numpy as np
import pandas as pd
import pickle
import os
import re
import random


def gen_songs_from_pickle(data_path, data_size, n_stride, n_channels, onehot=True, genres_to_train=None, shuffle=True, seed=None):
    '''
    Given a data path to a set of song folders (labeled by genre) iterate through and yield chunks
    of songs (in binary pickle format). Each chunk should match the data size and a song should be used 
    up before moving onto the next song.

    Songs need to be returned in overlapping windows set by n_stride.

    This can be randomized to shuffle genres together or aid training or be kept in the order
    files appear in the directory.

    inputs:
        data_path - str - absolute or relative filepath to the pickle data
        data_size - int - the number of data samples to return (aka 1024)
        n_stride - int - number of samples to stride across for each chunk
        onehot - bool - return the data as flat array or one hot encoded np.array
        genre_to_train - list - list of genres which the model will utilize as training data
        shuffle - bool - whether to shuffle the training data
        seed - int - random seed for reproducibility (can be None)

    outputs:
        chunk of song data as either list or np.array
    '''
    if seed:
        random.seed(seed)

    available_song_paths = get_all_song_paths(data_path, genres_to_train)

    if shuffle==True:
        random.shuffle(available_song_paths)

    # Iterate through each available song and store it's data into memory
    for song_path in available_song_paths:
        with open(song_path, 'rb') as pickfile:
            song_pickle_data = pickle.load(pickfile)

            # Iterate through the song data to return the correct chunk one at a time
            keep_iter = True
            i_iter = 0
            while keep_iter == True:
                song_chunk, keep_iter = get_chunk(song_pickle_data, i_iter, data_size, keep_iter)
                i_iter += n_stride
                if keep_iter == True:
                    if onehot == True:
                        yield one_hot_encode_chunk(song_chunk[:,0], n_channels)
                    else:
                        yield song_chunk[:,0]
                else:
                    pass
                

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


def get_all_song_paths(data_path, genres_to_train):
    '''
    Helper function to get all available song paths from the data path
    '''
    all_folders = [folder for folder in os.listdir(data_path) if os.path.isdir(data_path + folder)]

    available_song_paths = []

    # Generate a clean list of available songs to train on from within Genres
    for folder in all_folders:
        if genres_to_train == None or folder in genres_to_train: # Otherwise don't include
            
            all_songs = get_all_songs(path=(data_path + folder), filetype='pkl')
            for song in all_songs:
                available_song_paths.append(data_path + folder + '/' + song)

    return available_song_paths


def get_chunk(data, st_val, size, keep_iter):
    '''
    Grab a chunk of a song object and return the chunk plus whether the chunk is exhausted
    '''
    end_val = st_val + size
    try:
        chunk = data[st_val:end_val]
        if len(chunk) != size:
            chunk = None
            keep_iter=False
    except:
        chunk = None
        keep_iter = False
    return chunk, keep_iter


def one_hot_encode_chunk(data_chunk, n_channels):
    '''
    Simple manual onehot encoding by creating a 2d array output from a 1d input vector
    '''
    data_chunk_array = np.array(data_chunk)

    encoded_data = np.zeros((len(data_chunk_array), n_channels))
    encoded_data[np.arange(len(data_chunk_array)), data_chunk_array-1] = 1

    return encoded_data


def get_available_genres(data_path):
    '''
    Helper function to return a list of the available Genre folders which exist and 
    contain clean songs in correct format
    '''
    all_folders = [folder for folder in os.listdir(data_path) if os.path.isdir(data_path + folder)]
    return(all_folders)
