from dotenv import load_dotenv
import modules.data_bin_convert
import modules.genre
import modules.html
import modules.justwatch
import modules.runtime
import modules.shield
import os
import random


# Get user variables from .env
load_dotenv(dotenv_path='./my_data/.env')
when_to_start = int(os.environ.get('WHEN_TO_START'))
hours_to_print = int(os.environ.get('HOURS_TO_PRINT'))
outfile = str(os.environ.get('OUTFILE'))
stylesheet_path = str(os.environ.get('STYLESHEET_PATH'))
use_keyword_lists = os.environ.get('USE_KEYWORD_LIST').lower() == 'true'


# Scrape your data from JustWatch and stor in .bin files for later
# These can take a while, so it can sometimes be useful to store your data, especially while developing
modules.justwatch.scrape_justwatch('Movies')
modules.justwatch.scrape_justwatch('TV')


# Read all genres from scraped data and store in .bin file for later
modules.genre.get_genres_from_scraped_lists()


# Restore scraped data from stored .bin files and combine into a full list of all shows
data_list_movies = modules.data_bin_convert.bin_to_data('./my_data/saved_data_movies.bin')
data_list_tv = modules.data_bin_convert.bin_to_data('./my_data/saved_data_tv.bin')
data_list_everything = modules.justwatch.balance_movie_and_tv_lists(data_list_movies, data_list_tv, 0.7)


# Restore genres from stored .bin file
all_genres = modules.data_bin_convert.bin_to_data('./my_data/saved_data_genres.bin')


# Randomize the lists so you don't just end up with super-popular Action/Adventure movies
# (The output gets sorted later. All is well.)
random.shuffle(data_list_everything)
random.shuffle(all_genres)


# Look through data for keyword matches
# This can be used for special lists (e.g. movies you only watch during the holidays),
# or for things you might want to filter out (e.g. trigger warnings)
if use_keyword_lists:
    genre_triggers, remainder = modules.genre.split_by_keyword(data_list_everything,modules.genre.trigger_keywords())
    genre_christmas, remainder = modules.genre.split_by_keyword(remainder,modules.genre.christmas_keywords())
else:
    remainder = data_list_everything


# Loop through all_genres to separate data by genre
# Starts with data left over after pulling out keywords (if this is used), and splits into
# genre groupings. remainder gets smaller each pass until it eventually empties out.
i = 0
genre_lists = []
while len(remainder) > 0:
    list_with_genre, remainder = modules.genre.split_by_genre(remainder, all_genres[i])
    genre_lists.append(list_with_genre)
    i += 1


# Begin writing HTML output
html_handle = open(outfile,'+w')
html_handle.write(modules.html.generate_html_start(stylesheet_path))


# Begin writing the main table for your personal TV guide
html_handle.write(modules.html.generate_table_start())
html_handle.write(modules.html.generate_table_header_row(when_to_start,hours_to_print))

# Write table rows for keyword lists (if using)
if use_keyword_lists:
    html_handle.write(modules.html.generate_table_genre_row(genre_triggers,'Trigger Warning',hours_to_print))
    html_handle.write(modules.html.generate_table_genre_row(genre_christmas,'Christmas',hours_to_print))
    
# Write table rows for previously-separated genre lists, sorted alphabetically
genre_lists_str = []
i = 0
for i in range(len(genre_lists)):
    if genre_lists[i]:
        genre_lists_str.append(str(modules.html.generate_table_genre_row(genre_lists[i], all_genres[i], hours_to_print)))

genre_lists_str_sorted = sorted(genre_lists_str)

i = 0
for i in range(len(genre_lists_str_sorted)):
    html_handle.write(genre_lists_str_sorted[i])

html_handle.write(modules.html.generate_table_end())
# End of writing the main table for your personal TV guide


# Featured Film
html_handle.write(modules.html.generate_featured_film_table(modules.justwatch.get_random_show(data_list_movies)))


# Movies sorted by runtime
html_handle.write(modules.justwatch.generate_movies_by_runtime_table(data_list_movies))


# Finish writing HTML output
html_handle.write(modules.html.generate_html_end())
html_handle.close()
