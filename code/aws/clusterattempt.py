import re
import os
import numpy as np
import resampy
from pydub import AudioSegment
from scipy.io import wavfile
import tempfile


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
        data_out = songdata[:,0]
    return data_out


from pyspark import SparkConf, SparkContext, SQLContext, SparkFiles
from pyspark.sql import SparkSession
from pyspark.sql.types import *
import os
import time

# # Old version
conf = SparkConf().setAppName('song_converter')
sc=SparkContext(conf=conf)

# # New Spark
# spark = SparkSession.builder.master("local").appName("song_converter").getOrCreate()

# Parameters
n_partitions = 32

# File Paths                                                            
input_song_dir = "batch100/"

# sc.addFile("batch100",recursive=True)
# sc.addFile("Song46_Scott_Holmes_-_03_-_-_Humanity.mp3",recursive=True)
# sc.addFile("Song468_Scott_Holmes_-_13_-_Big_Apple.mp3",recursive=True)
# all_songs = ['Song46_Scott_Holmes_-_03_-_-_Humanity.mp3','Song468_Scott_Holmes_-_13_-_Big_Apple.mp3']



# sc.addFile('hdfs:///ip-172-31-29-25.us-east-2.compute.internal:8020/batch100',recursive=True)
# # Which songs to pull in

# sc.addFile("batch100/*",recursive=True)

