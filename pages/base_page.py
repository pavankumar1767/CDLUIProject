# from playwright.sync_api import Page
#
#
# class BasePage:
#     def __init__(self, page: Page):
#         self.page = page
#
#
#     def navigate(self, url):
#         self.page.goto(url)
#
#
#     def click(self, selector):
#         self.page.click(selector)
#
#
#     def fill(self, selector, text):
#         self.page.fill(selector, text)
#
#
#     def get_text(self, selector):
#         return self.page.inner_text(selector)
#
#
#     def wait_for_selector(self, selector):
#         self.page.wait_for_selector(selector)












# base_page.py
from playwright.sync_api import Page
import allure
import logging
from utilities.logger import setup_logger

logger = setup_logger()

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url):
        log_message = f"Navigating to URL: {url}"
        logger.info(log_message)
        self._attach_log_to_allure(log_message)
        self.page.goto(url)
        self._capture_screenshot("After Navigation")

    def click(self, selector, element_name="Element"):
        log_message = f"Clicking on element: {element_name}"
        logger.info(log_message)
        self._attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        self.page.click(selector)
        self._capture_screenshot(f"After Clicking {element_name}")

    def fill(self, selector, text, element_name="Element"):
        log_message = f"Filling text '{text}' into element: {element_name}"
        logger.info(log_message)
        self._attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        self.page.fill(selector, text)
        self._capture_screenshot(f"After Filling {text} into element: {element_name}")

    def get_text(self, selector, element_name="Element"):
        log_message = f"Retrieving text from element: {element_name}"
        logger.info(log_message)
        self._attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        text = self.page.inner_text(selector)
        self._capture_screenshot(f"After Retrieving Text from {element_name}")
        return text

    def wait_for_selector(self, selector):
        log_message = f"Waiting for element: {selector}"
        logger.info(log_message)
        self._attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        self._capture_screenshot(f"After Waiting for {selector}")

    def _capture_screenshot(self, description):
        try:
            screenshot = self.page.screenshot(full_page=True)
            allure.attach(screenshot, name=description, attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")

    def _attach_log_to_allure(self, log_message):
        allure.attach(log_message, name="Log", attachment_type=allure.attachment_type.TEXT)