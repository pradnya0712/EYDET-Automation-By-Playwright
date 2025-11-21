from playwright.sync_api import Page
import time
import os
from utils.excel_reader import read_excel_data
import pytest_check as check
import base64
from pytest_html import extras

testdata = read_excel_data(os.getcwd() + "/testdata/" + "TestData.xlsx", "Add_AWB")


class CommonActions:
    def __init__(self, page: Page):
        self.page = page
        self.search_icon = page.locator('//span[text()=" Search "]')
        self.search_screen = page.locator("#menuSearch")

    def set_zoom_level(self, zoom_percent: float):
        zoom_value = zoom_percent / 100
        self.page.wait_for_load_state("load")
        self.page.evaluate(
            f"""
        if (document.body) {{
            document.body.style.zoom = '{zoom_value}';
        }}
        """
        )

    def get_page_title(self):
        self.page.wait_for_timeout(1000)
        title = self.page.evaluate("() => document.title")
        print(f"📄 Page title is: {title}")
        return title

    def scroll_into_view(self, locator):
        locator.scroll_into_view_if_needed()

    def scroll_bottom(self):
        self.page.keyboard.press("End")

    def select_screen(self, screenname: str) -> Page:
        self.search_icon.click()
        self.search_screen.type(screenname)
        self.select_link = self.page.get_by_role("link", name=screenname).first
        self.select_link.click()
        self.page.wait_for_load_state("load")
        return self.page

    def select_dropdown_value(self, selectdropdownlocator, dropdownvalue: str):
        # select tag is not hidden
        selectdropdownlocator.click()
        self.select_option = self.page.locator(
            f'xpath=//option[@value="{dropdownvalue}"]'
        )

    def select_hiddendropdown_value(self, locator, value: str):
        # Get the raw DOM element from Playwright Locator
        element_handle = locator.element_handle()
        if element_handle:
            # Evaluate JavaScript in browser to set dropdown value and trigger change
            self.page.evaluate(
                """([select, value]) => {
                    select.value = value;
                    const event = new Event('change', { bubbles: true });
                    select.dispatchEvent(event);
                }""",
                [element_handle, value],  # Pass both select element and value as list
            )
            print(f"✅ Dropdown value '{value}' selected")
        else:
            print("❌ Could not get element handle for dropdown")

    def eight_digit_AWB(self, awbNo: int):
        modseven = int(awbNo) % 7
        eightdigitAWB = str(awbNo) + str(modseven)
        return eightdigitAWB

    def take_screenshot(self, page_title: str):
        pagetitle = self.get_page_title()
        currentDate = time.strftime("%d-%m-%y")
        currentTime = time.strftime("%I_%M_%S %p")
        timestamp = currentDate + "_" + currentTime
        project_root = os.getcwd()
        basefolderpath = folder_path = os.path.join(
            project_root, "logs", "screenshots", currentDate
        )

        if not os.path.exists(basefolderpath):
            os.makedirs(basefolderpath)

        screenwise_log_folder = os.path.join(basefolderpath, page_title)
        if not os.path.exists(screenwise_log_folder):
            os.makedirs(screenwise_log_folder)

        screenshotName = f"{page_title}_{currentTime}.png"
        screenshotPath = os.path.join(screenwise_log_folder, screenshotName)
        self.page.screenshot(path=screenshotPath)

    @staticmethod
    def soft_assert(page, expected, actual, msg="Soft assertion failed"):
        if expected != actual:

            # Create list if not present
            if not hasattr(page, "_soft_fail_screens"):
                page._soft_fail_screens = []

            # Take ONLY failure screenshot here
            image = page.screenshot()
            page._soft_fail_screens.append(image)

            print(
                f"❌ Soft Assert Failed:\nExpected: {expected}\nActual  : {actual}\nMsg     : {msg}"
            )

            # Mark failure in pytest-check
            check.equal(actual, expected, msg)
