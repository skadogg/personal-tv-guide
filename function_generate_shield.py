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
    
    i = 0
    for i in range(len(list)):
        # ('Making It', 'S3 E1', '+7', 'One In a Million', 'Reality TV, Comedy', '44min', 'TV-PG')
        show = list[i][0].replace('-','--').replace('?','')
        
        rating = list[i][6] if list[i][6] else ' '
        if rating in ['TV-Y7','TV-G','TV-PG']:
            rating_color = color_green
        elif rating in ['TV-14','PG-13']:
            rating_color = color_blue
        elif rating in ['TV-MA','R','NC-17','X']:
            rating_color = color_red
        else:
            rating_color = color_other
        rating = rating.replace('-','--')
        
        # ep = list[i][1]
        # ep_title = list[i][3]
            
        # print('<img src="https://img.shields.io/badge/' + show + ' - ' + rating + '-' + rating_color + '"><br>' + ep + ' ' + ep_title + '<br>')
        print('<img src="https://img.shields.io/badge/' + show + ' - ' + rating + '-' + rating_color + '?labelColor=' + color_base + '">')
