import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Open ScopeX Money website
    driver.get("https://scopex.money/")
    print("Opened ScopeX Money website")

    # Login process
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Login')]"))).click()

    # Avoid hardcoding credentials
    username = os.getenv("SCOPEX_USERNAME", "kishorebalaji3586@gmail.com")
    password = os.getenv("SCOPEX_PASSWORD", "Test@246")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in')]"))).click()
    print("Logged in successfully")

    # Wait for the dashboard menu to load
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Dashboard')]")))

    # Locate the Recipients menu button
    recipient_menu = driver.find_element(By.XPATH, "//span[contains(text(), 'Recipients')]/ancestor::button")

    # Click Recipients menu if it's collapsed
    if "bg-blue-100" not in recipient_menu.get_attribute("class"):  # Adjust if needed
        print("Clicking Recipients menu to expand")
        recipient_menu.click()
        time.sleep(1)  # Give time for UI to update

    # Navigate to "Add Recipient" page
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/Add-Recipient')]"))).click()
    print("Navigated to Add Recipient Page")

    # Wait for the recipient name field
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "recipient_name")))

    # Fill the recipient details
    recipient_data = {
        "recipient_name": "Kishore Balaji M",
        "recipient_nick_name": "Kishore",
        "bank_account_number": "625301555643",
        "ifsc_code": "ICIC0006253"
    }

    for field, value in recipient_data.items():
        try:
            input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, field)))
            input_element.clear()
            input_element.send_keys(value)
            print(f"{field} filled successfully")
        except Exception as e:
            print(f"Error filling {field}: {e}")

    # Select the Country (India)
    try:
        country_dropdown = driver.find_element(By.NAME, "country")
        country_dropdown.click()
        india_option = driver.find_element(By.XPATH, "//option[text()='India']")
        india_option.click()
        print("Country selected as India")
    except Exception as e:
        print(f"Error selecting country: {e}")

    # Wait for the submit button to become enabled
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit')]"))
    )

    # Click the Submit button
    if submit_button.is_enabled():
        submit_button.click()
        print("Form Submitted")

        # Wait for 10 seconds to allow processing
        time.sleep(1)

        # Check if a confirmation popup appears
        try:
            confirm_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
            )
            print("Confirmation popup detected! Clicking Confirm...")
            confirm_button.click()
        except:
            print("No confirmation popup appeared. Proceeding...")

        # **LOGOUT PROCESS**
        try:
            # Wait 10 seconds before logging out
            time.sleep(10)

            # Click the dropdown menu first
            dropdown_button = driver.find_element(By.CSS_SELECTOR, "svg.h-5.w-5")
            dropdown_button.click()
            print("Dropdown clicked successfully")

            # Click on Profile/Logout option
            profile_icon = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "menu-item-1"))  # Change this to the actual ID
            )
            profile_icon.click()
            print("Clicked logout option")

            # Wait for 5 seconds before quitting automatically
            time.sleep(5)
            print("Closing browser after 5 seconds...")

        except Exception as e:
            print(f"Error during logout: {e}")

    else:
        print("Submit button is not enabled. Check if all fields are valid.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
