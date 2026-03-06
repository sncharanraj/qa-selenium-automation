import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")

    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(15)

    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def logged_in_driver(driver):
    # ✅ Retry login up to 3 times — handles flaky network/load
    for attempt in range(3):
        try:
            driver.get("https://www.saucedemo.com")
            time.sleep(1)  # let page settle

            user = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "user-name"))
            )
            user.clear()
            user.send_keys("standard_user")

            pwd = driver.find_element(By.ID, "password")
            pwd.clear()
            pwd.send_keys("secret_sauce")

            driver.find_element(By.ID, "login-button").click()

            WebDriverWait(driver, 15).until(EC.url_contains("inventory"))
            return driver  # success

        except Exception as e:
            if attempt == 2:
                raise e
            time.sleep(2)  # wait before retry
