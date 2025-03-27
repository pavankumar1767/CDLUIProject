
import os
import shutil
from utilities.email import send_email

report_dir = "report"
allure_report_dir = "allure-report"

if os.path.exists(report_dir):
    shutil.rmtree(report_dir)  # ✅ Cross-platform way to delete a directory

# Define test cases to run
test_cases = [
    "tests/Job/test_TC01_log.py",
    "tests/Job/test_TC02_log.py",
    "tests/Job/test_TC03_trajectory.py",
    "tests/Job/test_TC04_wellboreGeometry.py",
    "tests/Job/test_TC05_rig.py",
    "tests/Job/test_TC06_message.py",
    "tests/Job/test_TC07_formationMarker.py",
    "tests/Job/test_TC12_target.py",
    "tests/Job/test_TC10_risk.py"
    "tests/Job/test_TC14_singleRigObject.py",
]

# Run pytest with Allure
pytest_command = f"pytest -v -s --alluredir={report_dir} {' '.join(test_cases)}"
print(f"Running command: {pytest_command}")
os.system(pytest_command)

# Generate the Allure report
allure_command = f"allure generate --single-file {report_dir} -o {allure_report_dir} --clean"
print(f"Running command: {allure_command}")
os.system(allure_command)


os.system("allure serve report")




















# import os
# import shutil
# import subprocess
#
# from utilities.email import send_email, parse_allure_report
#
#
# def run_tests_and_send_email():
#     """
#     Runs the tests, generates the Allure report, parses the report, and sends an email with the results.
#     """
#     report_dir = "report"
#     allure_report_dir = "allure-report"
#
#     # Delete the existing report directory if it exists
#     if os.path.exists(report_dir):
#         shutil.rmtree(report_dir)
#
#     # Define test cases to run
#     test_cases = [
#         # "tests/Job/test_TC01_log.py",
#         # "tests/Job/test_TC02_log.py",
#         # "tests/Job/test_TC03_trajectory.py",
#         "tests/Job/test_TC04_wellboreGeometry.py",
#         "tests/Job/test_TC05_rig.py"
#     ]
#
#     # Run pytest with Allure
#     pytest_command = f"pytest -v -s --alluredir={report_dir} {' '.join(test_cases)}"
#     print(f"Running command: {pytest_command}")
#     subprocess.run(pytest_command, shell=True)
#
#     # Generate the Allure report
#     allure_command = f"allure generate --single-file {report_dir} -o {allure_report_dir} --clean"
#     print(f"Running command: {allure_command}")
#     subprocess.run(allure_command, shell=True)
#
#     # Parse the Allure report for detailed results
#     try:
#         passed_tests, failed_tests, test_details = parse_allure_report(report_dir)
#     except FileNotFoundError as e:
#         print(f"Error parsing Allure report: {e}")
#         return
#
#     # Prepare the email body
#     subject = "Allure Test Report"
#     body = f"Test Execution Summary:\n"
#     body += f"Passed: {passed_tests}\n"
#     body += f"Failed: {failed_tests}\n\n"
#     body += "Test Case Details:\n"
#     body += "\n".join(test_details)
#
#     # Path to the Allure report file
#     attachment_path = os.path.join(allure_report_dir, "index.html")
#
#     # Check if the index.html file exists
#     if not os.path.exists(attachment_path):
#         raise FileNotFoundError(f"Allure report not found at: {attachment_path}")
#
#     # List of recipients
#     recipients = ["pavan.karri@covalensedigital.com"]
#
#     # Send the email
#     send_email(subject, body, recipients, attachment_path)
#
#
# if __name__ == "__main__":
#     run_tests_and_send_email()