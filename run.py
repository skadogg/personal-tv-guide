from dotenv import load_dotenv
import modules.genre
import modules.html
import modules.justwatch
import modules.runtime
import modules.shield
import os
import random


# Variables
load_dotenv(dotenv_path='./my_data/.env')
when_to_start = int(os.environ.get('WHEN_TO_START')) # first hour in output table
hours_to_print = int(os.environ.get('HOURS_TO_PRINT')) # how many hours worth of data in table
outfile = str(os.environ.get('OUTFILE'))
stylesheet_path = str(os.environ.get('STYLESHEET_PATH'))
use_keyword_lists = os.environ.get('USE_KEYWORD_LIST').lower() == 'true'


modules.justwatch.scrape_justwatch('Movies')
modules.justwatch.scrape_justwatch('TV')


# Create genres bin file
modules.genre.get_genres_from_scraped_lists()


# Restore my work
import modules.data_bin_convert
# TODO: rename this tuples stuff
# modules.data_bin_convert.data_to_bin(data_tuples)
data_tuples_movies = modules.data_bin_convert.bin_to_data('./my_data/saved_data_movies.bin')
data_tuples_tv = modules.data_bin_convert.bin_to_data('./my_data/saved_data_tv.bin')
all_genres = modules.data_bin_convert.bin_to_data('./my_data/saved_data_genres.bin')

data_tuples = modules.justwatch.balance_movie_and_tv_lists(data_tuples_movies, data_tuples_tv, 0.7)


# Randomize the lists
random.shuffle(data_tuples)
random.shuffle(all_genres)


# Look through data for keyword matches
# use_keyword_lists = True
# TODO: only do these if use_keyword_lists is True. Otherwise, this serves to exclude shows by keyword.
genre_triggers, remainder = modules.genre.split_by_keyword(data_tuples,modules.genre.trigger_keywords())
genre_christmas, remainder = modules.genre.split_by_keyword(remainder,modules.genre.christmas_keywords())


# Loop through all_genres to separate data by genre
i = 0
genre_lists = []
if not use_keyword_lists:
    remainder = data_tuples
while len(remainder) > 0:
    list_with_genre, remainder = modules.genre.split_by_genre(remainder, all_genres[i])
    genre_lists.append(list_with_genre)
    i += 1


# Begin writing data
html_handle = open(outfile,'+w')
html_handle.write(modules.html.generate_html_start(stylesheet_path))


# TV Guide
html_handle.write(modules.html.generate_table_start())
html_handle.write(modules.html.generate_table_th(when_to_start,hours_to_print))

# Write table rows for keyword lists
if use_keyword_lists:
    html_handle.write(modules.html.generate_html_genre_tds(genre_triggers,'Trigger Warning',hours_to_print))
    html_handle.write(modules.html.generate_html_genre_tds(genre_christmas,'Christmas',hours_to_print))
    
# Write table rows for looped genre_lists, sorted alphabetically
genre_lists_str = []
i = 0
for i in range(len(genre_lists)):
    if genre_lists[i]:
        genre_lists_str.append(str(modules.html.generate_html_genre_tds(genre_lists[i], all_genres[i], hours_to_print)))

genre_lists_str_sorted = sorted(genre_lists_str)

i = 0
for i in range(len(genre_lists_str_sorted)):
    html_handle.write(genre_lists_str_sorted[i])

html_handle.write(modules.html.generate_table_end())


# Featured Film
html_handle.write(modules.html.generate_featured_film_table(modules.justwatch.get_random_show(data_tuples_movies)))


# Movies sorted by runtime
html_handle.write(modules.justwatch.generate_movies_by_runtime_table(data_tuples_movies))


# Finish writing data
html_handle.write(modules.html.generate_html_end())
html_handle.close()
