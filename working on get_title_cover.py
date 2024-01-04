from selenium import webdriver
from selenium.webdriver.common.by import By

def get_title_cover(title):
    # Takes a movie list and looks up the URL for the cover iamge
    
    
    options = webdriver.ChromeOptions()

    # Run the browser in the background without opening a new window
    # options.add_argument("--headless=new")
    # this will disable image loading
    # options.add_argument('--blink-settings=imagesEnabled=false')

    # Open main window
    driver = webdriver.Chrome(options=options)

    driver.get('https://www.justwatch.com' + title[7])
    # left_bar = driver.find_element(By.XPATH, '//div[@class="title-sidebar"]')
    # picture = left_bar.find_element(By.XPATH, '//picture[@class="picture-comp title-poster__image"]')
    # source = picture.find_elements(By.TAG_NAME, 'source')[0]
    # source.find_element(By.TAG_NAME,'data-srcset')
    
    meta = driver.find_element(By.XPATH, '//meta[@property="og:image"]')
    meta.find_element(By.NAME, '//meta[@content]') #TODO: figure out how to get the content
    
    meta.value_of_css_property
    
    find_element_by_css_selector('meta[data-vmid="og:image"]')
    for i in range(len(meta)):
        if meta[i].data-vmid == 'og:image':
            i
    
    driver.quit()
    
    
    url = ''
    return url

import modules.data_bin_convert
title = modules.data_bin_convert.bin_to_data("saved_data_movies.bin")[1]

get_title_cover(title)