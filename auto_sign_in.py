from selenium import webdriver
from selenium.webdriver.common.by import By

def sign_in(driver):
    login_creds = {
        "email": "ydhaxkdefmcowfebti@cazlv.com",
        "password": "skadogg@!@#$555"
    }

    # go to sign in page
    driver.find_element(By.CLASS_NAME, "not-logged-in").click()
    driver.implicitly_wait(2.0)
    driver.find_elements(By.CLASS_NAME, "text-wrapper")[0].click()
    driver.find_elements(By.CLASS_NAME, "firebaseui-list-item")[3].click()

    # sign in
    driver.find_element(By.NAME, "email").send_keys(login_creds["email"])
    driver.find_element(By.CLASS_NAME, "firebaseui-id-submit").click()
    driver.find_element(By.NAME, "password").send_keys(login_creds["password"])
    driver.find_element(By.CLASS_NAME, "firebaseui-id-submit").click()