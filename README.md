# CS205-Waveforms

## Overview

Welcome to our CS205 final project - investigating the potentials of parallel computing to speed up, and therefore allow for the training of a deep, convolutional Wavenet model using PySpark and Keras for predictions of innovative audio. This repository contains all the code, documentation and reproducibility information required for you to attempt building your own version.

The codebase is broadly split into two categories - local code used for development and baselining but not intended for reproducibility and the AWS version of the code which (given access to the S3 song data or pointing the filepaths to a different repository) will enable model training in minutes. We decided to keep these two version separate (even though there is overlap) to ensure that the specific versions do not interfere where they have been edited for their specific systems.


![Overview of the Wavenet Parallelization](docs/imgs/NW_highlevel.png)

The above diagram highlights at a high level our approach to parallelizing this Wavenet, audio predictive model.


### How it Works

The approach can be split into four major segments:
1. Webscraping songs from FMA (in mp3 format)
2. Converting and preprocessing songs into a clean binary format (an array on values)
3. Utilizing the custom data generator to train the Neural Network (Wavenet model) in a memory efficent manner
4. Making predictions from the Wavenet model to create new songs.


## Code

The codebase is divided into three sections - local, aws and test codes. We decided to use this split for simplicity so that functions could be modified directly to work with AWS and Spark due to the different, packaging, methods and approach to data processing, there is however therefore some duplication in the function code which in future we'd like to split out into a folder which spans both approach.

Test code is for any debugging, test or examples used in development.

### Local Mode - Instructions

Local mode is designed to work on a local machine (mac, linux or windows) and hence is not designed for full reproduciblity. It is however the baseline environment for development of the code base (without paying for AWS instances) and was used to build and test the required data flow and model building functions.

This also allows for users to get up and running relatively quickly (albeit with some potential backend software/hardware dependency issues) without needing access to AWS or paying for AWS EMR instances.

Local mode can be found in the folders `code/local/`

To run the local mode the first step is to ensure key dependices are set up:
1. `FFMPEG` - this is the library which allows for mp3 conversion to wav. Please install the latest, the easiest method is via brew with `brew install ffmpeg`
2. Set up a new python3 virtual environment (ensure Python3 is installed) and load in the requirements file:
    a. `python3 -m venv waveforms_env`
    b. `source waveforms_env/bin/activate`
    c. `pip install -r local_requirements.txt`

The only scripts which need to be run are prefixed with "run_" and fall into the 4 major categories above, they are:
1. `run_webscraper.py`
2. `run_transformation_scripts.py`
3. `run_model_training.py`
4. `run_model_predictions.py`

If you wish to learn more about the specific of what each of the above processes are doing please see the AWS section where it is explained in further detail.

Each file has a clearly defined section at the top which will need editting to set up key parameters (mostly file system parameters). If you follow the file structure guide to create the required data subfolders this should be set up by default as it utilizes relative filepaths.

Running each of these scripts will take a few hours (model train and predict can take up to an hour each depending on datasize)

**NOTE**: For local model we'd highly recommend having fewer than 10 songs to train the model on and using either `filter_sizes = [64, 64, 64, 128]` or smaller otherwise the model train time will be prohibitive.

**NOTE2** Predicting a new song is also slow locally and hence we wouldn't recommend predicting more than 10 seconds of Audio at a time (~1hr).



### AWS Mode - Instructions

The approach on AWS remains similar to the above albeit much of the code is actually simplified by leverage mapping operations in Pyspark. In the `code/aws` folder are two main sections - data processing codes and model building codes. They can be run sequentially or separately on two different instances.

Files are stores on our S3 cloud repository which is not open to the public. Please message through github to request read access. The easiest option is to set up your own S3 bucket which then needs to be incorporated so that the I/O go to and from the correct place.

#### Web scraping

The webscraper is very straightforward - it requires an EC2 instance (any size is fine, we ran on a t2.micro for cost efficiency, there is no inherent speed up due to API rate limiting). 

1. `transfer_webscrape_files.sh hadoop@ec2(instance-id) ssh-key-id`
2. `scraper_setup.sh`
3. `vim scraper_aws.py` - edit the parameters at the top of the file to define scraping and S3 storage parameters
3. `python scraper_aws.py`