all_songs = ['Song464_Scott_Holmes_-_11_-_Make_Your_Dream_Reality.mp3', 'Song432_Podington_Bear_-_13_-_Brie.mp3', 'Song468_Scott_Holmes_-_13_-_Big_Apple.mp3', 'Song381_A_A_Aalto_-_Sneak.mp3', 'Song403_Benjamin_Bret_-_08_-_La_Porte_Mtallique.mp3', 'Song447_Simon_Mathewson_-_05_-_The_Smallest_Yeti.mp3', 'Song454_Simon_Mathewson_-_13_-_High_and_Dry-mouthed.mp3', 'Song407_Benjamin_Bret_-_04_-_Black_Kracougol.mp3', 'Song399_Benjamin_Bret_-_12_-_Comme_Moi.mp3', 'Song44_Derek_Clegg_-_01_-_Youre_The_Dummy.mp3', 'Song404_Benjamin_Bret_-_07_-_CD.mp3', 'Song446_Simon_Mathewson_-_04_-_Theos_Rhyme.mp3', 'Song422_Podington_Bear_-_04_-_Mouse_On_Mars.mp3', 'Song463_Scott_Holmes_-_07_-_Think_BIG.mp3', 'Song438_Sweet_N_Ju_-_05_-_Sweet_N_Juicy-Anything_For_You-Mar_2018-LIVE.mp3', 'Song466_Scott_Holmes_-_08_-_Motivational.mp3', 'Song380_Vincent_Augustus_-_woah.mp3', 'Song465_Scott_Holmes_-_06_-_Reach_for_Success.mp3', 'Song396_Mutestare_-_02_-_The_Golden_Homunculous.mp3', 'Song387_A_A_Aalto_-_Archipelago.mp3', 'Song401_Benjamin_Bret_-_10_-_Le_Festival.mp3', 'Song430_Podington_Bear_-_05_-_Dim_Dim.mp3', 'Song409_Benjamin_Bret_-_02_-_La_Bouteille_de_Whisky.mp3', 'Song429_Podington_Bear_-_14_-_Feta.mp3', 'Song417_Phillip_Gross_-_04_-_Swirling_Liquid.mp3', 'Song383_A_A_Aalto_-_Red_Wing.mp3', 'Song427_Podington_Bear_-_07_-_Hot_Chip.mp3', 'Song440_Sweet_N_-_03_-_Sweet_N_Juicy-Say_Hi-Mar_2018-LIVE.mp3', 'Song443_Vincent_Augustus_-_chonk.mp3', 'Song391_Branch_Line_Idols_-_07_-_Decision_For_You.mp3', 'Song394_Xqui_-_04_-_Orange.mp3', 'Song411_Joe_Kye_-_01_-_Joe_Kye-July_2018-LIVE.mp3', 'Song45_Scott_Holmes_-_02_-_-_Together_We_Stand.mp3', 'Song395_Vukovar_-_03_-_Tryst_of_Emanations.mp3', 'Song41_Small_Tall_Order_-_02_-_My_Fault.mp3', 'Song457_Simon_Mathewson_-_09_-_Basic_Interaction_Skills.mp3', 'Song405_Benjamin_Bret_-_06_-_La_Cantine.mp3', 'Song456_Simon_Mathewson_-_03_-_Chinless_Wonder.mp3', 'Song439_Sweet_N_Juicy_-_04_-_Sweet_N_Juicy-Haskins-Mar_2018-LIVE.mp3', 'Song414_Scott_Holmes_-_05_-_Corporate_Software.mp3', 'Song435_Greg_Atkinson_-_01_-_Name_This_Love.mp3', 'Song385_A_A_Aalto_-_Lantern_Music.mp3', 'Song413_Scott_Holmes_-_04_-_Happy_Ukulele.mp3', 'Song421_Podington_Bear_-_06_-_The_Album_Leaf.mp3', 'Song433_Podington_Bear_-_12_-_Blue.mp3', 'Song431_Podington_Bear_-_10_-_Cornershop.mp3', 'Song393_Brevyn_-_05_-_Sea_Cave.mp3', 'Song40_Silva_de_Alegria_-_03_-_El_Camino_del_Alce.mp3', 'Song453_Simon_Mathewson_-_07_-_Most_Unkind.mp3', 'Song43_Simon_Mathewson_-_Lonely_Cowboys.mp3', 'Song402_Benjamin_Bret_-_09_-_Marin_Marrant.mp3', 'Song423_Podington_Bear_-_15_-_Mont_Blanc.mp3', 'Song415_Phillip_Gross_-_02_-_Electric_Critters.mp3', 'Song400_Benjamin_Bret_-_11_-_Ide_de_Merde.mp3', 'Song390_Osiris_Saline_-_08_-_Tend_to_It.mp3', 'Song420_Podington_Bear_-_02_-_Thom_Yorke_At_Home.mp3', 'Song397_Kariatida_-_01_-_Belle_et_triste.mp3', 'Song461_Scott_Holmes_-_09_-_We_Made_It.mp3', 'Song406_Benjamin_Bret_-_05_-_Un_Muse_de_Vieilles_Merdes_sa.mp3', 'Song436_Sweet_N_-_07_-_Sweet_N_Juicy-Irresistable-Mar_2018-LIVE.mp3', 'Song419_Vincent_Augustus_-_light.mp3', 'Song38_Silva_de_Alegria_-_10_-_Primavera_en_la_Guerra_del_Sonido.mp3', 'Song386_A_A_Aalto_-_Bazaar.mp3', 'Song426_Podington_Bear_-_03_-_James_Murphy.mp3', 'Song398_Benjamin_Bret_-_13_-_Dans_un_Bar_de_Brest.mp3', 'Song39_Silva_de_Alegria_-_05_-_Veris_Bellum_Sonus.mp3', 'Song425_Podington_Bear_-_09_-_Lily_Allen.mp3', 'Song384_A_A_Aalto_-_Neat_As_A_Pin.mp3', 'Song389_Richey_Hackett_-_09_-_The_Ambulance.mp3', 'Song450_Simon_Mathewson_-_14_-_Queuing_Loons.mp3', 'Song442_Sweet_N_Juicy_-_01_-_Sweet_N_Juicy-Golden-Mar_2018-LIVE.mp3', 'Song388_J_G_Hackett_-_10_-_Now_Experience_Each_Others_Deaths_Through_Social_Media.mp3', 'Song444_Krestovsky_-_08_-_Paroled.mp3', 'Song412_Scott_Holmes_-_12_-_Feeling_Sunny.mp3', 'Song462_Scott_Holmes_-_05_-_Beyond_Dreams.mp3', 'Song3_Scott_Holmes_-_01_-_Storybook.mp3', 'Song418_Phillip_Gross_-_01_-_Cyber-_Rhythm.mp3', 'Song382_A_A_Aalto_-_Skip_Song.mp3', 'Song410_Benjamin_Bret_-_01_-_LEtron.mp3', 'Song424_Podington_Bear_-_11_-_Massive_Attack.mp3', 'Song392_Delicasession_-_06_-_Illusions_Part_1.mp3', 'Song458_Simon_Mathewson_-_10_-_At_the_End_Begin.mp3', 'Song428_Podington_Bear_-_08_-_Gruyere.mp3', 'Song455_Simon_Mathewson_-_15_-_Greek_Belief_Assunder.mp3', 'Song452_Simon_Mathewson_-_08_-_Never_Be_Forgot.mp3', 'Song459_Simon_Mathewson_-_01_-_Bad_School_Trip.mp3', 'Song448_Simon_Mathewson_-_12_-_Solid_Noise.mp3', 'Song449_Simon_Mathewson_-_02_-_Saline_Cluster.mp3', 'Song42_01_-_Until_We_Get_By.mp3', 'Song467_Scott_Holmes_-_12_-_Shine_Bright.mp3', 'Song434_Podington_Bear_-_01_-_Bjork.mp3', 'Song416_Phillip_Gross_-_03_-_Optimistic_Bits.mp3', 'Song451_Simon_Mathewson_-_11_-_Numbers_Rap_Reprise.mp3', 'Song437_Sweet_N_Ju_-_06_-_Sweet_N_Juicy-Whats_Good-Mar_2018-LIVE.mp3', 'Song460_Scott_Holmes_-_10_-_Follow_your_Dreams.mp3', 'Song445_Simon_Mathewson_-_06_-_When_You.mp3', 'Song46_Scott_Holmes_-_03_-_-_Humanity.mp3', 'Song408_Benjamin_Bret_-_03_-_Le_Pull_Kitsch.mp3', 'Song469_Ayato__Kecap_Tuyul_-_12_-_Empty_Saloon_Dance.mp3', 'Song441_Sweet_N_-_02_-_Sweet_N_Juicy-Complicate_Me-Mar_2018-LIVE.mp3']
for song in all_songs:
    sc.addFile(song)


