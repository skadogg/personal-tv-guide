from dotenv import load_dotenv
import logging
import modules.data_bin_convert
import os


def split_by_genre(list,genre_str):
    # Takes the list and splits into two lists: one with the given genre_str, and one without
    # >>> genre_romance, remainder = modules.genre.split_by_genre(data_list_everything,"Romance")
    logging.debug(f'{genre_str=}')
    list_with_genre, list_without_genre = [], []
    for i in range(len(list)):
        genres = list[i][4]
        if genre_str in genres:
            logging.debug('Match:')
            logging.debug(f'{str(list[i][0:4])=}')
            list_with_genre.append(list[i])
        else:
            logging.debug(f'Skip:')
            logging.debug(f'{list[i][4]=}')
            list_without_genre.append(list[i])
    return [list_with_genre,list_without_genre]


def get_genres_from_scraped_lists():
    # Read through the data and find all genres that exist there.
    # Data gets stored in .bin file``
    data_list_movies = modules.data_bin_convert.bin_to_data('./my_data/saved_data_movies.bin')
    data_list_tv = modules.data_bin_convert.bin_to_data('./my_data/saved_data_tv.bin')

    data_list_everything = data_list_movies + data_list_tv

    genre_str = ''
    for i in range(len(data_list_everything)):
        genre_str += data_list_everything[i][4] + ', '

    genre_list = sorted(list(set((genre_str.split(', ')))))

    while '' in genre_list:
        genre_list.remove('')
    
    logging.debug(genre_list)

    modules.data_bin_convert.data_to_bin(genre_list, './my_data/saved_data_genres.bin')


def christmas_keywords():
    # A list of Christmas keywords, used to make a custom row
    load_dotenv(dotenv_path='./my_data/.env')
    return os.environ.get('CHRISTMAS_KEYWORDS').split(',')


def trigger_keywords():
    # A list of keywords that some may find disturbing, used to make a custom row.
    # Example: My wife and I watch Hallmark movies, but they often center around a widow looking for a new love.
    #   Stories about widows make her sad, so I can watch these on my own if I want.
    load_dotenv(dotenv_path='./my_data/.env')
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
            logging.debug(word)
            if word in title or word in synopsis:
                logging.debug(title)
                logging.debug(synopsis)
                found = True
                break
            else:
                found = False

        if found:
            list_with_keywords.append(list[i])
        else:
            list_without_keywords.append(list[i])
        
        logging.debug(f'{str(len(list_with_keywords))=}')
        logging.debug(f'{str(len(list_without_keywords))=}')
    return [list_with_keywords,list_without_keywords]
