import os
import shutil
import subprocess
import json
import smtplib
import logging
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

# Configure logging to output to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

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

    logger.info(f"Preparing to send email to: {', '.join(to_email)}")
    logger.info(f"Subject: {subject}")
    logger.info(f"Attachment path: {attachment_path}")

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email)  # Display all recipients in To field
    msg['Subject'] = subject

    # Add the email body
    msg.attach(MIMEText(body, 'plain'))
    logger.info("Email body attached")

    # Attach the Allure report
    try:
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
            msg.attach(part)
            logger.info(f"Successfully attached file: {os.path.basename(attachment_path)}")
    except FileNotFoundError:
        logger.error(f"Attachment file not found: {attachment_path}")
        raise
    except Exception as e:
        logger.error(f"Error attaching file: {str(e)}")
        raise

    try:
        logger.info("Connecting to SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        logger.info("SMTP connection established")

        logger.info("Attempting to login...")
        server.login(from_email, from_password)
        logger.info("Login successful")

        text = msg.as_string()
        logger.info("Sending email...")
        server.sendmail(from_email, to_email, text)
        logger.info("Email sent successfully!")

        server.quit()
        logger.info("SMTP connection closed")
        return True
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP Authentication failed: {str(e)}")
        return False
    except smtplib.SMTPDataError as e:
        logger.error(f"SMTP Data error: {str(e)}")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error occurred: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        return False

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

    if not os.path.exists(report_dir):
        raise FileNotFoundError(f"Allure report directory not found: {report_dir}")

    # Only pick test result JSON files
    for filename in os.listdir(report_dir):
        if filename.endswith("-result.json"):  # ✅ filter real test cases
            try:
                with open(os.path.join(report_dir, filename), "r", encoding="utf-8") as file:
                    data = json.load(file)
                    status = data.get("status", "unknown")
                    name = data.get("name", "Unnamed Test")

                    total_tests += 1

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

import requests
def send_teams_message(webhook_url, subject, body, test_summary):
    try:
        # Format detailed results as a markdown list with line breaks
        formatted_summary = "\n".join([f"- {test}" for test in test_summary])

        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": subject,
            "title": f"📊 {subject}",
            "sections": [
                {
                    "activityTitle": body,
                    "markdown": True
                },
                {
                    "title": "🧪 Detailed Test Results",
                    "text": formatted_summary,
                    "markdown": True   # ✅ ensures Teams respects line breaks
                }
            ]
        }

        response = requests.post(webhook_url, json=message)
        if response.status_code == 200:
            print("✅ Teams message sent successfully.")
        else:
            print(f"❌ Failed to send Teams message: {response.status_code}, {response.text}")

    except Exception as e:
        print(f"❌ Exception while sending Teams message: {e}")
