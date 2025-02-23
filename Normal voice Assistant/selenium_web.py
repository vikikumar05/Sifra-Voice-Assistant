from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

class Info:
    def __init__(self):
        # Automatically installs and updates ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def get_info(self, query):
        self.driver.get("https://www.wikipedia.org/")

        search = self.driver.find_element(By.XPATH, '//*[@id="searchInput"]')
        search.click()
        search.send_keys(query + Keys.RETURN)  # Ensures search execution

        input("Press Enter to close the browser...")
        self.driver.quit()

#
# assist = Info()
# assist.get_info("black hole")
