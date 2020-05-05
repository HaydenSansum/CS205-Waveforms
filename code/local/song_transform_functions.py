import numpy as np

# ============ HELPER FUNCTIONS ================
def normalize_song(song):
    '''
    Given a song with arbitary continous values, rescale to be between -1 and 1
    '''
    new_song = song.copy()
    
    max_ch1 = np.max(abs(new_song[:,0]))
    max_ch2 = np.max(abs(new_song[:,1]))
    
    overall_max = np.max([max_ch1, max_ch2])
    
    # Convert to float
    new_ch1 = new_song[:,0] / overall_max
    new_ch2 = new_song[:,1] / overall_max

    normalized_song = np.vstack([new_ch1, new_ch2])
    normalized_song = normalized_song.transpose()
    
    return normalized_song


def mu_law(song, mu=255):
    '''
    Apply the mu law as described in Wavenet paper
    This is a more realistic compression of audio space than simple linear interpretation
    '''
    new_song = song.copy()
    scaled_song = np.sign(new_song) * (np.log(1 + mu * abs(new_song)) / np.log(1 + mu))
    
    return scaled_song


# ============ APPLICATION FUNCTIONS ==============
def song_digitizer(input_song, n_out_channels = 256):
    '''
    Convert continuous values to bins with n_channels (generally used on data normalized)
    between -1 and 1
    '''
    song_data = input_song

    song_data = normalize_song(song_data)
    song_data = mu_law(song_data)

    min_val = np.min(song_data[:,0])
    max_val = np.max(song_data[:,1])

    bin_cutoffs = np.linspace(min_val, max_val, n_out_channels)
    new_ch1 = np.digitize(song_data[:,0], bin_cutoffs)
    new_ch2 = np.digitize(song_data[:,1], bin_cutoffs)

    # Change back to int
    new_ch1 = new_ch1.astype('int16')
    new_ch2 = new_ch2.astype('int16')

    final_song = np.vstack([new_ch1, new_ch2])
    final_song = final_song.transpose()

    return final_song

def song_downsampler(input_song, output_path, n_out_channels = 256, output_freq=44100):
    pass