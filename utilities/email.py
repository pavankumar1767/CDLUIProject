
import os
import shutil
import subprocess
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText


def send_email(subject, body, to_email, attachment_path):
    """
    Sends an email with the test results and attaches the Allure report.

    :param subject: Email subject.
    :param body: Email body.
    :param to_email: List of recipient email addresses.
    :param attachment_path: Path to the Allure report file.
    """
    from_email = "sigmastreamautomation@gmail.com"
    from_password = "yque cesi nyqn pylv"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email)  # Display all recipients in To field
    msg['Subject'] = subject

    # Add the email body
    msg.attach(MIMEText(body, 'plain'))

    # Attach the Allure report
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully!")
    except smtplib.SMTPDataError as e:
        print(f"Failed to send email: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def parse_allure_report(report_dir):
    """
    Parses the Allure report to get detailed test results.

    :param report_dir: Path to the Allure report directory.
    :return: A tuple containing the number of passed tests, failed tests, broken tests, total tests, and a list of test details.
    """
    passed_tests = 0
    failed_tests = 0
    broken_tests = 0
    test_details = []
    total_tests = 0

    # Check if the report directory exists
    if not os.path.exists(report_dir):
        raise FileNotFoundError(f"Allure report directory not found: {report_dir}")

    # Iterate through all JSON files in the report directory
    for filename in os.listdir(report_dir):
        if filename.endswith(".json"):
            try:
                with open(os.path.join(report_dir, filename), "r", encoding="utf-8") as file:
                    data = json.load(file)
                    status = data.get("status", "unknown")
                    name = data.get("name", "Unnamed Test")

                    total_tests += 1  # Increment total tests count

                    if status == "passed":
                        passed_tests += 1
                    elif status == "failed":
                        failed_tests += 1
                    elif status == "broken":
                        broken_tests += 1

                    test_details.append(f"{name}: {status}")

            except Exception as e:
                print(f"⚠️ Failed to read {filename}: {e}")

    return passed_tests, failed_tests, broken_tests, total_tests, test_details
