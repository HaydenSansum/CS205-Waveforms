---
title: Background
---

## Motivation

With machine understanding of sound and natural speech having been revolutionized over the last decade, the task of audio generation is an important next step to realizing the long-standing computational dream of enabling human-machine conversation. Despite recent progress, audio generation remains a highly intensive (and slow) task, as it requires both huge amounts of data and complex networks for training. Thus, this task is one of many that sits at the intersection between Big Data and Big Compute. We discuss computational infrastructure for song generation, an instance of the broader task of audio signal synthesis, which aims to mitigate the computational costs (both time and money) of this task.

## Big Data

We train our fully convolutional model (described in detail below) on thousands of raw song waveforms which range in size up to 4GB per song. Each song contains over 44,000 sample points per second with 16 bits per sample (over 65,000 discrete output channels). Training an effective model thus requires gathering thousands of unique songs, i.e. TBs of data. Moreover, several preprocessing operations must be performed on each song, including file conversion from mp3 to wav form, downsampling, binning (digitizing to collapse the number output audio channels), and splitting into smaller chunks to speed up new song generation. The figure below shows a profile of serial implementation of these operations, which appear to follow an approximately linear time relationship with the number of songs.

Scraping song files from the FMA website, converting them from mp3 to wav, and digitizing them take approximately 1.75 seconds per song, 1.25 seconds per song, and 1.25 seconds per song, respectively. Thus, we face a data collection bottleneck that must be surmounted in order to acquire the high volume of songs needed for model training. These operations are not particularly complex, and fit well into a Spark MapReduce framework on AWS EMR to parallelize the execution of these operations across all songs. We discuss the results of this parallelization below.


## Big Compute







