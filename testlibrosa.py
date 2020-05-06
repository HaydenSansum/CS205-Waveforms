import librosa
import warnings
import os
import re
import numpy as np

import time
warnings.filterwarnings('ignore')


filepath = 'songs/mp3/Dance/Song8_Dee_Yan-Key_-_06_-_Six.mp3'
# start1 = time.time()
# y, sr = librosa.load(filepath)
# print(time.time()- start1)
# np.savetxt('librosa.txt',y)
# print('rate1',sr)


from scipy.io import wavfile
from pydub import AudioSegment
import tempfile
# mp3 = AudioSegment.from_mp3(filepath)
# _, path = tempfile.mkstemp()
# mp3.export(path, format="wav")
# rate, data = wavfile.read(path)

a_segment = AudioSegment.from_mp3(filepath)
_, temp_path = tempfile.mkstemp()
a_segment.export(temp_path, format="wav")
rate, songdata = wavfile.read(temp_path)

print(len(songdata[:,0]))

# np.savetxt("songout.csv", songdata, delimiter=",")
