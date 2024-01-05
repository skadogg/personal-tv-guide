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


def get_title_cover(title): # TODO:
    # Takes a movie list and looks up the URL for the cover iamge
    url = ''
    return url


def movie_of_the_week(list):
    # Takes a random movie from the list and returns the chosen movie and the URL for the cover iamge
    # Example: movie_of_the_week, img_url = movie_of_the_week(list)
    random.shuffle(list)
    show = list[0]
    cover_url = get_title_cover(show)
    return show, cover_url
