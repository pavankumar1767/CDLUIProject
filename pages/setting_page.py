import time

from pages.base_page import BasePage


class SettingPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def select_tab(self, tabname):
        element_xpath = f"//div[@role='tab']/div[normalize-space()='{tabname}']"
        self.click(element_xpath, f"{tabname}")



    def input_url(self, url):
        element_xpath = "//input[@ng-reflect-id='url']"
        self.fill(element_xpath, url, "url")

    def input(self, name, text):
        element_xpath = f"//input[@ng-reflect-name='{name}']"
        self.fill(element_xpath,text , f"{text}")



    def select_checkbox(self, field):
        time.sleep(3)
        checkbox_xpath = f"//mat-checkbox[@formcontrolname='{field}']//input[@type='checkbox']"
        clickable_xpath = f"//mat-checkbox[@formcontrolname='{field}']"
        self.page.wait_for_selector(checkbox_xpath)
        aria_checked = self.page.locator(checkbox_xpath).get_attribute("aria-checked")
        if aria_checked == "true":
            self.click(clickable_xpath, f"{field} - Unchecking")
            self.click(clickable_xpath, f"{field} - Rechecking")
        else:
            self.click(clickable_xpath, f"{field} - Checking")


