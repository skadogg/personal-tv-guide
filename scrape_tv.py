# inspired by https://towardsdatascience.com/how-to-use-selenium-to-web-scrape-with-example-80f9b23a843a


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
# import json
# from function_length_tv import length_tv


# Open main window
driver = webdriver.Chrome()

driver.get('https://www.justwatch.com/us/lists/tv-show-tracking?inner_tab=continue_watching')

driver.maximize_window()
# driver.implicitly_driwait(1.0)
# main_window_handle = driver.window_handles[0]





input("Sign in, and then press Enter to continue...")



items_in_list = 60
pages = items_in_list // 20
i = 0
for i in range(pages):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)



# name, episode number/title, left in season, main show link
show_cards = driver.find_elements(By.XPATH, '//div[@class="title-card-basic title-card-show-episode"]')
# len(show_cards)

i = 0
show_card_all_links = []
show_card_full_text = []
for i in range(len(show_cards)):
    show_card_all_links.append(show_cards[i].find_elements(By.TAG_NAME,'a'))
    show_card_full_text.append(show_cards[i].text)

# show_card_all_links[23][0].get_dom_attribute('href')
i = 0
show_main_link = []
for i in range(len(show_card_all_links)):
    # show_card_all_links[i][0].get_dom_attribute('href')
    show_main_link.append(show_card_all_links[i][0].get_dom_attribute('href'))

i = 0
show_name = []
episode_number = []
episode_left_in_season = []
episode_title = []
for i in range(len(show_card_full_text)):
    this_show_elements = show_card_full_text[i].split(sep='\n')
    show_name.append(this_show_elements[1])
    episode_number.append(this_show_elements[2])
    episode_left_in_season.append(this_show_elements[3])
    episode_title.append(this_show_elements[4])


# show_name
# episode_number
# episode_left_in_season
# episode_title
# show_main_link


# # Show name
# title_xpath = '//p[@class="title-card-show-episode__title-name"]'
# titles = driver.find_elements(By.XPATH, title_xpath)

# titles_list = []
# for p in range(len(titles)):
#     titles_list.append(titles[p].text)


# # Season, episode numbers
# episode_heading_xpath = '//h2[@class="title-card-heading"]'
# episode_headings = driver.find_elements(By.XPATH, episode_heading_xpath)

# episode_headings_list = []
# for p in range(len(episode_headings)):
#     episode_headings_list.append(episode_headings[p].text)


# # Episode name
# episode_name_xpath = '//p[@class="title-card-show-episode__episode-name"]'
# episode_names = driver.find_elements(By.XPATH, episode_name_xpath)

# episode_names_list = []
# for p in range(len(episode_names)):
#     episode_names_list.append(episode_names[p].text)


# # Show URL
# episode_url_xpath = '//div[@class="title-card-basic title-card-show-episode"]'
# episode_urls = []

# all_show_data = driver.find_elements(By.XPATH,episode_url_xpath)

# i = 0
# for i in range(len(all_show_data)):
#     episode_urls.append(all_show_data[i].find_element(By.TAG_NAME,'a').get_dom_attribute('href'))


# title_card = driver.find_element(By.XPATH, '//div[@class="title-card-basic title-card-show-episode"]')
# title_card.find_element(By.TAG_NAME,'a').get_dom_attribute('href')


# Show length
# driver.switch_to.new_window()
# tab_handle = driver.window_handles[1]
# driver.switch_to.window(tab_handle)


# episode_length = []
j = 0
show_genres = []
show_runtime = []
show_age_rating = []
for j in range(len(show_main_link)):
    # driver.switch_to.new_window()
    # tab_handle = driver.window_handles[1]
    # driver.switch_to.window(tab_handle)
    # length_tv(driver,'https://www.justwatch.com' + episode_urls[1])

    # https://www.browserstack.com/guide/selenium-wait-for-page-to-load
    driver.get('https://www.justwatch.com' + show_main_link[j])
    try:
        elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="title-info title-info"]'))
        )
    finally:
        time.sleep(1)

    # length_xpath = '//div[@class="detail-infos__value"]'
    # length_text = driver.find_elements(By.XPATH, length_xpath)[3].text
    # length_minutes = int(length_text.split("min")[0])

    # episode_length.append(length_minutes + 15 - (length_minutes % 15))


    # Genres, runtime, age rating
    title_info = driver.find_element(By.XPATH, '//div[@class="title-info title-info"]')
    detail_infos = title_info.find_elements(By.XPATH,'//div[@class="detail-infos"]')

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

    # shows_dict = dict(zip(title_info_heading[0:],title_info_value[0:]))
    shows_dict = dict(zip(title_info_heading,title_info_value))
    show_genres.append(shows_dict.get('GENRES'))
    show_runtime.append(shows_dict.get('RUNTIME'))
    show_age_rating.append(shows_dict.get('AGE RATING'))
    
    # show_genres
    # show_runtime
    # show_age_rating



# driver.close()
# driver.switch_to.window(main_window_handle)
# # time.sleep(1)


# Pull elements together
# df = pd.DataFrame(columns=['Show Name','Episode Number','Episode Name','Show URL','Runtime']) # creates master dataframe

# data_tuples = list(zip(titles_list[0:],episode_headings_list[0:],episode_names_list[0:],episode_urls[0:],episode_length[0:]))
df = pd.DataFrame(data_tuples, columns=['Show','Episode Number','Episode Name','URL','Length'])
# temp_df['Year'] = yr # adds season beginning year to each dataframe
# df = df.append(temp_df) # appends to master dataframe


# show_name
# episode_number
# episode_left_in_season
# episode_title
# show_genres
# show_runtime
# show_age_rating

data_tuples = list(zip(show_name,episode_number,episode_left_in_season,episode_title,show_genres,show_runtime,show_age_rating))
sorted(data_tuples)

df = pd.DataFrame(data_tuples, columns=['Show Name','Episode Number','Episodes Remaining','Episode Title','Genres','Runtime','Age Rating'])

html_string = df.to_html()


# jsonObject = json.dumps(data_tuples)
# print(jsonObject)
# print(type(jsonObject))


# driver.quit()

df.sample(2)

