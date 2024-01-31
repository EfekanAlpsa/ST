from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def login_to_local_page(username, password):
    driver = webdriver.Chrome()
    driver.get("http://localhost:63342/ST/index.html?_ijt=dq4dqm15oaesiq5qd0bn44dqof&_ij_reload=RELOAD_ON_SAVE")
    time.sleep(2)
    username_field = driver.find_element("id", "username")
    password_field = driver.find_element("id", "password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = driver.find_element("xpath", "//button[text()='Login']")
    login_button.click()

    time.sleep(2)
    driver.quit()

if __name__ == "__main__":
    login_to_local_page("user123", "pass456")
