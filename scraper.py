import re
import requests
import wget
import os
import shutil
import json
from bs4 import BeautifulSoup

# -----------------------
#       Parameters
# -----------------------
output_path = 'songs/'
song_ref_dict = {}

# Need to specify a list of genres to scrape
genres = ['Dance', 'Experimental']

# Specify the number of pages to scrape through (there are 20 songs per page)
page_nums = list(range(1,3))

# Set a scraping limit per page (1-20) - useful for testing if you only want a few songs
song_per_page_limit = 2

# CAREFUL: - if TRUE will overwrite existing directory
overwrite_files = True

# -----------------------
#       Scraper
# -----------------------
# Scrape through specified parameters
for genre in genres:
    
    # Set up folders for each genre
    output_folder_path = output_path + genre + '/'

    # Delete existing directory if required
    if overwrite_files == True:
        if os.path.exists(output_folder_path):
            shutil.rmtree(output_folder_path)
        os.mkdir(output_folder_path)
    else:
        os.mkdir(output_folder_path)

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
        print(len(list_of_urls))

        # Go through and clean each URL before scraping the song (Takes a while)
        for x in list_of_urls[0:song_per_page_limit]:
            clean_url_link = x[0][1:-1]
            clean_urls.append(clean_url_link) 

            song_name = clean_url_link.split("/")[-1]
            song_file = requests.get(clean_url_link)

            with open(output_path + genre + '/' + 'Song' + str(song_id) + '_' + song_name, 'wb') as f:
                f.write(song_file.content)

            # Iterate song ids
            song_id +=  1

            # Print to keep track of progress
            if song_id % 2 == 0:
                print(f'Scraped: {song_id} songs')

    # Add URLS to dictionary for later use if needed
    song_ref_dict[genre] = clean_urls

# Write out the file dictionary as a JSON
song_id_json = json.dumps(song_ref_dict)
f = open("songs/song_id_dict.json","w")
f.write(song_id_json)
f.close()
    