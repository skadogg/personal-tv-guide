def split_by_genre(list,genre_str):
    list_with_genre, list_without_genre = [], []
    for i in range(len(list)):
        genres = list[i][4]
        if genre_str in genres:
            list_with_genre.append(list[i])
        else:
            list_without_genre.append(list[i])
    return [list_with_genre,list_without_genre]


def get_genres_from_scraped_lists():
    # Restore my work
    import modules.data_bin_convert
    # modules.data_bin_convert.data_to_bin(data_tuples)
    data_tuples_movies = modules.data_bin_convert.bin_to_data('C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\saved_data_movies.bin')
    data_tuples_tv = modules.data_bin_convert.bin_to_data('C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\saved_data_tv.bin')

    data_tuples = data_tuples_movies + data_tuples_tv

    genre_str = ''
    for i in range(len(data_tuples)):
        genre_str += data_tuples[i][4] + ', '

    genre_list = sorted(list(set((genre_str.split(', ')))))

    while '' in genre_list:
        genre_list.remove('')

    modules.data_bin_convert.data_to_bin(genre_list, 'C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\saved_data_genres.bin')


    # full_genre_list = sorted(genre_str.split(', '))
    # count = 0
    # for j in (range(len(full_genre_list) - 1)):
    #     if full_genre_list[j+1] == full_genre_list[j]:
    #         count += 1
    #     else:
    #         print(full_genre_list[j] + str(count))
    #         count = 0


def christmas_keywords():
    list = ['Christmas','Holida','Hanukkah','Santa','Claus','Noel','Klaus','Merry','Fitzwilly','Preacher\'s Wife','Every Time a Bell Rings','Family Stone','Haul Out the Holly','Elf','Let It Snow','Scrooge','Baby, It\'s Cold','Winter Love Story','Mingle All the Way','Snow','Shop Around the Corner','Spirited','Home Alone','Five More Minutes','Fallen Angel','Family Man','New Year\'s','Tis the Season','Pottersville','Godmothered','Polar Express']
    return list


# TRIGGER WARNING
def trigger_keywords():
    list = ['widow','liver','aneurysm','assault','abuse','cruel','suicide','kidnap','abduct','miscarriage','abortion','torture']
    return list


def split_by_keyword(list,keyword_list):
    list_with_keywords, list_without_keywords = [], []
    for i in range(len(list)):
        title = list[i][0]
        
        for j in range(len(keyword_list)):
            if keyword_list[j] in title:
                found = True
                break
            else:
                found = False
        
        if found:
            list_with_keywords.append(list[i])
        else:
            list_without_keywords.append(list[i])
    return [list_with_keywords,list_without_keywords]
