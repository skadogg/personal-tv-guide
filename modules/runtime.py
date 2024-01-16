import logging
import modules.shield

def runtime_to_minutes(runtime_str, round_up = True):
    # Parses the JustWatch runtime_str into minutes
    # Input format: runtime_str = '2h 28min'
    # If round_up, rounds up to the next 15 minute increment
    logging.debug('Converting runtime:')
    logging.debug(f'{runtime_str=}')
    if 'h' in runtime_str:
        # split into hours/minutes
        runtime_split = runtime_str.split("h")
        runtime_minutes = (int(runtime_split[0]) * 60) + int(runtime_split[1].split("min")[0])
    else:
        runtime_minutes = int(runtime_str.split("min")[0])
    logging.debug(f'{str(runtime_minutes)=}')
    
    if round_up:
        logging.debug('Rounding:')
        runtime_rounded_up = runtime_minutes + 15 - (runtime_minutes % 15)
        logging.debug(f'{str(runtime_rounded_up)=}')
        return runtime_rounded_up
    else:
        return runtime_minutes


def time_left_in_tv_series(season_data, runtime_min, curr_season = 1, next_episode = 1):
    logging.debug('Calculating time left in tv series')
    season_lookup = {}
    for i in range(len(season_data)):
        seasonNumber = season_data[i]['seasonNumber']
        numberOfEpisodes = season_data[i]['numberOfEpisodes']
        season_lookup[seasonNumber] = numberOfEpisodes
    
    last_season_number = max(season_lookup)
    logging.debug(f'{str(last_season_number)=}')
    episodes_left = 0
    for j in range(curr_season, last_season_number+1):
        logging.debug('season:')
        logging.debug(f'{str(j)=}')
        if curr_season == j:
            episodes_left_in_season = season_lookup[j] - next_episode + 1
            episodes_left += episodes_left_in_season
        else:
            episodes_left += season_lookup[j]

    minutes_left_in_series = episodes_left * runtime_min
    return minutes_left_in_series


def percent_complete(minutes_left, minutes_total):
    # Example:
    #     minutes_left = modules.runtime.time_left_in_tv_series(season_data,50,3,21)
    #     minutes_total = modules.runtime.time_left_in_tv_series(season_data,50)
    #     pct_done = modules.runtime.percent_complete(minutes_left, minutes_total)
    return (minutes_total - minutes_left) / minutes_total


def time_left_in_tv_series_report(list):
    time_info = []
    for i in range(len(list)):
        show_title = modules.shield.generate_shield(list[i])
        current_season, current_episode = list[i][1].replace('S','').replace('E','').split(' ')
        season_data = list[i][11]
        runtime = runtime_to_minutes(list[i][5],False)
        # episodes_left
        
        minutes_left = time_left_in_tv_series(season_data,runtime,int(current_season),int(current_episode))
        minutes_total = time_left_in_tv_series(season_data,runtime)
        pct_done = percent_complete(minutes_left, minutes_total)
        
        time_info.append([show_title,minutes_left,minutes_total,pct_done])
    
    time_info_sorted = sorted(time_info, key=lambda x:(x[1], x[0]))
    return time_info_sorted
