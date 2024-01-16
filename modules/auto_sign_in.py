from base64 import b64encode, b64decode, decode
from modules import data_bin_convert
from os import path
from selenium.webdriver.common.by import By
import logging
import time


def sign_in(driver):
    # Sign in to JustWatch
    email = ''
    password = ''
    secret_login_file = './my_data/secret_login.bin'
    sleep_at_the_end = 7

    # Look for stored credentials and prompt if none are found
    if(path.isfile(secret_login_file)):
        logging.debug('Secret login file found:')
        logging.debug(f'{secret_login_file=}')
        login_data = data_bin_convert.bin_to_data(secret_login_file)
        email = login_data[0]
        password = b64decode(login_data[1]).decode("utf-8")
    else:
        logging.warning('Secret login file found not found. Prompting for creds.')
        print("If you enter the wrong password, delete secret login file:")
        print(f'{secret_login_file=}')
        email = input("Email Address:")
        password = input("Password:")
        hashed_password = b64encode(password.encode("utf-8"))
        login_data = [email, hashed_password]
        data_bin_convert.data_to_bin(login_data, secret_login_file)

    try:
        logging.debug('Trying to sign in')
        # Open sign in modal
        driver.find_element(By.CLASS_NAME, "not-logged-in").click()
        driver.implicitly_wait(2.0)
        driver.find_elements(By.CLASS_NAME, "text-wrapper")[0].click()
        driver.find_elements(By.CLASS_NAME, "firebaseui-list-item")[3].click()
        
        # Sign in with user credentials
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.CLASS_NAME, "firebaseui-id-submit").click()
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CLASS_NAME, "firebaseui-id-submit").click()
    except:
        logging.error('Error signing in')
    else:
        # Wait for successful sign in modal to go away - usually takes five to seven seconds (for me)
        logging.debug('Sleeping for x seconds:')
        logging.debug(f'{sleep_at_the_end=}')
        time.sleep(sleep_at_the_end)
