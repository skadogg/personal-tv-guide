import random

import modules.shield
import modules.html
import modules.runtime
import modules.genre


# Variables
when_to_start = 8 # first hour in output table
hours_to_print = 4 # how many hours worth of data in table
outfile = "C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\out.html"


# Restore my work
import modules.data_bin_convert
# modules.data_bin_convert.data_to_bin(data_tuples)
data_tuples_movies = modules.data_bin_convert.bin_to_data('C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\saved_data_movies.bin')
data_tuples_tv = modules.data_bin_convert.bin_to_data('C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\saved_data_tv.bin')
all_genres = modules.data_bin_convert.bin_to_data('C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\saved_data_genres.bin')

data_tuples = data_tuples_movies + data_tuples_tv


# Randomize the lists
random.shuffle(data_tuples)
random.shuffle(all_genres)


# Look through data for keyword matches
use_keyword_lists = True
genre_christmas, remainder = modules.genre.split_by_keyword(data_tuples,modules.genre.christmas_keywords())


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
html_handle.write(modules.html.generate_html_start())
html_handle.write(modules.html.generate_table_th(when_to_start,hours_to_print))


# Write table rows for keyword lists
if use_keyword_lists:
    html_handle.write(modules.html.generate_html_genre_tds(genre_christmas,'Christmas',hours_to_print))


# Write table rows for looped genre_lists
for i in range(len(genre_lists)):
    if genre_lists[i]:
        html_handle.write(modules.html.generate_html_genre_tds(genre_lists[i], all_genres[i], hours_to_print))


# Finish writing data
html_handle.write(modules.html.generate_html_end())
html_handle.close()
