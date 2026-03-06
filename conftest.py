import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)

    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def logged_in_driver(driver):
    driver.get("https://www.saucedemo.com")
    driver.find_element("id", "user-name").send_keys("standard_user")
    driver.find_element("id", "password").send_keys("secret_sauce")
    driver.find_element("id", "login-button").click()
    return driver
