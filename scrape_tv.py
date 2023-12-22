# inspired by https://towardsdatascience.com/how-to-use-selenium-to-web-scrape-with-example-80f9b23a843a


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# import pandas as pd
import time
# import json
# from function_length_tv import length_tv


# Open main window
driver = webdriver.Chrome()

driver.get('https://www.justwatch.com/us/lists/tv-show-tracking?inner_tab=continue_watching')

driver.maximize_window()
driver.implicitly_wait(1.0)
main_window_handle = driver.window_handles[0]





input("Sign in, and then press Enter to continue...")


driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(1)




# Show name
title_xpath = '//p[@class="title-card-show-episode__title-name"]'
titles = driver.find_elements(By.XPATH, title_xpath)

titles_list = []
for p in range(len(titles)):
    titles_list.append(titles[p].text)


# Season, episode numbers
episode_heading_xpath = '//h2[@class="title-card-heading"]'
episode_headings = driver.find_elements(By.XPATH, episode_heading_xpath)

episode_headings_list = []
for p in range(len(episode_headings)):
    episode_headings_list.append(episode_headings[p].text)


# Episode name
episode_name_xpath = '//p[@class="title-card-show-episode__episode-name"]'
episode_names = driver.find_elements(By.XPATH, episode_name_xpath)

episode_names_list = []
for p in range(len(episode_names)):
    episode_names_list.append(episode_names[p].text)


# Show URL
episode_url_xpath = '//div[@class="title-card-basic title-card-show-episode"]'
episode_urls = []

all_show_data = driver.find_elements(By.XPATH,episode_url_xpath)

i = 0
for i in range(len(all_show_data)):
    episode_urls.append(all_show_data[i].find_element(By.TAG_NAME,'a').get_dom_attribute('href'))


# Show length
driver.switch_to.new_window()
tab_handle = driver.window_handles[1]
# driver.switch_to.window(tab_handle)

episode_length = []
j = 0
for j in range(len(episode_urls)):
    # driver.switch_to.new_window()
    # tab_handle = driver.window_handles[1]
    # driver.switch_to.window(tab_handle)
    # length_tv(driver,'https://www.justwatch.com' + episode_urls[1])
    
    driver.get('https://www.justwatch.com' + episode_urls[j])
    time.sleep(3)

    length_xpath = '//div[@class="detail-infos__value"]'
    length_text = driver.find_elements(By.XPATH, length_xpath)[3].text
    length_minutes = int(length_text.split("min")[0])

    episode_length.append(length_minutes + 15 - (length_minutes % 15))

driver.close(tab_handle)
driver.switch_to.window(main_window_handle)
# time.sleep(1)


# Pull elements together
df = pd.DataFrame(columns=['Show','Episode Number','Episode Name','URL','Length']) # creates master dataframe 

data_tuples = list(zip(titles_list[0:],episode_headings_list[0:],episode_names_list[0:],episode_urls[0:],episode_length[0:]))
df = pd.DataFrame(data_tuples, columns=['Show','Episode Number','Episode Name','URL','Length'])
# temp_df['Year'] = yr # adds season beginning year to each dataframe
# df = df.append(temp_df) # appends to master dataframe


jsonObject = json.dumps(data_tuples)
print(jsonObject)
print(type(jsonObject))
    

driver.quit()