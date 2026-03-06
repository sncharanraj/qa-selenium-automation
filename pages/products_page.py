from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class ProductsPage(BasePage):
    TITLE       = (By.CLASS_NAME, "title")
    ADD_BUTTONS = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
    CART_BADGE  = (By.CLASS_NAME, "shopping_cart_badge")
    CART_ICON   = (By.CLASS_NAME, "shopping_cart_link")
    # ✅ FIXED: correct sort dropdown locator
    SORT_DD     = (By.CLASS_NAME, "product_sort_container")
    PRICES      = (By.CLASS_NAME, "inventory_item_price")
    NAMES       = (By.CLASS_NAME, "inventory_item_name")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT      = (By.ID, "logout_sidebar_link")

    def get_title(self):
        return self.get_text(*self.TITLE)

    def add_item(self, index=0):
        btns = self.driver.find_elements(*self.ADD_BUTTONS)
        btns[index].click()

    def get_cart_count(self):
        try:
            return int(self.get_text(*self.CART_BADGE))
        except:
            return 0

    def go_to_cart(self):
        self.click(*self.CART_ICON)

    def sort(self, option):
        # ✅ FIXED: wait for element, then wrap in Select
        dropdown_el = self.wait.until(
            EC.element_to_be_clickable(self.SORT_DD)
        )
        Select(dropdown_el).select_by_visible_text(option)

    def get_prices(self):
        els = self.driver.find_elements(*self.PRICES)
        return [float(e.text.replace("$", "")) for e in els]

    def get_names(self):
        els = self.driver.find_elements(*self.NAMES)
        return [e.text for e in els]

    def logout(self):
        # ✅ FIXED: wait for burger menu to be clickable before clicking
        self.wait.until(EC.element_to_be_clickable(self.BURGER_MENU)).click()
        # Wait for sidebar to open, then click logout
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT)).click()
