from selenium import webdriver
from selenium.webdriver.common.by import By
import random


def get_titles_count(driver):
    try:
        # Reads number of titles from top of page, e.g. "887 titles," and converts to int
        titles_count_str = driver.find_element(By.XPATH, '//div[@class="titles-count"]').text
        titles_count = int(titles_count_str.split(' titles')[0])
    except:
        print("Error getting title count")
    else:
        return titles_count


def get_random_show(list):
    # Takes a random show from the list and returns the chosen show
    r = random.randint(0,len(list))
    return list[r]
