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
