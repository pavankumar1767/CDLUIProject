# import pytest
# from playwright.sync_api import sync_playwright
# from utilities.config import Config
#
#
# @pytest.fixture(scope="function")
# def setup():
#     with sync_playwright() as p:
#         browser = p[Config.BROWSER].launch(headless=Config.HEADLESS)
#         page = browser.new_page()
#         yield page
#         browser.close()








#
#
#
#
#
#
# # conftest.py
# import pytest
# import allure
# import os
# import logging
# from playwright.sync_api import sync_playwright
# from utilities.config import Config
#
# logger = logging.getLogger(__name__)
#
# @pytest.fixture(scope="function")
# def setup(request):
#     with sync_playwright() as p:
#         # Define browser arguments
#         browser_args = [
#             "--ignore-certificate-errors",  # Ignore certificate errors
#             "--disable-notifications",  # Disable notifications
#             "--disable-infobars",  # Disable infobars (e.g., "Chrome is being controlled by automated test software")
#         ]
#
#         # Launch the browser with arguments
#         browser = p[Config.BROWSER].launch(
#             headless=Config.HEADLESS,
#             args=browser_args  # Pass browser arguments
#         )
#         os.makedirs("videos", exist_ok=True)
#
#         # Create a new context with video recording enabled
#         context = browser.new_context(record_video_dir="videos/")
#
#         # Create a new page
#         page = context.new_page()
#         page.set_default_timeout(60000)
#         yield page  # Provide the page to the test
#
#         # Close the context to release the video file
#         context.close()
#         browser.close()
#
#         # Attach video for all test cases (both passed and failed)
#         video_path = page.video.path()
#         if video_path and os.path.exists(video_path):
#             try:
#                 # Attach the video to the Allure report
#                 with open(video_path, "rb") as video_file:
#                     video_data = video_file.read()
#                 allure.attach(video_data, name="Execution Video", attachment_type=allure.attachment_type.WEBM)
#
#                 # Delete the video file after attaching it to the report
#                 os.remove(video_path)
#                 logger.info(f"Deleted video file: {video_path}")
#             except PermissionError as e:
#                 logger.error(f"Failed to delete video file: {e}")
#             except Exception as e:
#                 logger.error(f"Unexpected error: {e}")
#         else:
#             logger.error("Video file does not exist.")
#
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     # Execute all other hooks to obtain the report object
#     outcome = yield
#     report = outcome.get_result()
#
#     # Attach logs and screenshots to Allure report on failure
#     if report.when == "call" and report.failed:
#         page = item.funcargs.get("setup")
#         if page:
#             try:
#                 # Capture screenshot on failure
#                 screenshot = page.screenshot(full_page=True)
#                 allure.attach(screenshot, name="Screenshot on Failure", attachment_type=allure.attachment_type.PNG)
#
#                 # Capture console logs
#                 console_logs = page.evaluate("() => { return console.logs; }")
#                 if console_logs:
#                     allure.attach(str(console_logs), name="Console Logs", attachment_type=allure.attachment_type.TEXT)
#             except Exception as e:
#                 logger.error(f"Failed to capture screenshot or logs: {e}")




















import pytest
import allure
import os
import logging
from playwright.sync_api import sync_playwright
from utilities.config import Config  # Import your configuration

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def setup(request):
    with sync_playwright() as p:
        # Define browser arguments
        browser_args = [
            "--ignore-certificate-errors",  # Ignore certificate errors
            "--disable-notifications",  # Disable notifications
            "--disable-infobars",  # Disable infobars
        ]

        # Launch the browser with arguments
        browser = p[Config.BROWSER].launch(
            headless=Config.HEADLESS,
            args=browser_args  # Pass browser arguments
        )
        os.makedirs("videos", exist_ok=True)

        # Create a new context with video recording enabled (if video is enabled for pass or fail)
        context = browser.new_context(record_video_dir="videos/" if Config.VIDEO_ON_PASS == "yes" or Config.VIDEO_ON_FAIL == "yes" else None)

        # Create a new page
        page = context.new_page()
        page.set_default_timeout(60000)
        yield page  # Provide the page to the test

        # Close the context to release the video file (if video is enabled)
        context.close()
        browser.close()

        # Attach video for specific test cases (if video is enabled for pass or fail)
        if (Config.VIDEO_ON_PASS == "yes" and request.node.rep_call.passed) or (Config.VIDEO_ON_FAIL == "yes" and request.node.rep_call.failed):
            video_path = page.video.path()
            if video_path and os.path.exists(video_path):
                try:
                    # Attach the video to the Allure report
                    with open(video_path, "rb") as video_file:
                        video_data = video_file.read()
                    allure.attach(video_data, name="Execution Video", attachment_type=allure.attachment_type.WEBM)

                    # Delete the video file after attaching it to the report
                    os.remove(video_path)
                    logger.info(f"Deleted video file: {video_path}")
                except PermissionError as e:
                    logger.error(f"Failed to delete video file: {e}")
                except Exception as e:
                    logger.error(f"Unexpected error: {e}")
            else:
                logger.error("Video file does not exist.")



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # Attach logs and screenshots to Allure report based on configuration
    if report.when == "call":
        page = item.funcargs.get("setup")
        if page:
            try:
                # Attach screenshot if enabled for pass/fail
                if (report.passed and Config.SCREENSHOT_ON_PASS == "yes") or (report.failed and Config.SCREENSHOT_ON_FAIL == "yes"):
                    screenshot_data = page.screenshot(full_page=True)
                    allure.attach(screenshot_data, name="Screenshot", attachment_type=allure.attachment_type.PNG)

                # Capture console logs
                console_logs = page.evaluate("() => { return console.logs; }")
                if console_logs:
                    allure.attach(str(console_logs), name="Console Logs", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                logger.error(f"Failed to capture screenshot or logs: {e}")
