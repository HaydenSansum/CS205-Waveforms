import numpy as np

def one_hot_encode_chunk(data_chunk, n_channels=256):
    '''
    Simple manual onehot encoding by creating a 2d array output from a 1d input vector
    '''
    data_chunk_array = np.array(data_chunk)

    encoded_data = np.zeros((len(data_chunk_array), n_channels))
    encoded_data[np.arange(len(data_chunk_array)), data_chunk_array-1] = 1

    return encoded_data

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


def split_song_to_train(input_data, data_size, data_collect_stride):
    '''
    
    '''
    # Iterate through the song data to return the correct chunk one at a time
    keep_iter = True
    i_iter = 0
    
    # Set up list of datasets
    x_data = []

    while keep_iter == True:

        song_chunk, keep_iter = get_chunk(input_data, i_iter, data_size, keep_iter)
        
        if keep_iter == True:
            x_data.append(song_chunk)    
            i_iter += data_collect_stride

    return x_data

