def normalize_song(song):
    '''
    Given a song with arbitary continous values, rescale to be between -1 and 1
    '''
    new_song = song
    
    max_ch = np.max(abs(new_song))
    
    overall_max = np.max(max_ch)
    
    # Convert to float
    normalized_song = new_song / overall_max

    normalized_song = normalized_song.transpose()
    
    return normalized_song


def mu_law(song, mu=255):
    '''
    Apply the mu law as described in Wavenet paper
    This is a more realistic compression of audio space than simple linear interpretation
    '''
    new_song = song
    scaled_song = np.sign(new_song) * (np.log(1 + mu * abs(new_song)) / np.log(1 + mu))
    
    return scaled_song


def song_digitizer(input_song, n_out_channels = 256):
    '''
    Convert continuous values to bins with n_channels (generally used on data normalized)
    between -1 and 1
    '''
    song_data = input_song

    song_data = normalize_song(song_data)
    song_data = mu_law(song_data)

    min_val = np.min(song_data)
    max_val = np.max(song_data)

    bin_cutoffs = np.linspace(min_val, max_val, n_out_channels)
    new_ch = np.digitize(song_data, bin_cutoffs)

    # Change back to int
    final_song = new_ch.astype('int16')

    final_song = final_song.transpose()

    return final_song


def song_downsampler(input_song, n_out_channels = 256, input_freq = 44100, output_freq=8000):
    '''
    Uses resampys downsampler to convert to lower number of data points without ruining the
    audio file
    '''

    ds_ch = resampy.resample(input_song.astype(np.float), input_freq, output_freq)

    ds_song = ds_ch.transpose()

    return ds_song

def mp3_to_wavdata(song_file):
    '''
    reads in mp3 files, uses pydub,ffmpeg to convert them into wav
    wav file is exported to a temp path, and read back into data with scipy wavfile
    '''
    #Ignore hidden files
    if not re.match(r'^[.].*', song_file):
        # Read from mp3 and save to tempfile as wav
        a_segment = AudioSegment.from_mp3(song_file)
        _, temp_path = tempfile.mkstemp()
        a_segment.export(temp_path, format="wav")

        # read in wav tempfile and extract data
        rate, songdata = wavfile.read(temp_path)
        myout = songdata[:,0]
    return song_file, myout