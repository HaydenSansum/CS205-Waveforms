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

On the AWS EC2 instance follow these instructions:
https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html

This should then provide access to the S3 bucket from the AWS EC2 instance.


