from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class Music:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)  # Keeps browser open after script ends

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def play(self, query):
        self.driver.get("https://www.youtube.com/results?search_query=" + query)

        video = self.driver.find_element(By.XPATH, '(//a[@id="video-title"])[1]')  # Selects first video
        video.click()

        print("Video is playing... Press Enter to close the browser.")
        input()  # Waits for user input before closing

        self.driver.quit()  # Closes the browser when Enter is pressed

# #
# assist = Music()
# assist.play("Mehboob song")
