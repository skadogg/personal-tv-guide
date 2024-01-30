def generate_shield_text(input_activity):
    # Given a show list, generates text with a link to the show and its rating
    rating = input_activity.age_rating if input_activity.age_rating else '&nbsp;'
    if rating in ['TV-Y7','TV-G','TV-PG','PG','G']:
        rating_color = 'badge_green'
    elif rating in ['TV-14','PG-13']:
        rating_color = 'badge_blue'
    elif rating in ['TV-MA','R','NC-17','X']:
        rating_color = 'badge_red'
    else:
        rating_color = 'badge_other'
    
    output_str = '<div class="badge"><a href="' + input_activity.source_url + '">'
    output_str += '<span class="badge_main">' + input_activity.activity_name + ' (' + str(input_activity.year) + ')' + '</span>'
    output_str += '<span class="' + rating_color + '">' + rating + '</span>'
    output_str += '</a></div>\n'
    
    return output_str
