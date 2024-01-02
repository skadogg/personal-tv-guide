from selenium import webdriver
from selenium.webdriver.common.by import By


def get_titles_count(driver):
    # Reads number of titles from top of page, e.g. "887 titles," and converts to int
    titles_count_str = driver.find_element(By.XPATH, '//div[@class="titles-count"]').text
    titles_count = int(titles_count_str.split(' titles')[0])
    return titles_count
