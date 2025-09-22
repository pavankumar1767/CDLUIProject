




# import os
# import shutil
# import subprocess
# import zipfile
# import webbrowser  # Add this import for opening the report

# from utilities.email import send_email, parse_allure_report
# def run_tests_and_send_email():
#     """
#     Runs the tests, generates the Allure report, parses the report, and sends an email with the results.
#     """
#     report_dir = "report"
#     allure_report_dir = "allure-report"

#     # Delete the existing report directory if it exists
#     if os.path.exists(report_dir):
#         shutil.rmtree(report_dir)

#     # Define test cases to run
#     test_cases = [
#         "tests/Login/test_Login.py",
#         "tests/GroupAndUser/test_TC01_createGroup.py",
#         "tests/GroupAndUser/test_TC02_createUser.py",
#         "tests/GroupAndUser/test_TC03_updateUser.py",
#         "tests/GroupAndUser/test_TC04_dataExtraction.py",
#         "tests/GroupAndUser/test_TC06_negativeScenarios.py",
#         "tests/GroupAndUser/test_TC07_deleteUser.py",
#         "tests/GroupAndUser/test_TC08_deleteGroup.py",
#         "tests/GroupAndUser/test_TC09_groupPermissions.py",
#         "tests/GroupAndUser/test_TC10_multipleGroups.py",
#         "tests/Filters/test_TC01_extractFilter.py",
#         "tests/Filters/test_TC02_saveFilter.py",
#         "tests/Filters/test_TC03_editFilter.py",
#         "tests/Filters/test_TC04_editExtractFilter.py",
#         "tests/Filters/test_TC05_negative_scenarios.py",
#         "tests/Job/test_TC01_log.py",
#         "tests/Job/test_TC02_log.py",
#         "tests/Job/test_TC03_trajectory.py",
#         "tests/Job/test_TC04_wellboreGeometry.py",
#         "tests/Job/test_TC05_rig.py",
#         "tests/Job/test_TC06_message.py",
#         "tests/Job/test_TC07_formationMarker.py",
#         "tests/Job/test_TC08_mudlog.py",
#         "tests/Job/test_TC09_cement.py",
#         "tests/Job/test_TC10_risk.py",
#         "tests/Job/test_TC11_bharun.py",
#         "tests/Job/test_TC12_target.py",
#         "tests/Job/test_TC13_singlelogcurve.py",
#         "tests/Job/test_TC14_singleRigObject.py",

#     ]

#     # Run pytest with Allure
#     pytest_command = f"pytest -v -s --alluredir={report_dir} {' '.join(test_cases)}"
#     print(f"Running command: {pytest_command}")
#     subprocess.run(pytest_command, shell=True)

#     # Generate the Allure report
#     allure_command = f"allure generate --single-file {report_dir} -o {allure_report_dir} --clean"
#     print(f"Running command: {allure_command}")
#     subprocess.run(allure_command, shell=True)

#     # Parse the Allure report for detailed results
#     try:
#         passed_tests, failed_tests, broken_tests, total_tests, test_details = parse_allure_report(report_dir)
#     except FileNotFoundError as e:
#         print(f"Error parsing Allure report: {e}")
#         return

#     # Prepare the email body
#     subject = "Automation Test Execution Report"
#     body = f"Test Execution Summary:\n"
#     # body += f"Total Tests: {total_tests}\n"
#     body += f"Passed: {passed_tests}\n"
#     body += f"Failed: {failed_tests}\n"
#     body += f"Broken: {broken_tests}\n\n"
#     # body += "Test Case Details:\n"
#     # body += "\n".join(test_details)

#     # Path to the Allure report file (for zipping)
#     attachment_path = zip_allure_report(allure_report_dir)

#     # List of recipients
#     recipients = ["pavan.karri@covalensedigital.com", "dasharathi.chakaravarthy@covalensedigital.com"]

#     # Send the email
#     send_email(subject, body, recipients, attachment_path)

#     # Automatically open the Allure report in the default web browser
#     open_allure_report(allure_report_dir)


# def zip_allure_report(allure_report_dir):
#     """
#     Zips the Allure report directory into a .zip file.

#     :param allure_report_dir: Path to the Allure report directory.
#     :return: Path to the zip file.
#     """
#     zip_file = f"{allure_report_dir}.zip"

#     # Compress the Allure report directory into a .zip file
#     with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
#         for root, dirs, files in os.walk(allure_report_dir):
#             for file in files:
#                 zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), allure_report_dir))

#     return zip_file


# def open_allure_report(allure_report_dir):
#     """
#     Opens the Allure report in the default web browser.

#     :param allure_report_dir: Path to the Allure report directory.
#     """
#     report_file = os.path.join(allure_report_dir, "index.html")

