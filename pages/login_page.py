from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators — how to find each element on the page
    USERNAME  = (By.ID, "user-name")
    PASSWORD  = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        super().open("")  # opens https://www.saucedemo.com

    def login(self, username, password):
        self.type_text(*self.USERNAME, username)
        self.type_text(*self.PASSWORD, password)
        self.click(*self.LOGIN_BTN)

    def get_error(self):
        return self.get_text(*self.ERROR_MSG)

    def is_error_shown(self):
        return self.is_visible(*self.ERROR_MSG)
