# CS205-Waveforms

## Overview


### How it Works

The approach can be split into foru major segments:
1. Webscraping songs from FMA (in mp3 format)
2. Converting and preprocessing songs into a clean binary format (an array on values)
3. Utilizing the custom data generator to train the Neural Network (Wavenet model) in a memory efficent manner
4. Making predictions from the Wavenet model to create new songs.


## Code

The codebase is divided into three sections - local, aws and test codes. We decided to use this split for simplicity so that functions could be modified directly to work with AWS and Spark due to the different, packaging, methods and approach to data processing, there is however therefore some duplication in the function code which in future we'd like to split out into a folder which spans both approach.

Test code is for any debugging, test or examples used in development.

### Local Mode

Local mode is designed to work on a local machine (mac, linux or windows) and hence is not designed for full reproduciblity. It is however the baseline environment for development of the code base (without paying for AWS instances) and was used to build and test the required data flow and model building functions.

This also allows for users to get up and running relatively quickly (albeit with some potential backend software/hardware dependency issues) without needing access to AWS or paying for AWS EMR instances.

To run the local mode the first step is to ensure key dependices are set up:
* DEPENDCIES? (FFMPEG, Python, VENV, Packages)

The only scripts which need to be run are prefixed with "run_" and fall into the 4 major categories above, there are:
1. run_webscraper.py
2. run_transformation_scripts.py
3. run_model_training.py
4. run_model_predictions.py

Each file has a clearly defined section at the top which will need editting to set up key parameters (mostly file system parameters). If you follow the file structure guide to create the required data subfolders this should be set up by default as it utilizes relative filepaths.

Running each of these scripts will take a few hours (model train and predict can take up to an hour each depending on datasize)

**NOTE**: For local model we'd highly recommend having fewer than 10 songs to train the model on and using either `filter_sizes = [64, 64, 64, 128]` or smaller otherwise the model train time will be prohibitive.

**NOTE2** Predicting a new song is also slow locally and hence we wouldn't recommend predicting more than 10 seconds of Audio at a time (~1hr).


### AWS Mode

NEED TO WRITE UP INSTRUCTIONS HERE (Link to AWS_Setup.md)


## Ideas for write up:

* Timing of different spark nodes and sizes on data processing (can also do a cost to number of nodes ratio)
* Trying different types of instance (M4.large, M4.xlarge, M5...) and comparing the cost to performance ratio here


Model:
* Talk about generator approach to minize memory usage vs RDD approach on spark (not evaluated until pulled into model)
* Allows us to to train the 10 layer network locally which was failing before
* Trade off between input size and processing & Network complexity and training time

Issues:
* Synchronous vs asynchronous trainig and the kernel size of convolution
*