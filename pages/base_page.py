import time
from playwright.sync_api import Page
import allure
import logging
from utilities.logger import setup_logger
from utilities.FrameworkConfig import FrameworkConfig  # Import your configuration

logger = setup_logger()


def _attach_log_to_allure(log_message):
    allure.attach(log_message, name="Log", attachment_type=allure.attachment_type.TEXT)


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url):
        log_message = f"Navigating to URL: {url}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        self.page.goto(url)
        self._capture_screenshot("After Navigation")

    def click(self, selector, element_name="Element"):
        log_message = f"Clicking on element: {element_name}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        self.page.click(selector)
        self._capture_screenshot(f"After Clicking {element_name}")

    def fill(self, selector, text, element_name="Element"):
        log_message = f"Filling text '{text}' into element: {element_name}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        self.page.fill(selector, text)
        self._capture_screenshot(f"After Filling {text} into element: {element_name}")

    def get_text(self, selector, element_name="Element"):
        log_message = f"Retrieving text from element: {element_name}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        time.sleep(5)
        text = self.page.locator(selector).text_content()
        self._capture_screenshot(f"{text} Text Retrieved from {element_name}")
        return text.strip()

    def wait_for_selector(self, selector):
        log_message = f"Waiting for element: {selector}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        self._capture_screenshot(f"After Waiting for {selector}")

    def select_from_dropdown(self, selector, value, element_name="Dropdown"):
        log_message = f"Selecting value '{value}' from dropdown: {element_name}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        self.page.select_option(selector, value)
        self._capture_screenshot(f"After Selecting {value} from {element_name}")

    def handle_alert(self, accept=True, prompt_text=None):
        action = "accepting" if accept else "dismissing"
        log_message = f"{action.capitalize()} alert"
        if prompt_text:
            log_message += f" with prompt text: {prompt_text}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        if prompt_text:
            self.page.on('dialog', lambda dialog: dialog.accept(prompt_text))
        else:
            self.page.on('dialog', lambda dialog: dialog.accept() if accept else dialog.dismiss())
        self._capture_screenshot(f"After {action} Alert")

    def upload_file(self, selector, file_path, element_name="File Input"):
        log_message = f"Uploading file '{file_path}' to element: {element_name}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        self.page.set_input_files(selector, file_path)
        self._capture_screenshot(f"After Uploading File to {element_name}")

    def download_file(self, selector, download_path, element_name="Download Link"):
        log_message = f"Downloading file from element: {element_name} to {download_path}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        with self.page.expect_download() as download_info:
            self.page.click(selector)
        download = download_info.value
        download.save_as(download_path)
        self._capture_screenshot(f"After Downloading File from {element_name}")

    # Action Methods
    def hover(self, selector, element_name="Element"):
        log_message = f"Hovering over element: {element_name}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        self.page.hover(selector)
        self._capture_screenshot(f"After Hovering over {element_name}")

    def double_click(self, selector, element_name="Element"):
        log_message = f"Double-clicking on element: {element_name}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        self.page.dblclick(selector)
        self._capture_screenshot(f"After Double-Clicking {element_name}")

    def right_click(self, selector, element_name="Element"):
        log_message = f"Right-clicking on element: {element_name}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        self.page.click(selector, button="right")
        self._capture_screenshot(f"After Right-Clicking {element_name}")

    def drag_and_drop(self, source_selector, target_selector, source_name="Source Element",
                      target_name="Target Element"):
        log_message = f"Dragging element: {source_name} and dropping onto element: {target_name}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        self.page.wait_for_selector(source_selector)
        self.page.wait_for_selector(target_selector)
        self.page.drag_and_drop(source_selector, target_selector)
        self._capture_screenshot(f"After Dragging {source_name} and Dropping onto {target_name}")

    def scroll_to_element(self, selector, element_name="Element"):
        log_message = f"Scrolling to element: {element_name}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        self.page.wait_for_selector(selector)
        self.page.locator(selector).scroll_into_view_if_needed()
        self._capture_screenshot(f"After Scrolling to {element_name}")

    def press_key(self, key):
        log_message = f"Pressing key: {key}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        self.page.keyboard.press(key)
        self._capture_screenshot(f"After Pressing Key: {key}")

    def select_checkbox(self, selector, element_name="Checkbox"):
        log_message = f"Selecting checkbox: {element_name}"
        logger.info(log_message)
        _attach_log_to_allure(log_message)
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=60000)
            if not self.page.is_checked(selector):
                self.page.check(selector)
                logger.info(f"Checkbox '{element_name}' selected successfully.")
            else:
                logger.info(f"Checkbox '{element_name}' is already selected.")
            self._capture_screenshot(f"After Selecting Checkbox: {element_name}")
        except Exception as e:
            logger.error(f"Failed to select checkbox '{element_name}': {e}")
            self._capture_screenshot(f"Error Selecting Checkbox: {element_name}")
            raise e

    def _capture_screenshot(self, description):
        """
        Captures a screenshot and attaches it to the Allure report if screenshots are enabled in the configuration.
        """
        try:
            # Check if screenshots are enabled for pass/fail cases
            if (FrameworkConfig.LoggerScreenshot_ON_PASS == "yes" and not hasattr(self, "_test_failed")) or (
                    FrameworkConfig.LoggerScreenshot_ON_FAIL == "yes" and hasattr(self, "_test_failed")):
                screenshot = self.page.screenshot(full_page=True)
                allure.attach(screenshot, name=description, attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")


