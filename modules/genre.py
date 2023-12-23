def split_by_genre(list,genre_str):
    list_with_genre, list_without_genre = [], []
    for i in range(len(list)):
        genres = list[i][4]
        if genre_str in genres:
            list_with_genre.append(list[i])
        else:
            list_without_genre.append(list[i])
    return [list_with_genre,list_without_genre]