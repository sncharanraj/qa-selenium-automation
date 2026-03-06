import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.products_page import ProductsPage

def react_type(driver, field_id, value):
    """React-compatible input — uses native setter to trigger React state"""
    el = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, field_id))
    )
    driver.execute_script("""
        var el = arguments[0];
        var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value'
        ).set;
        nativeInputValueSetter.call(el, arguments[1]);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    """, el, value)
    time.sleep(0.2)

class TestCheckout:

    def _go_to_checkout(self, driver):
        p = ProductsPage(driver)
        p.add_item(0)
        p.go_to_cart()
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "checkout"))
        )
        driver.execute_script("arguments[0].click();", el)
        WebDriverWait(driver, 10).until(EC.url_contains("checkout-step-one"))

    def test_full_checkout_success(self, logged_in_driver):
        self._go_to_checkout(logged_in_driver)

        react_type(logged_in_driver, "first-name",  "Ravi")
        react_type(logged_in_driver, "last-name",   "Kumar")
        react_type(logged_in_driver, "postal-code", "560001")

        logged_in_driver.execute_script(
            "arguments[0].click();",
            logged_in_driver.find_element(By.ID, "continue")
        )
        WebDriverWait(logged_in_driver, 10).until(
            EC.url_contains("checkout-step-two")
        )
        logged_in_driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(logged_in_driver, 10).until(
                EC.element_to_be_clickable((By.ID, "finish"))
            )
        )
        header = WebDriverWait(logged_in_driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text
        assert "Thank you" in header

    def test_checkout_missing_first_name(self, logged_in_driver):
        self._go_to_checkout(logged_in_driver)
        react_type(logged_in_driver, "last-name",   "Kumar")
        react_type(logged_in_driver, "postal-code", "560001")
        logged_in_driver.execute_script(
            "arguments[0].click();",
            logged_in_driver.find_element(By.ID, "continue")
        )
        error = WebDriverWait(logged_in_driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        ).text
        assert "First Name is required" in error

    def test_checkout_missing_postal_code(self, logged_in_driver):
        self._go_to_checkout(logged_in_driver)
        react_type(logged_in_driver, "first-name", "Ravi")
        react_type(logged_in_driver, "last-name",  "Kumar")
        logged_in_driver.execute_script(
            "arguments[0].click();",
            logged_in_driver.find_element(By.ID, "continue")
        )
        error = WebDriverWait(logged_in_driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        ).text
        assert "Postal Code is required" in error
