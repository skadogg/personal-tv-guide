def generate_shield(list):
    # --nord3: #4c566a;
    color_base = '4c566a'
    
    # --nord11: #bf616a;
    color_red = 'bf616a'
    
    # --nord14: #a3be8c;
    color_green = 'a3be8c'
    
    # --nord10: #5e81ac;
    color_blue = '5e81ac'
    
    # --nord15: #b48ead;
    color_other = 'b48ead'
    
    # ('One Day at a Time', 'S2 E2', '+11', 'Schooled', 'Comedy, Drama', '28min', 'TV-PG', '/us/tv-show/one-day-at-a-time-2016', '2017', 'TVSeries', 'In a reimagining of the TV classic, a newly single....')
    show = list[0].replace('-','--').replace('?','')
    
    rating = list[6] if list[6] else ' '
    if rating in ['TV-Y7','TV-G','TV-PG','PG','G']:
        rating_color = color_green
    elif rating in ['TV-14','PG-13']:
        rating_color = color_blue
    elif rating in ['TV-MA','R','NC-17','X']:
        rating_color = color_red
    else:
        rating_color = color_other
    rating = rating.replace('-','--')
    
    return '<a href="https://www.justwatch.com' + list[7] + '"><img src="https://img.shields.io/badge/' + show + ' - ' + rating + '-' + rating_color + '?labelColor=' + color_base + '"></a>'
