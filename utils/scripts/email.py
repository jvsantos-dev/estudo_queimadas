import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email:
    def __init__(self, subject, body, to):
        self.subject = subject
        self.body = body
        self.to = to

    def send(self):
        print(f"Sending email to {self.to}")
        print(f"Subject: {self.subject}")
        print(f"Body: {self.body}")