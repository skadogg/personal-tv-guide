from selenium import webdriver
from selenium.webdriver.common.by import By

def length_tv(driver, url):
    driver.get(url)
    
    length_xpath = '//div[@class="detail-infos__value"]'
    length_text = driver.find_elements(By.XPATH, length_xpath)[3].text
    length_minutes = int(length_text.split("min")[0])

    length_rounded_up = length_minutes + 15 - (length_minutes % 15)
    
    return length_rounded_up

