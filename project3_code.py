from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumProjectChrome:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()

    def open_website(self):
        self.driver.get(self.url)

    def perform_search(self, search_query):
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

    def get_search_results(self):
        # Wait for the results to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3"))
        )
        results = self.driver.find_elements(By.CSS_SELECTOR, "h3")
        return [result.text for result in results]

    def close_browser(self):
        self.driver.quit()
