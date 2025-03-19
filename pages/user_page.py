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

    def selectRoles(self, formcontrolname: str, option_texts: list):
        mat_select_locator = f"//mat-select[@formcontrolname='{formcontrolname}']"
        self.page.click(mat_select_locator)
        for option_text in option_texts:
            option_locator = f"//mat-option[normalize-space()='{option_text}']"
            self.page.click(option_locator)
            print(f"Selected '{option_text}'")
        self.page.keyboard.press("Escape")

    def selectUser(self, username, button):
        element_xpath = f"//td[normalize-space()='{username}']/parent::tr/td[4]//mat-icon[normalize-space()='{button}']"
        self.click(element_xpath, f"{username} -> {button}")

    def search(self, text):
        element_xpath = "//mat-label[normalize-space()='Search']/ancestor::div//input"
        self.fill(element_xpath,text,f"{text}")

    def getEmail(self, username):
        element_xpath = f"//td[normalize-space()='{username}']/parent::tr/td[3]"
        return self.get_text(element_xpath, f"{username} email")

