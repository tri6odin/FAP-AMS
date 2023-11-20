import smtplib

from database.models.user import UserModel
from config import DEV_MODE, SMTP_PASSWORD, SMTP_PORT, SMTP_SENDER_NAME, SMTP_SERVER, SMTP_USERNAME

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils.logger import logger


# Calls code sending functions depending on the entered data

def send_code(user: UserModel, cred_type):
    if cred_type == 'email':
        return send_email(user.email, user.code_email)
    elif cred_type == 'phone':
        return send_sms(user.phone, user.code_phone)


# Sending a letter via SMTP gateway

def send_email(email, code):

    if DEV_MODE:
        logger.info("Email Code - %s - %s", str(email), str(code))
    plain_text_body = code
    html_body = f"""
                <html>
                    <body>
                        <div style=font-family:monospace;font-weight:bold;font-size:32px>
                            {code}
                        </div>
                    </body>
                </html>
                """
    subject = "One-time code:"

    # Create mail
    message = MIMEMultipart()
    message['From'] = SMTP_SENDER_NAME
    message['To'] = email
    message['Subject'] = subject

    # Add plain text body
    message.attach(MIMEText(plain_text_body, 'plain'))

    # Add HTML body
    message.attach(MIMEText(html_body if html_body else "No body", 'html'))

    # Sending
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_SENDER_NAME, email, message.as_string())
        server.quit()
    except Exception as e:
        logger.error("Email - %s", str(e))

# Sending SMS via API


def send_sms(phone, code):
    if DEV_MODE:
        logger.info("Phone Code - %s - %s", str(phone), str(code))
