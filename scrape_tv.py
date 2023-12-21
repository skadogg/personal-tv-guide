# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

driver = webdriver.Chrome()

driver.get('https://www.justwatch.com/us/lists/tv-show-tracking?inner_tab=continue_watching')


input("Sign in, and then press Enter to continue...")


driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(1)



title_xpath = '//p[@class="title-card-show-episode__title-name"]'
titles = driver.find_elements(By.XPATH, title_xpath)

titles_list = []
for p in range(len(titles)):
    titles_list.append(titles[p].text)


episode_heading_xpath = '//h2[@class="title-card-heading"]'
episode_headings = driver.find_elements(By.XPATH, episode_heading_xpath)

episode_headings_list = []
for p in range(len(episode_headings)):
    episode_headings_list.append(episode_headings[p].text)


episode_name_xpath = '//p[@class="title-card-show-episode__episode-name"]'
episode_names = driver.find_elements(By.XPATH, episode_name_xpath)

episode_names_list = []
for p in range(len(episode_names)):
    episode_names_list.append(episode_names[p].text)


df = pd.DataFrame(columns=['Show','Episode Number','Episode Name']) # creates master dataframe 

data_tuples = list(zip(titles_list[1:],episode_headings_list[1:],episode_names_list[1:]))
df = pd.DataFrame(data_tuples, columns=['Show','Episode Number','Episode Name'])
# temp_df['Year'] = yr # adds season beginning year to each dataframe
# df = df.append(temp_df) # appends to master dataframe
    

# driver.quit()