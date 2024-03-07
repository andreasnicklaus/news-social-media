import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

from datetime import datetime as dt


GMAIL_SENDER_ADDRESS = os.environ.get("GMAIL_SENDER_ADDRESS")
GMAIL_ACCESS_TOKEN = os.environ.get("GMAIL_ACCESS_TOKEN")
GMAIL_RECEIVER_ADDRESS = os.environ.get("GMAIL_RECEIVER_ADDRESS")


def send_with_attachment(content, attachment):
    sender_email = GMAIL_SENDER_ADDRESS
    recipient_email = GMAIL_RECEIVER_ADDRESS
    sender_password = GMAIL_ACCESS_TOKEN

    now = dt.now()

    message = MIMEMultipart()
    message[
        "Subject"
    ] = f"New Post - {now.strftime('%Y')}-{now.strftime('%m')}-{now.strftime('%d')}"
    message["From"] = sender_email
    message["To"] = recipient_email
    html_part = MIMEText(content)
    message.attach(html_part)

    if (attachment):
        with open(attachment, "rb") as attachment_file:
            # Add the attachment to the message
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment_file.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={attachment.split('/')[-1]}",
        )
        message.attach(part)

    with smtplib.SMTP_SSL("smtp.googlemail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("E-Mail sent")
