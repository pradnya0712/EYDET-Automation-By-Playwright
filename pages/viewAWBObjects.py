from playwright.sync_api import Page
from utils.helpers import CommonActions


class ViewAWB:
    def __init__(self, page: Page):
        self.page = page
        self.common = CommonActions(page)
        self._init_locators()

    def _init_locators(self):
        self.airline_prefix = self.page.locator("#airwayForm_carnumcod")
        self.serial_number = self.page.locator("#docnum")

        self.additinal_search_link = self.page.locator("#AdditionalSearchCriteria")
        self.select_mopfreight_dropdown = self.page.locator("#mopfrtchg")
        self.select_flownstatus_dropdown = self.page.locator("#flownStatus")
        self.select_exportstatus_dropdown = self.page.locator("#exportStatus")

        self.search_btn = self.page.locator("#airwayForm_searchBtn")
        self.actual_awb_count_message = self.page.locator(
            '(//span[contains(text(), " records found")])[2]'
        )

        self.select_record = self.page.locator("#listSectionTable_Select_0")
        self.scroll_toward_total_charges = self.page.locator("#totalChargesDiv_a")
        self.scroll_toward_close_btn = self.page.locator('//button[@name="closeBtn"]')
        self.detail_link = self.page.locator("#airwayForm_detailsBtn")
        self.proration_link = self.page.locator("#airwayForm_prorationBtn")
        self.flown_link = self.page.locator("#airwayForm_flownBtn")
        self.sector_link = self.page.locator("#airwayForm_sectorBtn")
        self.close_tab = self.page.locator('//*[@title="Close Tab"]')
        self.clear_btn = self.page.locator('//*[@id="airwayForm_clearBtn"]')
        self.get_flown_detail_serial_number = self.page.locator(
            '//*[@id="docnumAwbNo"]'
        )

    def enter_airline_prefix(self, airlineprefix: int):
        self.airline_prefix.fill(str(airlineprefix))

    def enter_serial_number(self, serialnumber: int):
        self.serial_number.fill(str(serialnumber))

    def expand_additional_search(self):
        self.additinal_search_link.click()

    def select_mop_freight(self, mopfreight: str):
        self.common.select_hiddendropdown_value(
            self.select_mopfreight_dropdown, mopfreight
        )

    def select_flownstaus(self, flownstatus: str):
        self.common.select_hiddendropdown_value(
            self.select_flownstatus_dropdown, flownstatus
        )

    def select_exportBillingStatus(self, exportstatus: str):
        self.common.select_hiddendropdown_value(
            self.select_exportstatus_dropdown, exportstatus
        )

    def enter_serial_number(self, serialnumber: int):
        self.serial_number.fill(str(serialnumber))

    def click_on_search_btn(self):
        self.search_btn.click()

    def get_actual_message(self):
        self.actual_awb_message_count = self.actual_awb_count_message.text_content()
        return self.actual_awb_message_count

    def select_awb_record(self):
        if not self.select_record.is_checked():
            self.select_record.check()
        else:
            for i in range(1, 3):  # loops for i = 1 and 2
                self.select_record.check()

    def click_on_detail_link(self):
        self.detail_link.click()

    def click_on_proration_link(self):
        self.proration_link.click()

    def click_on_flown_link(self):
        self.flown_link.click()

    def click_on_sector_link(self):
        self.sector_link.click()

    def get_serial_number_text(self):
        self.serialnumber = self.serial_number.input_value()
        return self.serialnumber

    def get_flown_details_document_number(self):
        self.get_serial_number = self.get_flown_detail_serial_number.input_value()
        return self.get_serial_number

    def click_on_close_btn(self):
        self.scroll_toward_close_btn.click()

    def close_open_tab(self):
        self.close_tab.click()

    def clear_data(self):
        self.clear_btn.click()