This will automatically scrape files and place directly into the S3 bucket so there is no issue with memory (1000 files is approximately 10GB in size). The next stages of the code then read from these raw data buckets as part of the model pipeline.

#### Data Pre-processing

In order to perform the data preprocessing, on aws, first create an EMR cluster using the online UI.

Once the AWS instance is up and running and you are connect you can run the following commands (ensure you're in the `code/aws/` directory):

1. [LOCAL] `source transfer_files.sh hadoop@ec2(instance-id) ssh-key-id` Transfer all required files to AWS instance 
2. [AWS] `source test_hdfs.sh` Test connection to HDFS 

**NOTE** This should list an `input.txt` and an `output.txt` in the HDFS. Sometimes inexplicably the AWS instance will lose access to, or not have access to the HDFS. We tried to debug to see whether it was related to some other software dependencies but found it would occur sporadically and seemly at random even without changing any infrastructure. If this occurs the only fix we found was to restart the instance.

3. [AWS] `setMaster('local[#]')` in `spark_preprocessing.py` Choose number of localmode cores to run in by editing the number  

**NOTE** At this time, our codebase framework does not have full support for clustermode implementation. Though the pyspark framework on EMR is generally easily extendable, we encountered major aws issues that restricted us from getting the processing running on the worker nodes. Please see website page discussion for further details.

4. [LOCAL] `process_mp3.sh` Upload a collection of mp3 songs to S3 bucket - enabling privacy permissions so as to access from EMR master, editing the bucket in  (or just using the default one) 

5. [AWS] `process_mp3.sh` Run the bash script helper function 

   * This script first creates a new directory `input_songs` in your home directory
   * It then uses `aws s3 sync` to pull mp3 songs from an S3 bucket and adds them into HDFS.
   * It then runs the preprocessing file `spark_preprocessing.py` on the defined number of workers, which will write the processed song data in a `pickle` form back into HDFS.
   * The script concludes by retrieving the processed files back into the home directory

6. [AWS] `aws s3 cp processed_songs s3://waveform-storage/ --recursive` For later access to the processed files, upload them back into the S3 bucket with their mp3 counterparts using


#### Model Training

In order to train the model on AWS there are a number of clear steps to take listed below. We highly recommend using at least an m4.2xlarge if not a 4x or 8x due to the increased RAM and capacity to process the large volumes of data involved. The model is trained via an RDD called from the HDFS file system and so it is memory efficient but the batching and dividing out of samples which occurs as part of the data generator to train the model can cause memory issues on small instances.

1. [AWS] `source elephas_setup.sh` Run the bash script to install all dependencies 
2. [AWS] `mkdir processed_songs `(Can skip to step 5 if coming directly from data preprocessing steps)
3. [AWS] `aws s3 sync s3://waveform-storage/input_data/song_processed/Pop/hsbatch processed_songs`
4. [AWS] `hadoop fs -put processed_songs/part-00001`
5. [AWS] `time spark-submit --driver-memory 4G spark_build_model.py`

Again another issue with running the model training (only occuring in asynchronous training mode) is that the FLASH APP that it relies on uses up and hogs the available ports.

If you see the error:
`error: [Errno 98] Address already in use`

Follow these instructions
https://medium.com/@sanzidkawsar/the-python-flask-problem-oserror-errno-98-address-already-in-use-flask-49daaccaef4f

The model should now be running and training! Some of the key parameters to tune for the model fitting are:

* num_worker (the number of workers that the SPARKMODEL splits the data into)
* num_nodes (the number of cores to user on local mode)
* Layers and Stacks
* Batch size and optimizer parameters
* Elephas parameters - sychronous vs asynchronous

The model will automatically be saved based on the parameters specified in the spark_build_model file (a `.json` file) and the weights will also be saved alongisde (`.h5` file). These can both be transferred back to local hardware for predictions as the predictions cannot be parallelized, are very slow and hence expensive to run on a large AWS instance like this. For song predictios please see the local mode above.

**NOTE** Code for AWS predictions are a next step for this project.
