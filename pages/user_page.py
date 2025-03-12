from pages.base_page import BasePage


class UserPage(BasePage):
    def __init__(self, page):
        super().__init__(page)


    def Button(self, button_text):
        element_xpath = f"//span[contains(normalize-space(), '{button_text}')]"
        self.click(element_xpath, f"{button_text}")

    def input(self, input_name, text):
        element_xpath = f"//input[@ng-reflect-name='{input_name}']"
        self.fill(element_xpath, text, input_name)

    def select_multiple_mat_options(self, formcontrolname: str, option_texts: list):
        mat_select_locator = f"//mat-select[@formcontrolname='{formcontrolname}']"
        self.page.click(mat_select_locator)
        for option_text in option_texts:
            option_locator = f"//mat-option[normalize-space()='{option_text}']"
            self.page.click(option_locator)
            print(f"Selected '{option_text}'")
        self.page.click("body")
