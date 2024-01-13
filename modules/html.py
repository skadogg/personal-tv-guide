import modules.shield
import modules.runtime
import random


def generate_table_th(hour_start = 8, hours = 4):
    # Creates the first (header) row of the table
    str_start = '<tr>\n<th>&nbsp;</th>\n'
    str_end = '</tr>\n'

    str_td = ''
    for hour_start in range(hour_start, hour_start + hours):
        str_td += '<th>' + str(12 if hour_start == 12 else hour_start % 12) + '</th><th>&nbsp;</th><th>&nbsp;</th><th>&nbsp;</th>\n'

    return str_start + str_td + str_end


def sort_by_runtime_table_header(headers_list):
    # Creates the first (header) row of the table
    str_start = '<tr>\n'
    str_end = '</tr>\n'

    str_tr = ''
    for i in range(len(headers_list)):
        str_tr += '<th>' + headers_list[i] + '</th>\n'

    return str_start + str_tr + str_end


def sort_by_runtime_table_row(row_list):
    # Creates the first (header) row of the table
    str_start = '<tr>\n'
    str_end = '</tr>\n'

    str_tr = '<td>' + row_list[0] + '</td><td>' + row_list[1] + '</td>\n'

    return str_start + str_tr + str_end


def generate_table_td(content, colspan = 1):
    # Wraps your content string in a <td> spanning colspan number of columns
    # <td colspan="6"><img alt="Static Badge" src="https://img.shields.io/badge/Herbie%20Hancock%3A%20Possibilities%20(2006)%20-%20PG-green"></td>
    str_start = '<td colspan="' + str(colspan) + '">'
    str_end = '</td>\n'

    return str_start + content + str_end


def generate_html_start(stylesheet_path):
    # Creates the first part of the HTML code
    # stylesheet_path = "./css/nord.css"
    html_start = '<html><head>\n<title>Personal TV Guide</title>\n<link rel="stylesheet" href="' + stylesheet_path + '">\n</head>\n<body>\n'
    
    navbar_html = '<div class="navbar">\n'
    navbar_html += '<img src="./images/icon.png" alt="Navbar Icon" class="navbar-icon">\n'
    navbar_html += '</div>\n'
    
    return html_start + navbar_html

def generate_html_end():
    # Creates the last part of the HTML code
    return '</body>\n</html>'


def generate_table_start():
    return '<p>\n<table>\n'


def generate_table_end():
    return '</table>\n</p>\n\n'


def generate_html_genre_tds(genre_list, genre, hours, random_start = True):
    # With each genre_list (lists of shows that have been found to have a matching genre), we can now generate the HTML
    # to put in our table(s). This loops through the genre_list and creates a <tr> for each up to the number of hours specified.
    str = '<tr><td class="genre">' + genre + '</td>\n'
    
    if random_start:
        i = random_start_time()
        if i > 0:
            str += generate_table_td('', i)
    else:
        i = 0

        
    time_countdown = hours * 4
    for i in range(len(genre_list)):
        this_item = genre_list[i]
        this_shield = modules.shield.generate_shield_table(this_item)

        if this_item[1] != '':
            this_ep = this_item[1] + ' : ' + this_item[3]
        else:
            this_ep = ''

        this_runtime = modules.runtime.runtime_to_minutes(this_item[5])
        this_colspan = this_runtime // 15

        col_left = time_countdown - this_colspan
        if col_left <= 0:
            this_colspan = time_countdown
            break
        else:
            time_countdown = col_left

        this_content = this_shield # + '<br>' + this_ep
        str += generate_table_td(this_content, this_colspan)
    return str + '</tr>\n'


def generate_featured_film_table(show):
    # Create the HTML code string for the featured film
    str_start = '<p>\n<table width="800px">\n<tr><th colspan="2">Featured Film</th></tr>\n'
    content = '<tr><td>' + modules.shield.generate_shield(show) + '</td>'
    content += '<td rowspan="3">' + show[10] + '</td></tr>\n' # synopsis
    content += '<tr><td>' + show[4] + '</td></tr>\n' # genre
    content += '<tr><td>' + show[5] + '</td></tr>\n' # runtime
    str_end = '</table>\n</p>\n'
    
    return str_start + content + str_end



def random_start_time():
    num = random.randint(1,100)
    if num < 53: # 53%
        out = 0
    elif num < (53 + 27): # next 27%
        out = 1
    elif num < (53 + 27 + 13): # next 13%
        out = 2
    else: # last 7%
        out = 3
    return out
