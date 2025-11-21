from pages.viewAWBObjects import ViewAWB
from utils.helpers import CommonActions
from utils.excel_reader import read_excel_data
from utils.config_reader import get_config
import os
import pytest
import pytest_check as check

config = get_config("LoginDetails")
testdata = read_excel_data(os.getcwd() + "/testdata/" + "TestData.xlsx", "View_AWB")


def test_View_AWB_TC1(browser_page):
    try:
        # page = login(browser_page)
        page = browser_page
        commonaction = CommonActions(page)
        view_awb = ViewAWB(page)

        # Select row from Excel
        specific_row_index = 0
        if specific_row_index >= len(testdata):
            pytest.skip(f"No row at index {specific_row_index} in Excel data")

        row = testdata[specific_row_index]

        # Navigate to AWB screen
        screenName = "View Air Waybill"
        page = commonaction.select_screen(screenName)

        pagetitle = commonaction.get_page_title()
        print("---> " + pagetitle)

        # Perform search
        awb_number = commonaction.eight_digit_AWB(row["Serial_Number"])
        view_awb.enter_airline_prefix(row["Airline_Prefix"])
        view_awb.enter_serial_number(awb_number)
        view_awb.click_on_search_btn()

        commonaction.take_screenshot(pagetitle)
        # Soft assertion: Validate message
        actual_message = view_awb.get_actual_message()
        expected_message = "0 records found"
        print("Search Result Message:", actual_message)

        CommonActions.soft_assert(
            page,
            expected_message,
            actual_message,
            f"Expected '{expected_message}' but got '{actual_message}'",
        )
        # Zoom & screenshot
        commonaction.set_zoom_level(60)
        commonaction.take_screenshot(pagetitle)

        # Cleanup
        view_awb.clear_data()
        print("Cleared data after test")

    except Exception as e:
        print(f"❌ Exception occurred in test_View_AWB_TC1: {str(e)}")
        pytest.fail(f"Test failed due to exception: {e}")