# all_songs=[song for song in os.listdir(input_song_dir)]
# print(all_songs)
# all_songs = all_songs[0:100]

print("here", SparkFiles.getRootDirectory())

start = time.time()
rdd = sc.parallelize(all_songs) \
            .map(mp3_to_wavdata) \
            .map(song_downsampler) \
            .map(song_digitizer) \
            .map(lambda x: x.tolist())

print("MyPartitions", rdd.getNumPartitions())

rdd.saveAsPickleFile('finaleh')





cd /usr/local/bin
sudo wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
sudo wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz.md5
sudo tar xvf ffmpeg-git-amd64-static.tar.xz
sudo mv ffmpeg-git-20200504-amd64-static/ffmpeg ffmpeg-git-20200504-amd64-static/ffprobe /usr/local/bin/
sudo ln -s /usr/local/bin/ffmpeg/ffmpeg /usr/bin/ffmpeg
cd ~
echo "export PATH=~/usr/local/bin:$PATH" >>~/.bash_profile
echo "export PATH=~/.local/bin:$PATH" >>~/.bash_profile
echo "export PATH=~/usr/local/bin/ffmpeg:$PATH" >>~/.bash_profile
echo "export PATH=/usr/local/bin:$PATH" >>~/.bash_profile
echo "export PATH=/usr/local/bin/ffmpeg:$PATH" >>~/.bash_profile
echo "export PATH=/usr/bin:$PATH" >>~/.bash_profile
echo "export PATH=/usr/bin/ffmpeg:$PATH" >>~/.bash_profile
source ~/.bash_profile
pip install --upgrade pip
sudo ln -s /usr/local/bin/pip /usr/bin/pip
pip install wheel
yum install numba
pip install -r emr_requirements_preprocessing.txt


# export PATH=~/usr/local/bin:$PATH
# export PATH=~/.local/bin:$PATH
# export PATH=/usr/bin:$PATH
# export PATH=/usr/local/bin:$PATH
# export PATH=~/usr/local/bin/ffmpeg:$PATH
# export PATH=/usr/local/bin/ffmpeg:$PATH
# export PATH=/usr/bin/ffmpeg:$PATH









aws-cfn-bootstrap==1.4
awscli==1.16.102
Babel==0.9.4
backports.functools-lru-cache==1.6.1
backports.ssl-match-hostname==3.4.0.2
beautifulsoup4==4.8.1
boto==2.48.0
boto3==1.13.0
botocore==1.12.92
bs4==0.0.1
certifi==2020.4.5.1
chardet==3.0.4
Cheetah==2.4.4
cloud-init==0.7.6
colorama==0.2.5
configobj==4.7.2
Cython==0.29.17
docutils==0.11
ecdsa==0.11
enum34==1.1.10
funcsigs==1.0.2
futures==3.0.3
hibagent==1.0.0
idna==2.9
iniparse==0.3.1
Jinja2==2.7.2
jmespath==0.9.2
jsonpatch==1.2
jsonpointer==1.0
kitchen==1.1.1
lockfile==0.8
lxml==4.4.2
Markdown==3.1.1
MarkupSafe==0.11
mysqlclient==1.4.6
nltk==3.4.5
nose==1.3.4
numba==0.13.0
numpy==1.16.6
oauth==1.0.1
pandas==0.24.2
paramiko==1.15.1
PIL==1.1.6
ply==3.4
prettytable==0.7.2
py4j==0.10.7
pyasn1==0.1.7
pycrypto==2.6.1
pycurl==7.19.0
pydub==0.23.1
pygpgme==0.3
pyliblzma==0.5.3
pyserial==3.4
pyspark==2.3.2
pystache==0.5.3
python-daemon==1.5.2
python-dateutil==2.5.0
python27-sagemaker-pyspark==1.2.6
pytz==2020.1
pyxattr==0.5.0
PyYAML==3.11
requests==2.23.0
resampy==0.1.5
rsa==3.4.1
s3transfer==0.3.3
scipy==1.2.3
simplejson==3.6.5
singledispatch==3.4.0.3
six==1.8.0
soupsieve==1.9.5
urlgrabber==3.10
urllib3==1.24.3
virtualenv==15.1.0
wget==3.2
windmill==1.6
yum-metadata-parser==1.1.4