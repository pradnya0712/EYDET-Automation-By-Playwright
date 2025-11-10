from utils.config_reader import get_config
from pages.LoginObjects import SsoLoginObjects
from utils.helpers import CommonActions

config = get_config("LoginDetails")


def login(browser_page):
    page = browser_page
    commonaction = CommonActions(page)
    pagetitle = commonaction.get_page_title()
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
    commonaction.take_screenshot(pagetitle)
    loginObject.click_on_login_btn()
    # loginObject.click_on_submit_otp_btn()
    commonaction.take_screenshot(pagetitle)

    return page
