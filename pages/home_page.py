import random

from playwright.sync_api import expect
from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def select_module(self, module_name):
        element_xpath = f"//li[@ng-reflect-router-link='{module_name}']"
        self.click(element_xpath, f"{module_name}")

