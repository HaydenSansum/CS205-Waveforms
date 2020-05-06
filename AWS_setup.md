# AWS 

In order to get the code running on AWS there are a number of steps to take in order to be set up consistently across all users.


### Storage

Firstly we need to be sure we all use the same S3 storage location - this will be the main repository for all our data files (code to remain on github as usual).

The bucket name is:
`waveform-storage`

First time you try to access it you will likely need to ask for permission so we can all see and access it.

The layout of the bucket is:

* waveform-storage
    * input_data
        * song_mp3 (raw scraped songs)
        * song_wav (converted to wav)
        * song_processed (processed and cleaned such as downsampling)
    * output_data
        * produced_songs (any outputs from the trained model)
    * models (storage of trained keras models)


### Flow

In general the flow on S3 will be:
1. A micro or small free tier EC2 compute unit will perform the webscraping, it will put data straight into an S3 bucket (see storage section).
2. An EMS Spark cluster will process the data, first converting to wav and saving in the relevant folder before performing the cleaning and again storing out.
3. An EMS Spark cluster leveraging Elephas will train the model (not sure how this works yet)
4. An EC2 unit can be used for generating the predictions - can test whether different sizes of unit make a difference in predict speeds.

### Basic EC2 Python Setup

NOTE: using Ubuntu 18... 

To get Python to work properly we need to ensure a consistent environment - hence we need pip and virtualenv, first use the following commands:

`curl -O https://bootstrap.pypa.io/get-pip.py`

`sudo apt-get install python3-distutils` (Say YES)

`python3 get-pip.py --user`

Add the following command to the bottom of the `.profile` file: (use sudo vim)

`export PATH=~/.local/bin:$PATH`

`source ~/.profile`

Now try: 

`pip3 --version` to ensure it is correctly installed.

Now install venv:

`python3 -m pip install --user virtualenv`

Activate the environment and install packages:

`virtualenv ~/cs205`

`source cs205/bin/activate`

`pip install -r requirements.txt`


### S3 Bucket - EC2 Connection Set up

In order for the webscraper to dump data into the S3 bucket it needs to be given access to the S3 bucket, this can be done by setting up an IAM profile by following the instructions here:

https://aws.amazon.com/premiumsupport/knowledge-center/ec2-instance-access-s3-bucket/

On the AWS EC2 instance follow these commands:

`curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"`

`sudo apt install unzip`

`unzip awscliv2.zip`

`sudo ./aws/install`

`aws s3 ls`

If all has worked you should see a list of AWS S3 buckets - hopefully including the waveforms-storage folder.

Further details can be found at this link:
https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html


Next we need to set up python to interface with the S3 buckets:

`pip install boto3` (hopefully included in the requirements txt so may not be needed)


Go to this link (section: Users, Permissions, and Credentials)

https://linuxacademy.com/guide/14209-automating-aws-with-python-and-boto3/

Follow the instructions for creating a role with an access and secret key.

NOTE: Download and store these keys locally otherwise you'll need to remake the role.

On EC2 again:

`aws configure`

Now input the following:
* ACCESS-KEY from the credentials.csv
* SECRET-KEY from the credentials.csv
* `us-east-2`
* `text`


### EMR Cluster

#### Installing FFMPEG

Instructions come from: https://www.johnvansickle.com/ffmpeg/faq/

`cd /usr/local/bin`

`sudo wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz`

`sudo wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz.md5`

`sudo tar xvf ffmpeg-git-amd64-static.tar.xz`

`sudo mv ffmpeg-git-20200504-amd64-static/ffmpeg ffmpeg-git-20200504-amd64-static/ffprobe /usr/local/bin/`

`sudo ln -s /usr/local/bin/ffmpeg/ffmpeg /usr/bin/ffmpeg`

`cd ~`

`sudo vim ~/.bash_profile` 

    Add the lines:
    
    `export PATH=~/usr/local/bin:$PATH`
    
    `export PATH=~/.local/bin:$PATH`
    
    `export PATH=~/usr/local/bin/ffmpeg:$PATH`
    
    `export PATH=/usr/local/bin:$PATH`
    
    `export PATH=/usr/local/bin/ffmpeg:$PATH`
    
    `export PATH=/usr/bin:$PATH`
    
    `export PATH=/usr/bin/ffmpeg:$PATH`

`source ~/.bash_profile`

#### Installing python packages

`pip install -r requirements.txt`
