import random

import modules.shield
import modules.html
import modules.runtime
import modules.genre


# Restore my work
import modules.data_bin_convert
# modules.data_bin_convert.data_to_bin(data_tuples)
data_tuples = modules.data_bin_convert.bin_to_data()


# Randomize the list
random.shuffle(data_tuples)


genre_reality, remainder = modules.genre.split_by_genre(data_tuples,"Reality TV")
genre_documentary, remainder = modules.genre.split_by_genre(remainder,"Documentary")
genre_romance, remainder = modules.genre.split_by_genre(remainder,"Romance")
genre_family, remainder = modules.genre.split_by_genre(remainder,"Kids & Family")
genre_comedy, remainder = modules.genre.split_by_genre(remainder,"Comedy")
genre_drama, remainder = modules.genre.split_by_genre(remainder,"Drama")



when_to_start = 11
hours_to_print = 4

html_handle = open("C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\out.html",'+w')
html_handle.write(modules.html.generate_html_start())
html_handle.write(modules.html.generate_table_th(when_to_start,hours_to_print))



# genre_list = genre_reality
# genre_list = [('Making It', 'S3 E1', '+7', 'One In a Million', 'Reality TV, Comedy', '44min', 'TV-PG'),('Making It2', 'S3 E1', '+7', 'One In a Million', 'Reality TV, Comedy', '144min', 'TV-PG'),('Making It3', 'S3 E1', '+7', 'One In a Million', 'Reality TV, Comedy', '1244min', 'TV-PG')]

# genre = 'Reality TV'
# hours = 4

html_handle.write(modules.html.generate_html_genre_tds(genre_reality,'Reality TV',hours_to_print))
html_handle.write(modules.html.generate_html_genre_tds(genre_documentary, 'Documentary', hours_to_print))
html_handle.write(modules.html.generate_html_genre_tds(genre_romance, 'Romance', hours_to_print))
html_handle.write(modules.html.generate_html_genre_tds(genre_family, 'Kids & Family', hours_to_print))
html_handle.write(modules.html.generate_html_genre_tds(genre_comedy, 'Comedy', hours_to_print))
html_handle.write(modules.html.generate_html_genre_tds(genre_drama, 'Drama', hours_to_print))

html_handle.write(modules.html.generate_html_end())

html_handle.close()
