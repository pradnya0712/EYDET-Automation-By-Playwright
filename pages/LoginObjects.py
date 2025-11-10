from playwright.sync_api import Page
import time


class SsoLoginObjects:
    def __init__(self, page: Page):
        self.page = page
        self.username = self.page.locator("#userName")
        self.password = self.page.locator("#password")
        self.loginBtn = self.page.locator("#loginForm_login")
        self.submitOTP = self.page.locator("#multiAuthForm_submitOTP")

    def enter_username(self, username: str):
        self.username.fill(username)

    def enter_password(self, password: str):
        self.password.fill(password)

    def click_on_login_btn(self):
        self.loginBtn.click()
        time.sleep(5)

        self.accept_popup = self.page.locator(
            "#sessionConfirmAlertForm_sessionYesButton"
        )
        try:
            self.accept_popup.wait_for(state="visible", timeout=1000)
            self.accept_popup.click()
            time.sleep(30)  # wait after popup click if needed
        except:
            pass  # popup not present

            time.sleep(60)  # wait for next steps (optional)

    def click_on_submit_otp_btn(self):
        self.submitOTP.click()
