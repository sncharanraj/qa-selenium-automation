# 🤖 Selenium Automation Framework — SauceDemo

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.18-green)
![Pytest](https://img.shields.io/badge/Pytest-8.1-orange)
![Tests](https://img.shields.io/badge/Tests-14%20Passed-brightgreen)
![POM](https://img.shields.io/badge/Design-Page%20Object%20Model-purple)

---

## 📌 Project Overview

End-to-end **Selenium automation framework** built with Python to test
the SauceDemo e-commerce web application. Uses the **Page Object Model
(POM)** design pattern for clean, maintainable, and scalable test code.

**Site Under Test:** https://www.saucedemo.com
**Total Tests:** 14 automated test cases
**Result:** 14/14 Passing ✅

---

## 📁 Project Structure

\`\`\`
qa-selenium-automation/
│
├── conftest.py               ← Browser setup/teardown fixtures
├── pytest.ini                ← Pytest configuration
├── requirements.txt          ← All dependencies
│
├── pages/                    ← Page Object Model classes
│   ├── base_page.py          ← Parent class with common helpers
│   ├── login_page.py         ← Login page locators & actions
│   └── products_page.py      ← Products page locators & actions
│
└── tests/                    ← Test suites
    ├── test_login.py          ← 5 login/auth test cases
    ├── test_products.py       ← 6 product & cart test cases
    └── test_checkout.py       ← 3 checkout test cases
\`\`\`

---

## 🧪 Test Cases

### 🔐 Login Tests (5)
| Test | Scenario | Result |
|------|---------|--------|
| test_valid_login | Valid credentials → redirects to products | ✅ Pass |
| test_wrong_password_shows_error | Wrong password → error message | ✅ Pass |
| test_locked_out_user | Locked account → specific error | ✅ Pass |
| test_empty_username | No input → validation error | ✅ Pass |
| test_logout_returns_to_login | Logout → back to login page | ✅ Pass |

### 📦 Products & Cart Tests (6)
| Test | Scenario | Result |
|------|---------|--------|
| test_products_page_loads | Products title visible after login | ✅ Pass |
| test_add_one_item_cart_shows_1 | Add 1 item → badge shows 1 | ✅ Pass |
| test_add_two_items_cart_shows_2 | Add 2 items → badge shows 2 | ✅ Pass |
| test_sort_price_low_to_high | Sort → prices ascending | ✅ Pass |
| test_sort_price_high_to_low | Sort → prices descending | ✅ Pass |
| test_sort_name_a_to_z | Sort → names alphabetical | ✅ Pass |

### 💳 Checkout Tests (3)
| Test | Scenario | Result |
|------|---------|--------|
| test_full_checkout_success | Full flow → Thank you page | ✅ Pass |
| test_checkout_missing_first_name | Blank first name → error | ✅ Pass |
| test_checkout_missing_postal_code | Blank postal code → error | ✅ Pass |

---

## ⚙️ Setup & Run

### Prerequisites
- Python 3.12+
- Google Chrome installed
- ChromeDriver (matching Chrome version)

### Installation
\`\`\`bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/qa-selenium-automation.git
cd qa-selenium-automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
\`\`\`

### Run Tests
\`\`\`bash
# Run all tests
pytest tests/ -v

# Run specific module
pytest tests/test_login.py -v

# Generate HTML report
pytest tests/ -v --html=report.html
\`\`\`

---

## 🏗️ Key Concepts Used

**Page Object Model (POM)**
Each page has its own class storing locators and actions.
Tests call page methods — never interact with the DOM directly.
This means if a locator changes, you update it in ONE place only.

**Explicit Waits**
Used \`WebDriverWait\` + \`ExpectedConditions\` instead of \`time.sleep()\`.
Tests wait for elements to be visible/clickable before interacting.

**JavaScript Click**
Used \`execute_script("arguments[0].click()")\` for elements blocked
by CSS animations (burger menu) or React rendering.

**React-Compatible Input**
SauceDemo checkout uses React controlled inputs.
Used native \`HTMLInputElement\` setter + dispatched input events
to properly trigger React state updates.

**Fixtures (conftest.py)**
\`driver\` fixture — fresh browser per test
\`logged_in_driver\` fixture — pre-authenticated browser for cart/checkout tests

---

## 🛠️ Tools & Technologies

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12 | Programming language |
| Selenium | 4.18 | Browser automation |
| Pytest | 8.1 | Test framework |
| pytest-html | 4.1 | HTML report generation |
| ChromeDriver | 145 | Chrome browser driver |
| WSL2 | Ubuntu 24 | Development environment |

---

## 💡 Challenges & Solutions

| Challenge | Solution |
|-----------|---------|
| webdriver_manager downloaded wrong file | Manually installed ChromeDriver |
| Burger menu animation blocking clicks | Used JavaScript click |
| React inputs not accepting send_keys | Used HTMLInputElement native setter |
| Sort dropdown timing issue | Used element_to_be_clickable wait |

---

## 👤 Author

**QA Engineer** — Trainee Testing Engineer
📍 Mangalore, Karnataka, India

---

## 📄 License
For portfolio and educational purposes only.
