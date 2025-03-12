class Config:
    BASE_URL = "https://149.255.39.63"
    # username = "AutomationQA"
    # password = "Abcd@1234"
    username = "sigmastream"
    password = "Init@123!"
    setpassword = "Abcd@1234"
    BROWSER = "chromium"  # Options: chromium, firefox, webkit
    HEADLESS = False

    # Report configurations
    VIDEO_ON_PASS = "no"
    VIDEO_ON_FAIL = "yes"
    SCREENSHOT_ON_PASS = "no"
    SCREENSHOT_ON_FAIL = "yes"
    LoggerScreenshot_ON_PASS = "yes"  # Options: "yes", "no"
    LoggerScreenshot_ON_FAIL = "yes"