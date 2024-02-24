from dotenv import load_dotenv
import logging
import modules.data_bin_convert
import modules.genre
import modules.html
import modules.justwatch
import modules.runtime
import os
import random

# Get user variables from .env
load_dotenv(dotenv_path='./.env')
when_to_start = int(os.environ.get('WHEN_TO_START'))
hours_to_print = int(os.environ.get('HOURS_TO_PRINT'))
outfile = str(os.environ.get('OUTFILE'))
stylesheet_path = str(os.environ.get('STYLESHEET_PATH'))
use_keyword_lists = os.environ.get('USE_KEYWORD_LIST').lower() == 'true'
dev_mode = os.environ.get('DEV_MODE').lower() == 'true'

# Logging
if dev_mode:
    logging.basicConfig(filename='./my_data/run.log', encoding='utf-8', level=logging.DEBUG, filemode='w',
                        format="%(asctime)s %(levelname)s %(message)s")
else:
    logging.basicConfig(filename='./my_data/run.log', encoding='utf-8', level=logging.INFO, filemode='w',
                        format="%(asctime)s %(levelname)s %(message)s")

# Scrape your data from JustWatch and stor in .bin files for later
# These can take a while, so it can sometimes be useful to store your data, especially while developing
logging.info('Scraping data from JustWatch')

# TV in progress
modules.justwatch.scrape_justwatch('https://www.justwatch.com/us/lists/tv-show-tracking?inner_tab=continue_watching')
# TV not started
modules.justwatch.scrape_justwatch('https://www.justwatch.com/us/lists/tv-show-tracking?inner_tab=havent_started')
# Movies
modules.justwatch.scrape_justwatch('https://www.justwatch.com/us/lists/my-lists?content_type=movie&sort_by=popular_30_day')

# Read all genres from scraped data and store in .bin file for later
logging.info('Reading genres from scraped data')
modules.genre.get_genres_from_scraped_lists()

# Restore scraped data from stored .bin files and combine into a full list of all shows
# data_list_movies = modules.data_bin_convert.bin_to_data('./my_data/saved_data_movies.bin')
# data_list_tv = modules.data_bin_convert.bin_to_data('./my_data/saved_data_tv.bin')
# balance_factor = 4  # TODO base this on how many hours in final report (with some comments)
# logging.info('Combining movie and tv data into balanced list')
# logging.info(f'{balance_factor=}')
# data_list_everything = modules.justwatch.balance_movie_and_tv_lists(data_list_movies, data_list_tv, balance_factor)
data_list_everything = modules.data_bin_convert.bin_to_data('./my_data/saved_data.bin')

# Restore genres from stored .bin file
all_genres = modules.data_bin_convert.bin_to_data('./my_data/saved_data_genres.bin')

# Randomize the list
logging.info('Shuffling data')
random.shuffle(data_list_everything)

# Sort by genre frequency so you don't just end up with super-popular Action/Adventure movies
all_genres = sorted(all_genres, key = all_genres.count, reverse = False)

# Look through data for keyword matches
# This can be used for special lists (e.g. movies you only watch during the holidays),
# or for things you might want to filter out (e.g. trigger warnings)
logging.info('Splitting by keyword')
if use_keyword_lists:
    logging.debug('triggers')
    genre_triggers, remainder = modules.genre.split_by_keyword(data_list_everything, modules.genre.trigger_keywords())
    logging.debug('Christmas')
    genre_christmas, remainder = modules.genre.split_by_keyword(remainder, modules.genre.christmas_keywords())
else:
    remainder = data_list_everything

# Loop through all_genres to separate data by genre
# Starts with data left over after pulling out keywords (if this is used), and splits into
# genre groupings. remainder gets smaller each pass until it eventually empties out.
logging.info('Splitting by standard genre')
i = 0
genre_lists = []
while len(remainder) > 0:
    list_with_genre, remainder = modules.genre.split_by_genre(remainder, all_genres[i])
    genre_lists.append(list_with_genre)
    i += 1

# Begin writing HTML output
logging.info('Writing HTML output')
logging.info('-------------------')
html_handle = open(outfile, '+w', encoding="utf-8")
html_handle.write(modules.html.generate_html_start(stylesheet_path))

# Begin writing the main table for your personal TV guide
logging.info('Writing main table start')
html_handle.write(modules.html.generate_table_start())
html_handle.write(modules.html.generate_table_header_row(when_to_start, hours_to_print))

# Write table rows for keyword lists (if using)
logging.info('Writing keyword rows')
if use_keyword_lists:
    html_handle.write(modules.html.generate_table_genre_row(genre_triggers, 'Trigger Warning', hours_to_print))
    html_handle.write(modules.html.generate_table_genre_row(genre_christmas, 'Christmas', hours_to_print))

# Write table rows for previously-separated genre lists, sorted alphabetically
logging.info('Generating table HTML for standard genre rows')
genre_lists_str = []
i = 0
for i in range(len(genre_lists)):
    logging.debug(all_genres[i])
    if genre_lists[i]:
        genre_lists_str.append(
            str(modules.html.generate_table_genre_row(genre_lists[i], all_genres[i], hours_to_print)))

logging.info('Sorting rows')
genre_lists_str_sorted = sorted(genre_lists_str)

logging.info('Writing standard genre rows')
i = 0
for i in range(len(genre_lists_str_sorted)):
    html_handle.write(genre_lists_str_sorted[i])

html_handle.write(modules.html.generate_table_end())
# End of writing the main table for your personal TV guide


# Featured Film
logging.info('Writing Featured Film table')
html_handle.write(modules.html.generate_featured_film_table(modules.justwatch.get_random_show(data_list_everything)))

# Write table for time left in TV series
logging.info('Writing time left in TV series table')
time_info = modules.runtime.time_left_in_tv_series_report(data_list_everything)
html_handle.write('<p>\n<table>\n<th>Title</th><th>Minutes Left</th>\n')
for i in range(len(time_info)):
    # html_handle.write('<tr><td>' + time_info[i][0] + '</td><td>' + str(round(time_info[i][3] * 100,
    # 0)) + '%</td></tr>') #percent done
    html_handle.write('<tr><td>' + time_info[i][0] + '</td><td>' + str(time_info[i][1]) + '</td></tr>')  # minutes left
html_handle.write('</table>\n</p>\n')

# # # Movies sorted by runtime
logging.info('Writing Movies sorted by runtime table')
html_handle.write(modules.justwatch.generate_movies_by_runtime_table(data_list_everything))

# Finish writing HTML output
html_handle.write(modules.html.generate_html_end())
html_handle.close()
logging.info('-------------------')
