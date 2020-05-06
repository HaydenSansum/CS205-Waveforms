from scraper import scrape_fma

# Set up parameters
output_path = '../../songs/mp3/'
genres = ['Jazz']
page_nums = list(range(1,3))
song_per_page_limit = 2
overwrite_files = True

scrape_fma(output_path, genres, page_nums, song_per_page_limit, overwrite_files)
