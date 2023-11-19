import os
from pathlib import Path

BASE_URL = os.environ.get('BASE_URL', "localhost")
DEV_MODE = bool(os.environ.get('DEV_MODE', True))
SWAGGER = bool(os.environ.get('SWAGGER', True))
REDOC = bool(os.environ.get('REDOC', True))
# Frequency of background task
SCHEDULER_FREQUENCY_SECONDS = int(
    os.environ.get('SCHEDULER_FREQUENCY_SECONDS', 600))
BATCH_SIZE = int(os.environ.get('BATCH_SIZE', 100))
# Logs settings
BACKUPS = int(os.environ.get('BACKUPS', 100))
LOG_SIZE_BYTES = int(os.environ.get('LOG_SIZE_BYTES', 1000000))
# Connect to Postgres
DB_USERNAME = os.environ.get('DB_USERNAME', "myuser")
DB_PASSWORD = os.environ.get('DB_PASSWORD', "mypassword")
DB_HOST = os.environ.get('DB_HOST', "localhost")
DB_PORT = int(os.environ.get('DB_PORT', 5432))
DB_NAME = os.environ.get('DB_NAME', "mydatabase")
# Connect to SMTP
SMTP_SERVER = os.environ.get('SMTP_SERVER', "___")
SMTP_PORT = int(os.environ.get('SMTP_PORT', 465))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', "___")
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', "___")
SMTP_SENDER_NAME = os.environ.get('SMTP_SENDER_NAME', "FAP-AMS")
# Connect to SMS API
SMS_API_URL = os.environ.get(
    'SMS_API_URL', "https://smsapi.yourservice.com/send")
SMS_API_KEY = os.environ.get('SMS_API_KEY', "yourapikey")
# Password length
PASSWD_MIN_LENGTH = int(os.environ.get('PASSWD_MIN_LENGTH', 6))
PASSWD_MAX_LENGTH = int(os.environ.get('PASSWD_MAX_LENGTH', 21))
# Nickname length
NICKNAME_MIN_LENGTH = int(os.environ.get('NICKNAME_MIN_LENGTH', 3))
NICKNAME_MAX_LENGTH = int(os.environ.get('NICKNAME_MAX_LENGTH', 42))
# Length of the string (name, phone, etc.)
STR_MAX_LENGTH = int(os.environ.get('STR_MAX_LENGTH', 42))
# Password attempts
PASSWORD_ATTEMPT = int(os.environ.get('PASSWORD_ATTEMPT', 3))
# Code attempts
CODE_ATTEMPT = int(os.environ.get('CODE_ATTEMPT', 3))
# Token issuance cooldown
TOKEN_COOLDOWN_SECONDS = int(os.environ.get('TOKEN_COOLDOWN_SECONDS', 60))
# Token expiration time
JWT_EXPIRATION_MINUTES = int(os.environ.get('JWT_EXPIRATION_MINUTES', 60))
RT_EXPIRATION_HOURS = int(os.environ.get('RT_EXPIRATION_HOURS', 1))
# Token expiration time
CODE_TOTAL_DIGITS = int(os.environ.get('CODE_TOTAL_DIGITS', 6))
CODE_UNIQUE_DIGITS = int(os.environ.get('CODE_UNIQUE_DIGITS', 4))
# Code issuance cooldown
CODE_COOLDOWN_SECONDS = int(os.environ.get('CODE_COOLDOWN_SECONDS', 60))
# Location of keys
PRIVATE_KEY_PATH = os.environ.get('PRIVATE_KEY_PATH', "keys/private_key.pem")
PUBLIC_KEY_PATH = os.environ.get('PUBLIC_KEY_PATH', "keys/public_key.pem")


# Keys loading function
def load_keys():
    private_key_path = Path(PRIVATE_KEY_PATH)
    public_key_path = Path(PUBLIC_KEY_PATH)
    return private_key_path.read_text(), public_key_path.read_text()


PRIVATE_KEY, PUBLIC_KEY = load_keys()
