from bs4 import BeautifulSoup
import json
import requests


def get_ld_json(url: str) -> dict:
    # Takes in a URL, reads the ld+json data, and returns useable json data
    # https://stackoverflow.com/questions/43655169/how-to-parse-ldjson-using-python
    # Example: >>>data = get_ld_json('https://www.justwatch.com/us/tv-show/battlestar-galactica')
    #     name = data['name']
    #     year = data['dateCreated'].split('-')[0]
    #     media_type = data['@type']
    #     age_rating = data['contentRating']
    #     synopsis = data['description']
    #     main_link = data['@id']
    #     season_data = data['containsSeason']
    parser = "html.parser"
    req = requests.get(url)
    soup = BeautifulSoup(req.text, parser)
    return json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))
