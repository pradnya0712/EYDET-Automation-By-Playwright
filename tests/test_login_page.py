from utils.config_reader import get_config
from pages.LoginObjects import SsoLoginObjects
from utils.helpers import CommonActions
from playwright.sync_api import TimeoutError  # <-- REQUIRED

config = get_config("LoginDetails")


def login(browser_page, save_state=False):
    page = browser_page
    commonaction = CommonActions(page)
    context = page.context

    page.goto(config["base_url"])
    print("\nBrowser launched successfully")
    print(f"Page title: {page.title()}")
    print(f"Current page URL: {page.url}")

    assert (
        "EK DET Environment - Login" in page.title()
    ), "title does not match with expected title"

    loginObject = SsoLoginObjects(page)

    loginObject.enter_username(config["username"])
    loginObject.enter_password(config["password"])
    loginObject.click_on_login_btn()

    # OTP screen is handled inside your POM method
    # loginObject.click_on_submit_otp_btn()

    print("➡ Waiting for home page after OTP...")
    try:
        page.wait_for_url("**/CRA/home*", timeout=120000)
        print("✔ Login successful — Home page loaded.")
    except TimeoutError:
        print("❌ OTP failed or login error!")
        raise

    if save_state:
        context.storage_state(path="auth.json")
        print("Login state saved to auth.json")

    return page
