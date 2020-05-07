import numpy as np
import resampy

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


def inverse_mu_law(song, mu=255):
    '''
    Rescale to between -1 and 1 and then inverse mu law
    '''
    max_val = np.max(abs(song))

    # Rescale to between zero and 2
    norm_song = song / (max_val * 0.5)

    # Rescale to between -1 and 1
    norm_song = norm_song - (max_val * 0.5)

    inv_mu_song = np.sign(song) * (1/mu) * ((1 + mu)**(abs(song)) - 1)
    
    return inv_mu_song


def inverse_normalize_song(song, max_val = 32000):
    '''
    Expand the song values back out to be the correct scale for WAV

    Must be applied after inverse mu law
    '''
    cur_max = np.max(abs(song))
    rescale_factor = max_val / cur_max

    wav_scale_song = song * rescale_factor

    return wav_scale_song


def decode_onehot(song):
    '''
    Reverse the one hot encoding of a song back to a single array
    '''
    song_array = np.argmax(song, axis=1)
    return(song_array)



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


def song_downsampler(input_song, n_out_channels = 256, input_freq = 44100, output_freq=8000):
    '''
    Uses resampys downsampler to convert to lower number of data points without ruining the
    audio file
    '''
    down_song = input_song.copy()

    ds_ch1 = down_song[:,0]
    ds_ch2 = down_song[:,1]

    ds_ch1 = resampy.resample(ds_ch1, input_freq, output_freq)
    ds_ch2 = resampy.resample(ds_ch2, input_freq, output_freq)

    ds_song = np.vstack([ds_ch1, ds_ch2])
    ds_song = ds_song.transpose()

    return ds_song