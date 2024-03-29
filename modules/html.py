import logging
import modules.runtime
import modules.shield
import random
import classes.activity


def generate_table_header_row(hour_start=8, hours=4):
    # Creates the first (header) row of the table
    str_start = '<tr>\n<th>&nbsp;</th>\n'
    str_end = '</tr>\n'

    str_td = ''
    for hour_start in range(hour_start, hour_start + hours):
        str_td += '<th>' + str(
            12 if hour_start == 12 else hour_start % 12) + '</th><th>&nbsp;</th><th>&nbsp;</th><th>&nbsp;</th>\n'

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


def generate_table_row(content, colspan=1):
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
    navbar_html += '<img src="../images/logo_text.png" alt="Navbar Icon" class="navbar-icon">\n'
    navbar_html += '</div>\n'

    return html_start + navbar_html


def generate_html_end():
    # Creates the last part of the HTML code
    return '</body>\n</html>'


def generate_table_start():
    return '<p>\n<table>\n'


def generate_table_end():
    return '</table>\n</p>\n\n'


def generate_table_genre_row(activity_list, genre, hours, random_start=True):
    # With each genre_list (lists of shows that have been found to have a matching genre), we can now generate the HTML
    # to put in our table(s). This loops through the genre_list and creates a <tr> for each up to the number of hours specified.
    str = '<tr><td class="genre">' + genre + '</td>\n'

    if random_start:
        i = random_start_time()
        logging.debug(f'{i=}')
        if i > 0:
            str += generate_table_row('', i)
    else:
        logging.debug('No random start')
        i = 0

    time_countdown = hours * 4
    logging.debug(f'{time_countdown=}')
    for i in range(len(activity_list)):
        this_item = activity_list[i]
        this_shield = modules.shield.generate_shield_text(this_item)

        # if this_item[1] != '':
        #     this_ep = this_item[1] + ' : ' + this_item[3]
        # else:
        #     this_ep = ''

        # this_runtime = modules.runtime.runtime_to_minutes(this_item[5])
        this_runtime = classes.activity.Activity.round_to_next_quarter_hr(this_item.duration)
        this_colspan = this_runtime // 15
        logging.debug(f'{this_runtime=} {this_colspan=}')

        col_left = time_countdown - this_colspan
        logging.debug(f'{col_left=}')
        if col_left <= 0:
            this_colspan = time_countdown
            break
        else:
            time_countdown = col_left

        this_content = this_shield  # + '<br>' + this_ep
        str += generate_table_row(this_content, this_colspan)
    return str + '</tr>\n'


def generate_featured_film_table(show):
    # Create the HTML code string for the featured film

    this_show_url = show.source_url
    try:
        # Get year, media type, age rating, and synopsis quickly from ld-json data
        logging.debug('Trying to read ld_json metadata')
        show_ld_json_data = modules.ld_json.get_ld_json(this_show_url)
        image_url = show_ld_json_data['image']
    except Exception as e:
        print('Error getting data for ' + this_show_url + '. Skipping...')
        logging.error(f'{this_show_url=}')

    str_start = '<p>\n<table width="800px">\n<tr><th colspan="3">Featured Film</th></tr>\n'
    content = '<tr><td rowspan="3"><img class="featured_film" src="' + image_url + '"></img></td>\n'  # image
    content += '<td>' + modules.shield.generate_shield_text(show) + '</td>'
    content += '<td rowspan="3">' + show.description + '</td></tr>\n'  # synopsis
    content += '<tr><td>' + show.get_category_str() + '</td></tr>\n'  # genre
    duration_hr_min = classes.activity.Activity.minutes_to_hour_and_minute(show.duration)
    content += '<tr><td>' + str(duration_hr_min[0]) + 'hr ' + str(
        duration_hr_min[1]) + 'min' + '</td></tr>\n'  # runtime
    str_end = '</table>\n</p>\n'

    return str_start + content + str_end


def random_start_time():
    # Generate weighted (logrithmic) random numbers
    # This is used in the random-width blank columns at the start of the table:
    # most shows start right away, some start 15 minutes later, a few start at the half hour,
    # and they may occasionally begin after 45 minutes.
    num = random.randint(1, 100)
    if num < 53:  # 53%
        out = 0
    elif num < (53 + 27):  # next 27%
        out = 1
    elif num < (53 + 27 + 13):  # next 13%
        out = 2
    else:  # last 7%
        out = 3
    return out
