from pages.viewAWBObjects import ViewAWB
from test_login_page import login
from utils.helpers import CommonActions
from utils.excel_reader import read_excel_data
from utils.config_reader import get_config
import os
import pytest
import time

config = get_config("LoginDetails")
testdata = read_excel_data(os.getcwd() + "/testdata/" + "TestData.xlsx", "View_AWB")


def test_View_AWB_TC2(browser_page):
    page = login(browser_page)
    commonaction = CommonActions(page)

    view_awb = ViewAWB(page)

    # for row in testdata:
    specific_row_index = 1  # 0 = first row after header, 1 = second, 2=third etc.
    if specific_row_index >= len(testdata):
        pytest.skip(f"No row at index {specific_row_index} in Excel data")

    row = testdata[specific_row_index]
    screenName = "View Air Waybill"
    page = commonaction.select_screen(screenName)
    # time.sleep(3)
    pagetitle = commonaction.get_page_title()
    print("---> " + pagetitle)
    view_awb.enter_airline_prefix(row["Airline_Prefix"])
    view_awb.enter_serial_number(commonaction.eight_digit_AWB(row["Serial_Number"]))
    view_awb.expand_additional_search()
    view_awb.select_mop_freight(row["MOP_Freight"])
    view_awb.select_flownstaus(row["Flown_Status"])
    view_awb.select_exportBillingStatus(row["ExportBilling_Status"])
    commonaction.set_zoom_level(60)
    commonaction.take_screenshot(pagetitle)

    view_awb.click_on_search_btn()
    view_awb.expand_additional_search()

    actual_message = view_awb.get_actual_message()
    print(actual_message)
    assert "1 records found" in actual_message, "Please check with valid data"

    view_awb.clear_data()
