
import os
import shutil
from utilities.email import send_email

report_dir = "report"
allure_report_dir = "allure-report"

if os.path.exists(report_dir):
    shutil.rmtree(report_dir)  # ✅ Cross-platform way to delete a directory

# Define test cases to run
test_cases = [
    "tests/Login/test_Login.py"
]

# Run pytest with Allure
pytest_command = f"pytest -v -s --alluredir={report_dir} {' '.join(test_cases)}"
print(f"Running command: {pytest_command}")
os.system(pytest_command)

# Generate the Allure report
allure_command = f"allure generate --single-file {report_dir} -o {allure_report_dir} --clean"
print(f"Running command: {allure_command}")
os.system(allure_command)

# Path to the generated index.html file
index_html_path = os.path.join(allure_report_dir, "index.html")

# Check if the index.html file exists
if not os.path.exists(index_html_path):
    raise FileNotFoundError(f"Allure report not found at: {index_html_path}")

# Email recipients
recipients = ["pavan.karri@covalensedigital.com"]

# Send the report via email
send_email(
    subject="Allure Test Report",
    body="Please find the attached Allure test report (index.html).",
    to_email=recipients,
    attachment_path=index_html_path
)

print("Email sent successfully!")