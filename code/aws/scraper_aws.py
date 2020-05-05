import re
import requests
import wget
import boto3
import json
import time
from bs4 import BeautifulSoup

s3 = boto3.resource('s3')
client = boto3.client('s3')

# -----------------------
#       Parameters
# -----------------------
bucket_name = 'waveform-storage'
output_path = 'input_data/song_mp3/'
song_ref_dict = {}

# Need to specify a list of genres to scrape
genres = ['Pop']

# Specify the number of pages to scrape through (there are 20 songs per page)
page_nums = list(range(1,51))

# Set a scraping limit per page (1-20) - useful for testing if you only want a few songs
song_per_page_limit = 20


# -----------------------
#       Scraper
# -----------------------
# Scrape through specified parameters
for genre in genres:
    
    # Set up folders for each genre
    output_folder_path = output_path + genre + '/'

    # Check if the folder exists, if not create it
    result = client.list_objects(Bucket=bucket_name, Prefix=output_folder_path)
    if not result:
        s3.Bucket(bucket_name).put_object(Key=output_folder_path)

    clean_urls = []
    song_id = 0
    
    # Go through each page
    for i in page_nums:

        # Grab the HTML webpage and find all the links to each song
        page = requests.get(f"https://freemusicarchive.org/genre/{genre}?sort=track_date_published&d=1&page={i}")
        soup = BeautifulSoup(page.content, 'html.parser')
        playlist_space = soup.find(class_="playlist playlist-lrg")
        song_space = playlist_space.find_all(class_="icn-arrow")

        # Build a messy list of all the song URLS on the page
        list_of_urls = re.findall("(?<=href=)(.*?)( )", str(song_space))

        # Go through and clean each URL before scraping the song (Takes a while)
        for x in list_of_urls[0:song_per_page_limit]:
            clean_url_link = x[0][1:-1]
            clean_urls.append(clean_url_link) 

            song_name = clean_url_link.split("/")[-1]
            song_file = requests.get(clean_url_link)
            
            song_file_name = output_folder_path + 'Song' + str(song_id) + '_' + song_name
            s3.Bucket(bucket_name).put_object(Key=song_file_name, Body=song_file.content)
   
            # Iterate song ids
            song_id +=  1

            # Print to keep track of progress
            if song_id % 20 == 0:
                print(f'Scraped: {song_id} songs')

        # Wait for 2 seconds to ensure webserver isn't overloaed
        time.sleep(2)

    # Add URLS to dictionary for later use if needed
    song_ref_dict[genre] = clean_urls

# Write out the file dictionary as a JSON
song_id_json = json.dumps(song_ref_dict)
s3.Bucket(bucket_name).put_object(Key='input_data/song_id_dict.json', Body=song_id_json)

    