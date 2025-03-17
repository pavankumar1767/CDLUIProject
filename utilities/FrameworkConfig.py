class FrameworkConfig:
    BROWSER = "chromium"  # Options: chromium, firefox, webkit
    HEADLESS = False

    # Report configurations
    VIDEO_ON_PASS = "yes"
    VIDEO_ON_FAIL = "yes"
    SCREENSHOT_ON_PASS = "no"
    SCREENSHOT_ON_FAIL = "yes"
    LoggerScreenshot_ON_PASS = "yes"  # Options: "yes", "no"
    LoggerScreenshot_ON_FAIL = "yes"