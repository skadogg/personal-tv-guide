import random

import modules.shield
import modules.html
import modules.runtime
import modules.genre


# Restore my work
import modules.data_bin_convert
# modules.data_bin_convert.data_to_bin(data_tuples)
data_tuples_movies = modules.data_bin_convert.bin_to_data('C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\saved_data_movies.bin')
data_tuples_tv = modules.data_bin_convert.bin_to_data('C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\saved_data_tv.bin')
all_genres = modules.data_bin_convert.bin_to_data('C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\saved_data_genres.bin')

data_tuples = data_tuples_movies + data_tuples_tv

# Randomize the list
random.shuffle(data_tuples)


random.shuffle(all_genres)

i = 0
genre_lists = []
remainder = data_tuples
while len(remainder) > 0:
    list_with_genre, remainder = modules.genre.split_by_genre(remainder, all_genres[i])
    genre_lists.append(list_with_genre)
    i += 1

# genre_reality, remainder = modules.genre.split_by_genre(data_tuples,"Reality TV")
# genre_documentary, remainder = modules.genre.split_by_genre(remainder,"Documentary")
# genre_romance, remainder = modules.genre.split_by_genre(remainder,"Romance")
# genre_family, remainder = modules.genre.split_by_genre(remainder,"Kids & Family")
# genre_comedy, remainder = modules.genre.split_by_genre(remainder,"Comedy")
# genre_drama, remainder = modules.genre.split_by_genre(remainder,"Drama")




when_to_start = 12
hours_to_print = 6

html_handle = open("C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\out.html",'+w')
html_handle.write(modules.html.generate_html_start())
html_handle.write(modules.html.generate_table_th(when_to_start,hours_to_print))



# genre_list = genre_reality
# genre_list = [('Making It', 'S3 E1', '+7', 'One In a Million', 'Reality TV, Comedy', '44min', 'TV-PG'),('Making It2', 'S3 E1', '+7', 'One In a Million', 'Reality TV, Comedy', '144min', 'TV-PG'),('Making It3', 'S3 E1', '+7', 'One In a Million', 'Reality TV, Comedy', '1244min', 'TV-PG')]

# genre = 'Reality TV'
# hours = 4




for i in range(len(genre_lists)):
    if genre_lists[i]:
        html_handle.write(modules.html.generate_html_genre_tds(genre_lists[i], all_genres[i], hours_to_print))


# html_handle.write(modules.html.generate_html_genre_tds(genre_reality,'Reality TV',hours_to_print))
# html_handle.write(modules.html.generate_html_genre_tds(genre_documentary, 'Documentary', hours_to_print))
# html_handle.write(modules.html.generate_html_genre_tds(genre_romance, 'Romance', hours_to_print))
# html_handle.write(modules.html.generate_html_genre_tds(genre_family, 'Kids & Family', hours_to_print))
# html_handle.write(modules.html.generate_html_genre_tds(genre_comedy, 'Comedy', hours_to_print))
# html_handle.write(modules.html.generate_html_genre_tds(genre_drama, 'Drama', hours_to_print))

html_handle.write(modules.html.generate_html_end())

html_handle.close()
