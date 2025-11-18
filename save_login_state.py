from playwright.sync_api import sync_playwright
import time
from tests.test_login_page import login  # your login() function


def generate_state():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Perform full login + OTP using your existing login() function
        time.sleep(3)
        print("Login is completed successfully")
        login(page, save_state=True)

        print("✔ auth.json has been created successfully.")

        browser.close()


if __name__ == "__main__":
    generate_state()
