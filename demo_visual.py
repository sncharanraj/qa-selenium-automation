import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

options = Options()
options.add_argument("--headless=new")           # new headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")            # ✅ KEY FIX for WSL
options.add_argument("--disable-software-rasterizer")  # ✅ disable GPU fallback
options.add_argument("--disable-gpu-sandbox")
options.add_argument("--window-size=1280,800")

service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

def pause(msg, secs=1):
    print(f"\n👉 {msg}")
    time.sleep(secs)

try:
    print("\n" + "="*55)
    print("🤖 SELENIUM AUTOMATION DEMO STARTING...")
    print("="*55)

    # ── STEP 1: Open website ──────────────────────────────────
    pause("Opening https://www.saucedemo.com ...", 1)
    driver.get("https://www.saucedemo.com")
    pause(f"✅ Page loaded! Title: '{driver.title}'", 1)

    # ── STEP 2: Login ─────────────────────────────────────────
    print("\n" + "-"*40)
    print("🔐 LOGGING IN")
    print("-"*40)
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    pause("✅ Typed username: standard_user", 1)
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    pause("✅ Typed password: secret_sauce", 1)
    driver.find_element(By.ID, "login-button").click()
    wait.until(EC.url_contains("inventory"))
    pause(f"✅ LOGIN SUCCESS! URL: {driver.current_url}", 1)

    # ── STEP 3: Read all products ─────────────────────────────
    print("\n" + "-"*40)
    print("📦 READING ALL PRODUCTS")
    print("-"*40)
    names  = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    pause(f"Found {len(names)} products:", 1)
    for name, price in zip(names, prices):
        print(f"   • {name.text:<45} {price.text}")

    # ── STEP 4: Sort products ─────────────────────────────────
    print("\n" + "-"*40)
    print("🔃 SORTING BY PRICE LOW TO HIGH")
    print("-"*40)
    dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
    Select(dropdown).select_by_visible_text("Price (low to high)")
    pause("✅ Sort applied!", 1)
    prices_sorted = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    names_sorted  = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    for name, price in zip(names_sorted, prices_sorted):
        print(f"   • {name.text:<45} {price.text}")

    # ── STEP 5: Add 2 items to cart ───────────────────────────
    print("\n" + "-"*40)
    print("🛒 ADDING ITEMS TO CART")
    print("-"*40)
    first = driver.find_elements(By.CLASS_NAME, "inventory_item_name")[0].text
    buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-test^='add-to-cart']")))
    buttons[0].click()
    badge = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))).text
    pause(f"✅ Added '{first}' → Cart: {badge}", 1)

    second = driver.find_elements(By.CLASS_NAME, "inventory_item_name")[1].text
    buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-test^='add-to-cart']")))
    buttons[0].click()
    wait.until(lambda d: d.find_element(By.CLASS_NAME, "shopping_cart_badge").text == "2")
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    pause(f"✅ Added '{second}' → Cart: {badge}", 1)

    # ── STEP 6: View cart ─────────────────────────────────────
    print("\n" + "-"*40)
    print("👜 VIEWING CART")
    print("-"*40)
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    wait.until(EC.url_contains("cart"))
    pause(f"✅ On cart page!", 1)
    cart_items  = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    cart_prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    for item, price in zip(cart_items, cart_prices):
        print(f"   • {item.text:<45} {price.text}")

    # ── STEP 7: Checkout ──────────────────────────────────────
    print("\n" + "-"*40)
    print("💳 CHECKOUT")
    print("-"*40)
    driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "checkout"))
    wait.until(EC.visibility_of_element_located((By.ID, "first-name")))
    pause("✅ On checkout form — filling details...", 1)

    driver.find_element(By.ID, "first-name").send_keys("Ravi")
    driver.find_element(By.ID, "last-name").send_keys("Kumar")
    driver.find_element(By.ID, "postal-code").send_keys("560001")
    pause("✅ Filled: Ravi Kumar, 560001", 1)

    driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "continue"))
    wait.until(EC.url_contains("checkout-step-two"))

    subtotal = driver.find_element(By.CLASS_NAME, "summary_subtotal_label").text
    tax      = driver.find_element(By.CLASS_NAME, "summary_tax_label").text
    total    = driver.find_element(By.CLASS_NAME, "summary_total_label").text
    print(f"\n   {subtotal}")
    print(f"   {tax}")
    print(f"   {total}")

    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable((By.ID, "finish")))
    )
    header = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
    ).text
    pause(f"🎉 ORDER PLACED! '{header}'", 1)

    # ── STEP 8: Logout ────────────────────────────────────────
    print("\n" + "-"*40)
    print("🚪 LOGGING OUT")
    print("-"*40)
    driver.execute_script(
        "arguments[0].click();",
        driver.find_element(By.ID, "react-burger-menu-btn")
    )
    time.sleep(1)
    driver.execute_script(
        "arguments[0].click();",
        wait.until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link")))
    )
    wait.until(EC.url_to_be("https://www.saucedemo.com/"))
    pause(f"✅ Logged out! Back at: {driver.current_url}", 1)

    print("\n" + "="*55)
    print("🏆 FULL AUTOMATION DEMO COMPLETE!")
    print("   Every action above = Python code, zero human clicks!")
    print("="*55)

finally:
    time.sleep(1)
    driver.quit()
