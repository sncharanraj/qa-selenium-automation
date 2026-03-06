from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    BASE_URL = "https://www.saucedemo.com"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, path=""):
        self.driver.get(self.BASE_URL + path)

    def find(self, by, locator):
        # Wait until element is visible, then return it
        return self.wait.until(EC.visibility_of_element_located((by, locator)))

    def click(self, by, locator):
        self.wait.until(EC.element_to_be_clickable((by, locator))).click()

    def type_text(self, by, locator, text):
        field = self.find(by, locator)
        field.clear()
        field.send_keys(text)

    def get_text(self, by, locator):
        return self.find(by, locator).text

    def is_visible(self, by, locator):
        try:
            self.find(by, locator)
            return True
        except:
            return False
