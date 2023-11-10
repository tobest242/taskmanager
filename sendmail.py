import time
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
load_dotenv()


def send_email(subject, body, recipient_email):
    subject = subject
    body = body
    sender_email = os.environ.get('sender_email')
    recipient_email = recipient_email

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    smtp_server.login(os.environ.get('sender_email'), 
                      os.environ.get('app_password')) 
    smtp_server.sendmail(sender_email, recipient_email, msg.as_string())
    smtp_server.quit()
    print("email sent !!")

