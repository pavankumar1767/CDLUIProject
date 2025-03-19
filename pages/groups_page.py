from pages.base_page import BasePage


class GroupsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def Button_2(self, button_text):
        element_xpath = f"(//span[contains(normalize-space(), '{button_text}')])[2]"
        self.click(element_xpath, f"{button_text}")

    def selectIcon(self, group_name, button_text):
        element_xpath = f"//td[normalize-space()='{group_name}']/parent::tr/td[2]//mat-icon[normalize-space()='{button_text}']"
        self.click(element_xpath, f"{group_name} -> {button_text}")

    def selectAllPermissions(self, module_name):
        element_xpath = f"//h2[contains(normalize-space(),'Permissions')]/ancestor::mat-dialog-container//table/tbody/tr/td[normalize-space()='{module_name}']/parent::tr/td[6]/mat-checkbox"
        self.click(element_xpath, f"{module_name} -> select all permissions")

    def selectAllObjectsList(self, permissions: list):
        for permission in permissions:
            self.selectAllPermissions(permission)


