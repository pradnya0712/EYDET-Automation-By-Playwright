from pages.viewAWBObjects import ViewAWB
from test_login_page import login
from utils.helpers import CommonActions
from utils.excel_reader import read_excel_data
from utils.config_reader import get_config
import os
import pytest

config = get_config("LoginDetails")
testdata = read_excel_data(os.getcwd() + "/testdata/" + "TestData.xlsx", "View_AWB")


def test_View_AWB_TC3(browser_page):
    # page = login(browser_page)
    page = browser_page
    commonaction = CommonActions(page)

    view_awb = ViewAWB(page)

    # for row in testdata:
    specific_row_index = 2  # 0 = first row after header, 1 = second, 2=third etc.
    if specific_row_index >= len(testdata):
        pytest.skip(f"No row at index {specific_row_index} in Excel data")

    row = testdata[specific_row_index]
    screenName = "View Air Waybill"
    page = commonaction.select_screen(screenName)

    pagetitle = commonaction.get_page_title()
    print("---> " + pagetitle)
    view_awb.enter_airline_prefix(row["Airline_Prefix"])
    view_awb.enter_serial_number(commonaction.eight_digit_AWB(row["Serial_Number"]))
    view_awb.click_on_search_btn()
    commonaction.take_screenshot(pagetitle)

    actual_message = view_awb.get_actual_message()
    print(actual_message)
    assert "1 records found" in actual_message, "Please check with valid data"
    view_awb.select_awb_record()
    commonaction.set_zoom_level(60)
    commonaction.take_screenshot(pagetitle)

    view_awb.click_on_detail_link()
    details_serialnumber = view_awb.get_serial_number_text()
    assert str(row["Serial_Number"]) in details_serialnumber, "please check the logs"
    commonaction.set_zoom_level(60)
    commonaction.take_screenshot(pagetitle)

    commonaction.scroll_into_view(view_awb.scroll_toward_total_charges)

    commonaction.take_screenshot(pagetitle)
    commonaction.scroll_into_view(view_awb.scroll_toward_close_btn)
    commonaction.take_screenshot(pagetitle)
    view_awb.click_on_close_btn()

    view_awb.click_on_proration_link()
    proration_serialnumber = view_awb.get_serial_number_text()
    assert str(row["Serial_Number"]) in proration_serialnumber, "please check the logs"
    commonaction.set_zoom_level(60)
    commonaction.take_screenshot(pagetitle)

    view_awb.close_open_tab()
    view_awb.click_on_flown_link()
    flown_serialnumber = view_awb.get_flown_details_document_number()
    assert str(row["Serial_Number"]) in flown_serialnumber, "please check the logs"
    commonaction.set_zoom_level(60)
    commonaction.take_screenshot(pagetitle)

    view_awb.close_open_tab()
    view_awb.click_on_sector_link()
    sector_serialnumber = view_awb.get_serial_number_text()
    assert str(row["Serial_Number"]) in sector_serialnumber, "please check the logs"
    commonaction.set_zoom_level(60)
    commonaction.take_screenshot(pagetitle)

    view_awb.close_open_tab()
    view_awb.clear_data()
