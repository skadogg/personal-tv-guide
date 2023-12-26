import json

import requests
from bs4 import BeautifulSoup

url = 'https://www.justwatch.com/us/tv-show/battlestar-galactica'

def get_ld_json(url: str) -> dict:
    parser = "html.parser"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, parser)
    return json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))

data = get_ld_json(url)

# ('Making It', 'S3 E1', '+7', 'One In a Million', 'Reality TV, Comedy', '44min', 'TV-PG')


name = data['name']
year = data['dateCreated'].split('-')[0]
media_type = data['@type']
age_rating = data['contentRating']
synopsis = data['description']
main_link = data['@id']
season_data = data['containsSeason']


print(json.dumps(data, indent=2))

# p = str(soup.find('script', {'type':'application/ld+json'}))



def time_to_finish_show(season_data, curr_season = 4, next_episode = 19, runtime_min = 50):
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

    return float((episodes_left * runtime_min) / 60)

time_to_finish_show(season_data,2,1,50)

# max(season_lookup)[0]

