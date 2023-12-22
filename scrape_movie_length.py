from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



driver = webdriver.Chrome()

driver.get('https://www.justwatch.com/us/movie/8-bit-christmas')



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
length_text = driver.find_elements(By.XPATH, length_xpath)[9].text

length_text_hour = length_text.split(" ")[0]
length_text_min = length_text.split(" ")[1]
length_minutes = (int(length_text_hour.split("h")[0]) * 60) + int(length_text_min.split("min")[0])


length_rounded_up = length_minutes + 15 - (length_minutes % 15)



driver.quit()