#     if os.name == 'nt':  # If the OS is Windows
#         os.startfile(report_file)  # Open the file in the default browser
#     elif os.name == 'posix':  # If the OS is Linux or macOS
#         subprocess.run(["open", report_file])  # Open the file in the default browser
#     else:
#         print(f"Cannot open the Allure report automatically on this OS: {os.name}")


# if __name__ == "__main__":
#     run_tests_and_send_email()





import os
import shutil
import subprocess
import zipfile
import webbrowser
import logging
import sys

from utilities.email import send_email, parse_allure_report, send_teams_message

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_tests_and_send_email():
    """
    Runs the tests, generates the Allure report, parses the report, and sends an email with the results.
    """
    report_dir = "report"
    allure_report_dir = "allure-report"

    # Delete the existing report directory if it exists
    if os.path.exists(report_dir):
        try:
            shutil.rmtree(report_dir)
            logger.info(f"Deleted existing report directory: {report_dir}")
        except Exception as e:
            logger.warning(f"Could not delete report directory: {e}")

    # Define test cases to run in specific order
    test_cases = [
        # "tests/Login/test_Login.py",
        # "tests/Login/test_TC02_invalidLogin.py",
        # "tests/Login/test_TC03_forgotPassword.py",
        # "tests/Login/test_TC04_resetPassword.py",
        # "tests/Login/test_TC05_sessionTimeout.py"

        "tests/Audit/test_TC01_login_audit.py",
        "tests/GroupAndUser/test_TC01_createGroup.py",
        "tests/GroupAndUser/test_TC02_createUser.py",
        "tests/GroupAndUser/test_TC03_updateUser.py",
        "tests/GroupAndUser/test_TC07_deleteUser.py",
        "tests/GroupAndUser/test_TC08_deleteGroup.py",
        "tests/Settings/test_TC01_settings.py",
        "tests/Filters/test_TC02_saveFilter.py",
        "tests/Audit/test_TC02_systemconfig.py",

    ]

    # Run each test file sequentially
    for test_file in test_cases:
        logger.info(f"Running command: pytest -v -s --alluredir={report_dir} {test_file}")
        subprocess.run(f"pytest -v -s --alluredir={report_dir} {test_file}", shell=True)

    # Generate the Allure report
    allure_command = f"allure generate --single-file {report_dir} -o {allure_report_dir} --clean"
    logger.info(f"Running command: {allure_command}")
    subprocess.run(allure_command, shell=True)

    # Parse the Allure report for detailed results
    try:
        passed_tests, failed_tests, broken_tests, total_tests, test_details = parse_allure_report(report_dir)
        logger.info(f"Test results parsed: Passed={passed_tests}, Failed={failed_tests}, Broken={broken_tests}, Total={total_tests}")
    except FileNotFoundError as e:
        logger.error(f"Error parsing Allure report: {e}")
        return

    # Prepare the email body
    subject = "Automation Test Execution Report for Login module"
    body = f"Test Execution Summary:\n"
    body += f"Passed: {passed_tests}\n"
    body += f"Failed: {failed_tests}\n"
    body += f"Broken: {broken_tests}\n\n"

    # Path to the Allure report file (for zipping)
    logger.info("Creating zip file of Allure report...")
    attachment_path = zip_allure_report(allure_report_dir)
    logger.info(f"Zip file created at: {attachment_path}")

    # List of recipients
    recipients = ["pavan.karri@covalensedigital.com", "dasharathi.chakaravarthy@covalensedigital.com"]
    logger.info(f"Preparing to send email to: {', '.join(recipients)}")

    # Send the email
    email_sent = send_email(subject, body, recipients, attachment_path)
    if email_sent:
        logger.info("Email sent successfully")
    else:
        logger.error("Failed to send email")
        # --- Send Teams Notification ---
    webhook_url = "https://covalensedigital.webhook.office.com/webhookb2/1cc58207-7d96-40dd-9519-eff91795e067@3473a586-677d-4216-ac29-91a55b9b642d/IncomingWebhook/1605e12ef7be497a9fe20c97de2220b6/cedac22f-fef6-410a-99a7-663ce64c4508/V2kcXP7dnKUKjL9ihlExEOu7cBajS1YGjKeJZpu01kr2M1"  # 🔑 Replace with your Teams webhook
    send_teams_message(webhook_url, subject, body, test_details)

    logger.info("Test execution completed. Check the allure-report directory for results.")


def zip_allure_report(allure_report_dir):
    """
    Zips the Allure report directory into a .zip file.

    :param allure_report_dir: Path to the Allure report directory.
    :return: Path to the zip file.
    """
    zip_file = f"{allure_report_dir}.zip"

    # Compress the Allure report directory into a .zip file
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(allure_report_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), allure_report_dir))

    return zip_file


if __name__ == "__main__":
    run_tests_and_send_email()

