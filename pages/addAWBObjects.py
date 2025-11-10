from playwright.sync_api import Page
from utils.helpers import CommonActions
from datetime import date
from utils.helpers import CommonActions
import time


class addAWB:
    def __init__(self, page: Page):
        self.page = page
        self.common = CommonActions(page)

        self.airline_prefix = self.page.locator("#addAirWaybillForm_actcarnumcod")
        self.serial_number = self.page.locator("#docnum")
        self.issue_date = self.page.locator("#issdat")
        self.city_of_Sale = self.page.locator("#addAirWaybillForm_issctycod")
        self.mop_freight = self.page.locator("#addAirWaybillForm_mopfrtchg")  # dropdown
        self.currency = self.page.locator("#addAirWaybillForm_curcod")
        self.commodity_name = self.page.locator("#cmdnam")
        self.shipper_name = self.page.locator("#shpnam")
        self.consignee_name = self.page.locator("#cnenam")
        self.location_code = self.page.locator("#addAirWaybillForm_loccod")
        self.add_routing_icon = self.page.locator("#add_routingEditableTable")
        self.from_airport = self.page.locator("#arpcod_0")
        self.to_airport = self.page.locator("#toarpcod_0")
        self.carrier = self.page.locator("#carnumcod_0")
        self.add_chargelineinfo_icon = self.page.locator("#add_chargeLineEditableTable")
        self.no_of_pieces = self.page.locator("#numpcs")
        self.unit_of_weight = self.page.locator("#untwgtind")
        self.gross_weight = self.page.locator("#grswgt")
        self.rate_class = self.page.locator("#ratclscod_0")
        self.chargeable_weight = self.page.locator("#chgwgt")
        self.rate = self.page.locator("#ratval")
        self.discount = self.page.locator("#dscamt")
        self.commission = self.page.locator("#comamt")
        self.expand_othercharges_icon = self.page.locator("#OtherCharge_span")
        self.mop_othercharge = self.page.locator("#addAirWaybillForm_mopothchgJQ")
        self.add_othercharges_icon = self.page.locator("#add_otherChargeEditableTable")
        self.othercharge_code = self.page.locator("#othchgcod_0")
        self.othercharge_amount = self.page.locator("#chgAmtOthChg")
        # self.ocdcamount_in_totalCharges = self.page.locator("#ocdcar")
        self.expand_additionalDetails = self.page.locator("#additionaDetailsDiv_a")
        self.flighatDetails_fromSector = self.page.locator(
            "#addAirWaybillForm_fstfrmarpcod"
        )
        self.flighatDetails_toSector = self.page.locator(
            "#addAirWaybillForm_fsttooarpcod"
        )
        self.flightNumber = self.page.locator("#fstfltnum")
        self.flightDate = self.page.locator("#fstfltdat")

        self.saveBtn = self.page.locator(
            "//*[@id='addAirWaybillForm_downCommitButton']"
        )
        self.getSuccess_messsage = self.page.locator("#pageInformationMsgDiv")
        self.getError_message = self.page.locator("#pageErrorMsgDiv")
        self.close_message_popup = self.page.locator("#closeButton")
        self.cancelBtn = self.page.locator("#addAirWaybillForm_downCancelBtn")

    def enter_airline_prefix(self, airlineprefix: str):
        time.sleep(3)
        self.airline_prefix.fill(airlineprefix)

    def enter_serial_number(self, serialnumber: int):
        self.serial_number.fill(str(serialnumber))

    def enter_issue_date(self, issuedate: date):
        self.issue_date.fill(str(issuedate))

    def enter_city_of_sale(self, cityofsale: str):
        self.city_of_Sale.fill(cityofsale)

    def select_mop_frieght(self, value: str):
        self.common.select_hiddendropdown_value(self.mop_freight, value)

    def enter_currency(self, curr: str):
        self.currency.fill(curr)

    def enter_commodity_name(self, commodityname: str):
        self.commodity_name.fill(commodityname)

    def enter_shipper_name(self, shippername: str):
        self.shipper_name.fill(shippername)

    def enter_consignee_name(self, consigneename: str):
        self.consignee_name.fill(consigneename)

    def enter_agent_code(self, slcode: int):
        self.location_code.fill(str(slcode))

    def click_on_add_routing_info_icon(self):
        self.add_routing_icon.click()

    def enter_from_airport(self, fromairport: str):
        self.from_airport.fill(fromairport)

    def enter_to_airport(self, toairport: str):
        self.to_airport.fill(toairport)

    def enter_carrier(self, Carrier: str):
        self.carrier.wait_for(state="visible")
        self.carrier.click()
        time.sleep(2)
        self.carrier.type(Carrier)

    def click_on_add_chargelineinfo_icon(self):
        self.add_chargelineinfo_icon.click()

    def enter_no_of_pieces(self, pieces: int):
        self.no_of_pieces.clear()
        self.no_of_pieces.fill(str(pieces))

    def select_unit_of_weight(self, unitofweight: str):

        self.common.select_hiddendropdown_value(self.unit_of_weight, unitofweight)

    def enter_gross_weight(self, grossweight: int):
        self.gross_weight.clear()
        self.gross_weight.fill(str(grossweight))

    def enter_rate_class(self, rateclass: str):
        self.rate_class.clear()
        self.rate_class.fill(rateclass)

    def enter_chargeable_weight(self, chargeableweight: int):
        self.chargeable_weight.clear()
        self.chargeable_weight.fill(str(chargeableweight))

    def enter_rate(self, rate: int):
        self.rate.wait_for(state="visible")
        self.rate.click()
        self.rate.press("Control+A")
        self.rate.press("Backspace")
        time.sleep(2)
        self.rate.fill(str(rate))

    def enter_discount(self, discount: int):
        self.discount.fill(str(discount))

    def enter_commission(self, commission: int):
        self.commission.fill(str(commission))

    def click_on_expand_other_charge_icon(self):
        self.expand_othercharges_icon.click()

    def click_on_add_other_charges_icon(self):
        self.add_othercharges_icon.click()

    def select_mop_other_charge(self, mopvalue: str):
        self.mop_othercharge.click()
        self.common.select_hiddendropdown_value(self.mop_othercharge, mopvalue)

    def enter_othercharge_code(self, otherchargecode: str):
        self.othercharge_code.click()
        self.othercharge_code.fill(otherchargecode)

    def enter_othercharge_code_amount(self, otherchargecodeAmount: int):
        self.othercharge_amount.fill(str(otherchargecodeAmount))

    def enter_OCDC_amount_in_TotalCharges(self, ocdc_Amt: int):
        self.ocdcamount_in_totalCharges.click()
        self.ocdcamount_in_totalCharges.clear()
        self.ocdcamount_in_totalCharges.fill(str(ocdc_Amt))

    def click_on_expan_additionalDetaisl(self):
        self.expand_additionalDetails.click()

    def enter_flight_number(self, flightnum: str):
        self.flightNumber.fill(str(flightnum))

    def enter_flight_date(self, flightdate: str):
        self.flightDate.fill(str(flightdate))

    def enter_flight_from_sector(self, fromsector: str):
        self.flighatDetails_fromSector.fill(fromsector)

    def enter_flight_to_sector(self, tosector: str):
        self.flighatDetails_toSector.fill(tosector)

    def click_on_save_btn(self):
        self.saveBtn.scroll_into_view_if_needed()
        self.saveBtn.click()

    def get_message_on_awb_save(self):
        if self.getError_message.is_visible():
            self.errormessage = self.getError_message.inner_text()
            return self.errormessage
        else:
            self.successmessage = self.getSuccess_messsage.inner_text()
            return self.successmessage

    def click_on_close_popup_message(self):
        self.close_message_popup.click()

    def scroll_down(self):
        self.cancelBtn.scroll_into_view_if_needed()

    def click_on_cancel_btn(self):
        self.cancelBtn.click()
