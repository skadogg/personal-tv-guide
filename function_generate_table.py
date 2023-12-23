def generate_table_th(hour_start = 8, hours = 4):
    str_start = '<th>'
    str_end = '</th>'
    
    str_td = ''
    for hour_start in range(hour_start, hour_start + hours):
        str_td += '<td>' + str(hour_start) + '</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td>'
    
    return str_start + str_td + str_end


def generate_table_td(content, colspan = 1):
    str_start = '<td colspan="' + str(colspan) + '">'
    str_end = '</td>'
    
    # <td colspan="6"><img alt="Static Badge" src="https://img.shields.io/badge/Herbie%20Hancock%3A%20Possibilities%20(2006)%20-%20PG-green"></td>

    return str_start + content + str_end