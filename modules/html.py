import modules.shield
import modules.runtime


def generate_table_th(hour_start = 8, hours = 4):
    str_start = '<tr>\n<th>&nbsp;</th>\n'
    str_end = '</tr>\n'
    
    str_td = ''
    for hour_start in range(hour_start, hour_start + hours):
        str_td += '<th>' + str(hour_start % 12) + '</th><th>&nbsp;</th><th>&nbsp;</th><th>&nbsp;</th>\n'
    
    return str_start + str_td + str_end


def generate_table_td(content, colspan = 1):
    str_start = '<td colspan="' + str(colspan) + '">'
    str_end = '</td>\n'
    
    # <td colspan="6"><img alt="Static Badge" src="https://img.shields.io/badge/Herbie%20Hancock%3A%20Possibilities%20(2006)%20-%20PG-green"></td>

    return str_start + content + str_end


def generate_html_start():
    stylesheet_path = "C:\\Users\\gunner\\Documents\\git\\personal-tv-guide\\css\\nord.css"
    return '<head>\n<title>Personal TV Guide</title>\n<link rel="stylesheet" href="' + stylesheet_path + '">\n</head>\n<body>\n<table>\n'


def generate_html_end():
    return '</table>\n</body>\n'


def generate_html_genre_tds(genre_list, genre, hours):
    # ('Making It', 'S3 E1', '+7', 'One In a Million', 'Reality TV, Comedy', '44min', 'TV-PG')
    str = '<tr><td class="genre">' + genre + '</td>\n'
    i = 0
    time_countdown = hours * 4
    for i in range(len(genre_list)):
        this_item = genre_list[i]
        this_shield = modules.shield.generate_shield(this_item)
        
        this_ep = this_item[1] + ' : ' + this_item[3]
        
        this_runtime = modules.runtime.runtime_to_minutes(this_item[5])
        this_colspan = this_runtime // 15
        
        col_left = time_countdown - this_colspan
        if col_left < 0:
            this_colspan = time_countdown
            break
        else:
            time_countdown = col_left
        
        this_content = this_shield + '<br>' + this_ep
        str += generate_table_td(this_content, this_colspan)
    return '<tr>\n' + str