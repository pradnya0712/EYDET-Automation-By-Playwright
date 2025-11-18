from pages.addAWBObjects import addAWB
from test_login_page import login
from utils.helpers import CommonActions
from utils.excel_reader import read_excel_data
from utils.config_reader import get_config
import os

import pytest
import pytest_check as check

config = get_config("LoginDetails")
testdata = read_excel_data(os.getcwd() + "/testdata/" + "TestData.xlsx", "Add_AWB")
print("Excel columns:", testdata[0].keys())


def test_Add_AWB_TC1(browser_page):
    try:
        # page = login(browser_page)
        page = browser_page
        commonaction = CommonActions(page)

        add_awb = addAWB(page)

        # for row in testdata:

        # Target a specific row (e.g., second row after header)
        specific_row_index = 0  # 0 = first row after header, 1 = second, etc.
        if specific_row_index >= len(testdata):
            pytest.skip(f"No row at index {specific_row_index} in Excel data")

        row = testdata[specific_row_index]
        screenName = "Add Air Waybill"
        page = commonaction.select_screen(screenName)

        pagetitle = commonaction.get_page_title()
        print("---> " + pagetitle)
        commonaction.set_zoom_level(60)
        add_awb.enter_airline_prefix(row["Airline_Prefix"])
        add_awb.enter_serial_number(row["Serial_Number"])
        add_awb.enter_issue_date(row["Issue_Date"])
        add_awb.enter_city_of_sale(row["City_Of_Sale"])
        add_awb.select_mop_frieght(row["MOP_Freight"])
        add_awb.enter_currency(row["Currency"])
        add_awb.enter_commodity_name(row["Commodity"])

        commonaction.take_screenshot(pagetitle)

        add_awb.enter_shipper_name(row["Shipper"])
        add_awb.enter_consignee_name(row["Consignee"])
        add_awb.enter_agent_code(row["Selling_Location"])
        add_awb.click_on_add_routing_info_icon()
        add_awb.enter_from_airport(row["Origin"])
        add_awb.enter_to_airport(row["Destination"])
        add_awb.enter_carrier(row["Carrier"])

        commonaction.take_screenshot(pagetitle)

        add_awb.click_on_add_chargelineinfo_icon()
        add_awb.enter_no_of_pieces(row["No_Of_Pieces"])
        add_awb.select_unit_of_weight(row["Unit_Of_Weight"])
        add_awb.enter_gross_weight(row["Gross_Weight"])
        add_awb.enter_rate_class(row["Rate_Class"])
        add_awb.enter_chargeable_weight(row["Chargeable_Weight"])
        add_awb.enter_rate(row["Rate"])
        commonaction.take_screenshot(pagetitle)
        add_awb.enter_discount(row["Discount"])
        add_awb.enter_commission(row["Commission"])

        commonaction.take_screenshot(pagetitle)

        add_awb.click_on_expand_other_charge_icon()
        add_awb.click_on_add_other_charges_icon()
        add_awb.select_mop_other_charge(row["MOP_Other_Charge"])
        add_awb.enter_othercharge_code(row["Other_Charge_Code"])
        add_awb.enter_othercharge_code_amount(row["Other_Charge_Code_Amount"])
        # add_awb.enter_OCDC_amount_in_TotalCharges(row["Other_Charge_Code_Amount"])

        commonaction.take_screenshot(pagetitle)

        # add_awb.click_on_expan_additionalDetaisl()
        # add_awb.enter_flight_from_sector(row["Flight_from_Airport"])
        # add_awb.enter_flight_to_sector(row["Flight_to_Airport"])
        # add_awb.enter_flight_number(row["Flight_Number"])
        # add_awb.enter_flight_date(row["Flight_Date"])
        add_awb.click_on_save_btn()
        print("Click on save btn")

        commonaction.take_screenshot(pagetitle)

        message = add_awb.get_message_on_awb_save()
        awbNum = commonaction.eight_digit_AWB(row["Serial_Number"])
        print(message)
        expected_message = (
            "AWB - "
            + str(row["Airline_Prefix"])
            + " "
            + str(awbNum)
            + " successfully validated."
        )
        check.is_in(
            message,
            expected_message,
            "AWB - "
            + str(row["Airline_Prefix"])
            + " "
            + str(awbNum)
            + " is not save. Please check logs.",
        )
        add_awb.click_on_close_popup_message()
        print("Click on close popup icon")

        add_awb.scroll_down()
        commonaction.take_screenshot(pagetitle)
        add_awb.click_on_cancel_btn()
        print("Click on cancel btn")

    except Exception as e:
        # Properly catch and print exceptions
        print(f"❌ Exception occurred in test_Add_AWB_TC1: {str(e)}")
        pytest.fail(f"Test failed due to exception: {e}")
