from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



driver = webdriver.Chrome()

driver.get('https://www.justwatch.com/us/tv-show/one-day-at-a-time-2016/season-2')


# input("Sign in, and then press Enter to continue...")


# driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
# time.sleep(1)
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
# time.sleep(1)
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
# time.sleep(1)
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
# time.sleep(1)



length_xpath = '//div[@class="detail-infos__value"]'
length_text = driver.find_elements(By.XPATH, length_xpath)[7].text
length_minutes = int(length_text.split("min")[0])

length_rounded_up = length_minutes + 15 - (length_minutes % 15)



driver.quit()