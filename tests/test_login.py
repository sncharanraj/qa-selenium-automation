from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

class TestLogin:

    def test_valid_login(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "secret_sauce")
        assert "inventory" in driver.current_url

    def test_wrong_password_shows_error(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login("standard_user", "wrongpass")
        assert login.is_error_shown()
        assert "do not match" in login.get_error()

    def test_locked_out_user(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login("locked_out_user", "secret_sauce")
        assert "locked out" in login.get_error().lower()

    def test_empty_username(self, driver):
        login = LoginPage(driver)
        login.open()
        login.click(*login.LOGIN_BTN)
        assert "Username is required" in login.get_error()

    def test_logout_returns_to_login(self, logged_in_driver):
        # ✅ FIX: use JavaScript click — bypasses headless burger menu animation issue
        burger = WebDriverWait(logged_in_driver, 10).until(
            EC.presence_of_element_located((By.ID, "react-burger-menu-btn"))
        )
        logged_in_driver.execute_script("arguments[0].click();", burger)

        logout = WebDriverWait(logged_in_driver, 10).until(
            EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
        )
        logged_in_driver.execute_script("arguments[0].click();", logout)

        # ✅ Wait until URL is exactly the login page
        WebDriverWait(logged_in_driver, 10).until(
            EC.url_to_be("https://www.saucedemo.com/")
        )
        assert logged_in_driver.current_url == "https://www.saucedemo.com/"
