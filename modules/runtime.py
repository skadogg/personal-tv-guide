def runtime_to_minutes(runtime_str, round_up = True):
    # Parses the JustWatch runtime_str into minutes
    # Input format: runtime_str = '2h 28min'
    # If round_up, rounds up to the next 15 minute increment
    
    if 'h' in runtime_str:
        # split into hours/minutes
        runtime_split = runtime_str.split("h")
        runtime_minutes = (int(runtime_split[0]) * 60) + int(runtime_split[1].split("min")[0])
    else:
        runtime_minutes = int(runtime_str.split("min")[0])
    
    if round_up:
        return runtime_minutes + 15 - (runtime_minutes % 15)
    else:
        return runtime_minutes


def time_left_in_tv_series(season_data, runtime_min, curr_season = 1, next_episode = 1):
    season_lookup = {}
    for i in range(len(season_data)):
        seasonNumber = season_data[i]['seasonNumber']
        numberOfEpisodes = season_data[i]['numberOfEpisodes']
        season_lookup[seasonNumber] = numberOfEpisodes
    
    last_season_number = max(season_lookup)
    episodes_left = 0
    for j in range(curr_season, last_season_number+1):
        if curr_season == j:
            episodes_left_in_season = season_lookup[j] - next_episode + 1
            episodes_left += episodes_left_in_season
        else:
            episodes_left += season_lookup[j]

    minutes_left_in_series = episodes_left * runtime_min
    return minutes_left_in_series


def percent_complete(amt_done, amt_total):
    # minutes_left = modules.runtime.time_left_in_tv_series(season_data,50,3,21)
    # minutes_total = modules.runtime.time_left_in_tv_series(season_data,50)
    # pct_done = modules.runtime.percent_complete(minutes_left, minutes_total)
    return (amt_total - amt_done) / amt_total