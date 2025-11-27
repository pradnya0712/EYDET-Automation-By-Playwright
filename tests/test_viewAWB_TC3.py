import pytest
import pytest_check as check
import os
from pages.viewAWBObjects import ViewAWB
from utils.helpers import CommonActions
from utils.excel_reader import read_excel_data
from utils.config_reader import get_config

config = get_config("LoginDetails")
testdata = read_excel_data(os.getcwd() + "/testdata/" + "TestData.xlsx", "View_AWB")


@pytest.mark.view_awb
def test_View_AWB_TC3(browser_page):
    try:
        # page = login(browser_page)
        page = browser_page
        commonaction = CommonActions(page)
        view_awb = ViewAWB(page)

        specific_row_index = 2
        if specific_row_index >= len(testdata):
            pytest.skip(f"No row at index {specific_row_index} in Excel data")

        row = testdata[specific_row_index]

        # Navigate to screen
        screenName = "View Air Waybill"
        page = commonaction.select_screen(screenName)
        pagetitle = commonaction.get_page_title()
        print("---> " + pagetitle)

        # Search
        awb_number = commonaction.eight_digit_AWB(row["Serial_Number"])
        view_awb.enter_airline_prefix(row["Airline_Prefix"])
        view_awb.enter_serial_number(awb_number)
        view_awb.click_on_search_btn()
        commonaction.take_screenshot(pagetitle)

        # Soft assertion: record count
        actual_message = view_awb.get_actual_message()
        print("Search Result Message:", actual_message)

        actual_message = view_awb.get_actual_message()
        expected_message = " 1 records found"
        print("Search Result Message:", actual_message)

        CommonActions.soft_assert(
            page,
            expected_message,
            actual_message,
            f"Expected '{expected_message}' but got '{actual_message}'",
        )
        # Select record
        view_awb.select_awb_record()
        commonaction.set_zoom_level(60)
        commonaction.take_screenshot(pagetitle)

        # DETAILS TAB
        view_awb.click_on_detail_link()
        details_serial = view_awb.get_serial_number_text()
        CommonActions.soft_assert(
            page,
            awb_number,
            details_serial,
            "Serial number mismatch in Details tab",
        )

        commonaction.set_zoom_level(60)
        commonaction.take_screenshot(pagetitle)
        commonaction.scroll_into_view(view_awb.scroll_toward_total_charges)

        commonaction.take_screenshot(pagetitle)
        commonaction.scroll_into_view(view_awb.scroll_toward_close_btn)
        view_awb.click_on_close_btn()

        # PRORATION TAB
        view_awb.click_on_proration_link()

        proration_serial = view_awb.get_serial_number_text()
        CommonActions.soft_assert(
            page,
            awb_number,
            proration_serial,
            "Serial number mismatch in Proration tab",
        )
        commonaction.set_zoom_level(60)
        commonaction.take_screenshot(pagetitle)
        view_awb.close_open_tab()

        # FLOWN TAB
        view_awb.click_on_flown_link()
        flown_serial = view_awb.get_flown_details_document_number()
        CommonActions.soft_assert(
            page,
            awb_number,
            flown_serial,
            "Serial number mismatch in Flown tab",
        )
        commonaction.set_zoom_level(60)
        commonaction.take_screenshot(pagetitle)
        view_awb.close_open_tab()

        # SECTOR TAB
        view_awb.click_on_sector_link()
        sector_serial = view_awb.get_serial_number_text()
        CommonActions.soft_assert(
            page,
            awb_number,
            sector_serial,
            "Serial number mismatch in Sector tab",
        )
        commonaction.set_zoom_level(60)
        commonaction.take_screenshot(pagetitle)
        view_awb.close_open_tab()

        # Cleanup
        view_awb.clear_data()
        print("Test completed successfully and cleaned up.")

    except Exception as e:
        print(f"❌ Exception occurred in test_View_AWB_TC3: {str(e)}")
        pytest.fail(f"Test failed due to exception: {e}")
