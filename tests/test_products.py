from pages.products_page import ProductsPage

class TestProducts:

    def test_products_page_loads(self, logged_in_driver):
        p = ProductsPage(logged_in_driver)
        assert p.get_title() == "Products"

    def test_add_one_item_cart_shows_1(self, logged_in_driver):
        p = ProductsPage(logged_in_driver)
        p.add_item(0)
        assert p.get_cart_count() == 1

    def test_add_two_items_cart_shows_2(self, logged_in_driver):
        p = ProductsPage(logged_in_driver)
        p.add_item(0)
        p.add_item(1)
        assert p.get_cart_count() == 2

    def test_sort_price_low_to_high(self, logged_in_driver):
        p = ProductsPage(logged_in_driver)
        p.sort("Price (low to high)")
        prices = p.get_prices()
        assert prices == sorted(prices)   # sorted() returns ascending order

    def test_sort_price_high_to_low(self, logged_in_driver):
        p = ProductsPage(logged_in_driver)
        p.sort("Price (high to low)")
        prices = p.get_prices()
        assert prices == sorted(prices, reverse=True)

    def test_sort_name_a_to_z(self, logged_in_driver):
        p = ProductsPage(logged_in_driver)
        p.sort("Name (A to Z)")
        names = p.get_names()
        assert names == sorted(names)
