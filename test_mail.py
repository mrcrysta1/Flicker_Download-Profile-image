import os
import smtplib
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

print("Email:", EMAIL_ADDRESS)
print("App Password:", EMAIL_APP_PASSWORD)
print("To:", TO_EMAIL)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
    smtp.sendmail(EMAIL_ADDRESS, TO_EMAIL, "Subject: Test\n\nHello from Python!")
    print("✅ Email sent successfully")
