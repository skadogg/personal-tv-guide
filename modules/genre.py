import os
from dotenv import load_dotenv

load_dotenv()


def split_by_genre(list,genre_str):
    # Takes the list and splits into two lists: one with the given genre_str, and one without
    # >>> genre_romance, remainder = modules.genre.split_by_genre(data_list_everything,"Romance")
    list_with_genre, list_without_genre = [], []
    for i in range(len(list)):
        genres = list[i][4]
        if genre_str in genres:
            list_with_genre.append(list[i])
        else:
            list_without_genre.append(list[i])
    return [list_with_genre,list_without_genre]


def get_genres_from_scraped_lists():
    # This is where we get the list of genres that is used in build_html.py. It shouldn't be needed too often,
    # but this is how I pulled the list after scraping movie and tv data from JustWatch.
    # Current list:
    # ['Action & Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'History', 'Horror', 'Kids & Family', 'Made in Europe', 'Music & Musical', 'Mystery & Thriller', 'Reality TV', 'Romance', 'Science-Fiction', 'Sport', 'War & Military', 'Western']

    # Restore my work
    import modules.data_bin_convert
    # modules.data_bin_convert.data_to_bin(data_list_everything)
    data_list_movies = modules.data_bin_convert.bin_to_data('./my_data/saved_data_movies.bin')
    data_list_tv = modules.data_bin_convert.bin_to_data('./my_data/saved_data_tv.bin')

    data_list_everything = data_list_movies + data_list_tv

    genre_str = ''
    for i in range(len(data_list_everything)):
        genre_str += data_list_everything[i][4] + ', '

    genre_list = sorted(list(set((genre_str.split(', ')))))

    while '' in genre_list:
        genre_list.remove('')

    modules.data_bin_convert.data_to_bin(genre_list, './my_data/saved_data_genres.bin')


def christmas_keywords():
    # A list of Christmas keywords, used to make a custom row
    return os.environ.get('CHRISTMAS_KEYWORDS').split(',')


# TRIGGER WARNING
def trigger_keywords():
    # A list of keywords that some may find disturbing, used to make a custom row.
    # Example: My wife and I watch Hallmark movies, but they often center around a widow looking for a new love.
    #   Stories about widows make her sad, so I can watch these on my own if I want.
    return os.environ.get('TRIGGER_KEYWORDS').split(',')


def split_by_keyword(list,keyword_list):
    # Takes the list and splits into two lists: one with the given keywords, and one without
    # >>> genre_christmas, remainder = modules.genre.split_by_keyword(data_list_everything,modules.genre.christmas_keywords())
    list_with_keywords, list_without_keywords = [], []
    for i in range(len(list)):
        title = list[i][0]
        synopsis = list[i][10]

        for j in range(len(keyword_list)):
            word = keyword_list[j]
            if word in title or word in synopsis:
                found = True
                break
            else:
                found = False

        if found:
            list_with_keywords.append(list[i])
        else:
            list_without_keywords.append(list[i])
    return [list_with_keywords,list_without_keywords]
