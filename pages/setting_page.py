import time

import allure

from pages.base_page import BasePage, logger



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

    def clear_input_text(self, name):
        element_xpath = f"//input[@ng-reflect-name='{name}']"
        input_element = self.page.locator(element_xpath)
        input_element.clear()



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

    def assert_url_filed_error(self, text):
        log_message = f"Asserting field level error: {text}"
        logger.info(log_message)
        allure.attach(log_message, name="error Assertion Log", attachment_type=allure.attachment_type.TEXT)

        popup_locator = self.page.get_by_text(text)
        popup_locator.wait_for(state="visible", timeout=10000)  # 10 seconds timeout
        popup_text = popup_locator.text_content()

        allure.attach(popup_text, name="error Text", attachment_type=allure.attachment_type.TEXT)
        self._capture_screenshot("error Displayed")

        assert text == popup_text, f"Expected error text: '{text}', but got: '{popup_text}'"



