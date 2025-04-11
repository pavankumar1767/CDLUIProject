class FrameworkConfig:
    BROWSER = "chromium"  # Options: chromium, firefox, webkit
    HEADLESS = False

    # Report configurations
    VIDEO_ON_PASS = "no"
    VIDEO_ON_FAIL = "no"
    SCREENSHOT_ON_PASS = "no"
    SCREENSHOT_ON_FAIL = "yes"
    LoggerScreenshot_ON_PASS = "no"  # Options: "yes", "no"
    LoggerScreenshot_ON_FAIL = "yes"