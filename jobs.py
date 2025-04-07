


import os
import shutil
import subprocess
import zipfile
import webbrowser  # Add this import for opening the report

from utilities.email import send_email, parse_allure_report
def run_tests_and_send_email():
    """
    Runs the tests, generates the Allure report, parses the report, and sends an email with the results.
    """
    report_dir = "report"
    allure_report_dir = "allure-report"

    # Delete the existing report directory if it exists
    if os.path.exists(report_dir):
        shutil.rmtree(report_dir)

    # Define test cases to run
    test_cases = [
        "tests/Job/test_TC01_log.py",
        "tests/Job/test_TC02_log.py",
        "tests/Job/test_TC03_trajectory.py",
        "tests/Job/test_TC04_wellboreGeometry.py",
        "tests/Job/test_TC05_rig.py",
        "tests/Job/test_TC06_message.py",
        "tests/Job/test_TC07_formationMarker.py",
        "tests/Job/test_TC08_mudlog.py",
        "tests/Job/test_TC09_cement.py",
        "tests/Job/test_TC10_risk.py",
        "tests/Job/test_TC11_bharun.py",
        "tests/Job/test_TC12_target.py",
        "tests/Job/test_TC13_singlelogcurve.py",
        "tests/Job/test_TC14_singleRigObject.py",    ]

    # Run pytest with Allure
    pytest_command = f"pytest -v -s --alluredir={report_dir} {' '.join(test_cases)}"
    print(f"Running command: {pytest_command}")
    subprocess.run(pytest_command, shell=True)

    # Generate the Allure report
    allure_command = f"allure generate --single-file {report_dir} -o {allure_report_dir} --clean"
    print(f"Running command: {allure_command}")
    subprocess.run(allure_command, shell=True)

    # Parse the Allure report for detailed results
    try:
        passed_tests, failed_tests, broken_tests, total_tests, test_details = parse_allure_report(report_dir)
    except FileNotFoundError as e:
        print(f"Error parsing Allure report: {e}")
        return

    # Prepare the email body
    subject = "Automation Test Execution Report for Jobs module"
    body = f"Test Execution Summary:\n"
    # body += f"Total Tests: {total_tests}\n"
    body += f"Passed: {passed_tests}\n"
    body += f"Failed: {failed_tests}\n"
    body += f"Broken: {broken_tests}\n\n"
    # body += "Test Case Details:\n"
    # body += "\n".join(test_details)

    # Path to the Allure report file (for zipping)
    attachment_path = zip_allure_report(allure_report_dir)

    # List of recipients
    recipients = ["pavan.karri@covalensedigital.com"]

    # Send the email
    send_email(subject, body, recipients, attachment_path)

    # Automatically open the Allure report in the default web browser
    open_allure_report(allure_report_dir)


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


def open_allure_report(allure_report_dir):
    """
    Opens the Allure report in the default web browser.

    :param allure_report_dir: Path to the Allure report directory.
    """
    report_file = os.path.join(allure_report_dir, "index.html")

    if os.name == 'nt':  # If the OS is Windows
        os.startfile(report_file)  # Open the file in the default browser
    elif os.name == 'posix':  # If the OS is Linux or macOS
        subprocess.run(["open", report_file])  # Open the file in the default browser
    else:
        print(f"Cannot open the Allure report automatically on this OS: {os.name}")


if __name__ == "__main__":
    run_tests_and_send_email()