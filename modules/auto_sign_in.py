from base64 import b64encode, b64decode, decode
from modules import data_bin_convert
from os import path
from selenium.webdriver.common.by import By
import time

def sign_in(driver):
    email = ""
    password = ""

    if(path.isfile('./secret_login.bin')):
        login_data = data_bin_convert.bin_to_data('./secret_login.bin')
        email = login_data[0]
        password = b64decode(login_data[1]).decode("utf-8")
    else:
        print("If you enter the wrong password, delete the 'secret_login.bin' file...")
        email = input("Email Address:")
        password = input("Password:")
        hashed_password = b64encode(password.encode("utf-8"))
        login_data = [email, hashed_password]
        data_bin_convert.data_to_bin(login_data, './secret_login.bin')

    # go to sign in page
    driver.find_element(By.CLASS_NAME, "not-logged-in").click()
    driver.implicitly_wait(2.0)
    driver.find_elements(By.CLASS_NAME, "text-wrapper")[0].click()
    driver.find_elements(By.CLASS_NAME, "firebaseui-list-item")[3].click()

    # sign in
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.CLASS_NAME, "firebaseui-id-submit").click()
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CLASS_NAME, "firebaseui-id-submit").click()
    
    # Wait for successful sign in modal to go away
    time.sleep(2.5)