



import pytest
import allure
import os
import logging
from playwright.sync_api import sync_playwright
from utilities.FrameworkConfig import FrameworkConfig  # Import your configuration

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
        browser = p[FrameworkConfig.BROWSER].launch(
            headless=FrameworkConfig.HEADLESS,
            args=browser_args
        )
        os.makedirs("videos", exist_ok=True)

        # Set lower video quality by reducing resolution (e.g., 640x480)
        record_video_size = {"width": 640, "height": 480}  # Lower resolution

        # Create a new context with reduced video resolution
        context = browser.new_context(
            record_video_dir="videos/" if FrameworkConfig.VIDEO_ON_PASS == "yes" or FrameworkConfig.VIDEO_ON_FAIL == "yes" else None,
            record_video_size=record_video_size  # Apply low-quality video setting
        )

        # Create a new page
        page = context.new_page()
        page.set_default_timeout(60000)
        yield page  # Provide the page to the test

        # Close the context to release the video file
        context.close()
        browser.close()

        # Attach video for specific test cases (if video is enabled for pass or fail)
        if (FrameworkConfig.VIDEO_ON_PASS == "yes" and request.node.rep_call.passed) or (FrameworkConfig.VIDEO_ON_FAIL == "yes" and request.node.rep_call.failed):
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
                if (report.passed and FrameworkConfig.SCREENSHOT_ON_PASS == "yes") or (report.failed and FrameworkConfig.SCREENSHOT_ON_FAIL == "yes"):
                    screenshot_data = page.screenshot(full_page=True)
                    allure.attach(screenshot_data, name="Screenshot", attachment_type=allure.attachment_type.PNG)

                # Capture console logs
                console_logs = page.evaluate("() => { return console.logs; }")
                if console_logs:
                    allure.attach(str(console_logs), name="Console Logs", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                logger.error(f"Failed to capture screenshot or logs: {e}")

import pytest
from utilities.config import load_config

ENV = "stage"  # Change this to 'qa' or 'prod' as needed

@pytest.fixture(scope="session")
def config():
    """
    Load the configuration for the specified environment.
    """
    return load_config(ENV)
