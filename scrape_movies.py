# inspired by https://towardsdatascience.com/how-to-use-selenium-to-web-scrape-with-example-80f9b23a843a

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# import pandas as pd
import time
# import json
import modules.ld_json
import modules.auto_sign_in
import modules.justwatch
from alive_progress import alive_bar
import os
from dotenv import load_dotenv

load_dotenv()

dev_mode = os.environ.get('DEV_MODE').lower() == 'true'

options = webdriver.ChromeOptions()

# Run the browser in the background without opening a new window
options.add_argument("--headless=new")
# this will disable image loading
options.add_argument('--blink-settings=imagesEnabled=false')

# Open main window
driver = webdriver.Chrome(options=options)

driver.get('https://www.justwatch.com/us/lists/my-lists?content_type=movie&sort_by=random&sort_asc=true&sorting_random_seed=1')

driver.maximize_window()
# driver.implicitly_driwait(1.0)
# main_window_handle = driver.window_handles[0]


# Sign in to JustWatch using stored credentials (secret_login.bin)
modules.auto_sign_in.sign_in(driver)

time.sleep(5)

# Scroll to the end of the page
items_in_list = modules.justwatch.get_titles_count(driver)
if dev_mode:
    items_in_list = 5
pages = (items_in_list // 20) + 1
i = 0
with alive_bar(pages, spinner='waves', bar='squares') as bar:
    for i in range(pages):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(.5)
        bar()


# Get name, episode number/title, left in season, main show link from main watchlist
show_cards = driver.find_elements(By.XPATH, '//div[@class="title-card-basic title-card-basic"]')
if dev_mode:
    show_cards = show_cards[0:5]

i = 0
show_card_all_links = []
show_card_full_text = []
for i in range(len(show_cards)):
    show_card_all_links.append(show_cards[i].find_elements(By.TAG_NAME,'a'))
    show_card_full_text.append(show_cards[i].text)

i = 0
show_main_link = []
for i in range(len(show_card_all_links)):
    show_main_link.append(show_card_all_links[i][0].get_dom_attribute('href'))

i = 0
show_name = []
episode_number = []
episode_left_in_season = []
episode_title = []
for i in range(len(show_card_full_text)):
    this_show_elements = show_card_full_text[i].split(sep='\n')
    show_name.append(this_show_elements[0])
    # episode_number.append(this_show_elements[2])
    # if this_show_elements[3][0] == "+":
    #     episode_left_in_season.append(this_show_elements[3])
    #     episode_title.append(this_show_elements[4])
    # else:
    #     episode_left_in_season.append('')
    #     episode_title.append(this_show_elements[3])
    episode_number.append('')
    episode_left_in_season.append('')
    episode_title.append('')


# Get genres, runtime, age rating from show pages
j = 0
show_genres = []
show_runtime = []
show_age_rating = []
year = []
media_type = []
synopsis = []
with alive_bar(len(show_main_link), spinner='waves', bar='squares') as bar:
    for j in range(len(show_main_link)):
        full_url = 'https://www.justwatch.com' + show_main_link[j]

        # Get year, media type, age rating, and synopsis quickly from ld-json data
        show_ld_json_data = modules.ld_json.get_ld_json(full_url)


        # Visit each page to get genres and runtimes
        # from https://www.browserstack.com/guide/selenium-wait-for-page-to-load
        driver.get(full_url)
        try:
            elem = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="title-info title-info"]'))
            )
        finally:
            time.sleep(.5)

        title_info = driver.find_element(By.XPATH, '//div[@class="title-info title-info"]')
        detail_infos = title_info.find_elements(By.XPATH,'//div[@class="detail-infos"]')

        # Loop through each section on the page to get headings and text
        k = 0
        title_info_heading = []
        title_info_value = []
        shows_dict = []
        for k in range(len(detail_infos)):
            text = detail_infos[k].text
            if len(text) > 0:
                text_split = text.split(sep='\n')
                split_head = text_split[0]
                split_value = text_split[1]
                title_info_heading.append(split_head)
                title_info_value.append(split_value)

        shows_dict = dict(zip(title_info_heading,title_info_value))
        show_genres.append(shows_dict.get('GENRES'))
        show_runtime.append(shows_dict.get('RUNTIME'))
        # show_age_rating.append(shows_dict.get('AGE RATING'))

        year.append(str(show_ld_json_data['dateCreated']).split('-')[0])
        media_type.append(show_ld_json_data['@type'])
        show_age_rating.append(show_ld_json_data['contentRating'])
        synopsis.append(show_ld_json_data['description'])
        
        bar.text = show_main_link[j]
        bar()


# driver.close()
driver.quit()


# Pull elements together
data_tuples = list(zip(show_name,episode_number,episode_left_in_season,episode_title,show_genres,show_runtime,show_age_rating,show_main_link,year,media_type,synopsis))
# sorted(data_tuples)

# df = pd.DataFrame(data_tuples, columns=['Show Name','Episode Number','Episodes Remaining','Episode Title','Genres','Runtime','Age Rating'])
# html_string = df.to_html()


# Save my work
import modules.data_bin_convert
modules.data_bin_convert.data_to_bin(data_tuples, './saved_data_movies.bin')
# data_tuples = modules.data_bin_convert.bin_to_data()
