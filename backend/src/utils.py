import re
import random
import string
from smtplib import SMTP
from email.mime.text import MIMEText

from fastapi import HTTPException
from starlette import status

from core.config import settings


async def send_registration_email(email: str, name: str):
    conn = SMTP(host=settings.mail_config.MAIL_SERVER, port=settings.mail_config.MAIL_PORT)
    conn.starttls()
    conn.login(user=settings.mail_config.MAIL_USERNAME, password=settings.mail_config.MAIL_PASSWORD)
    message = MIMEText(
        f"Здорова {name}!\n\nНам лень делать подтверждение почты.\nТак что надеюсь ты сделал все правильно\n\n"
        f"С уважением,\nКоманда кинотеатра")
    message["Subject"] = "Спасибо за регу"
    message["To"] = email
    message["From"] = settings.mail_config.MAIL_FROM
    conn.sendmail(settings.mail_config.MAIL_FROM, email, message.as_string())


async def send_reset_password_email(email: str, name: str, new_password: str):
    conn = SMTP(host=settings.mail_config.MAIL_SERVER, port=settings.mail_config.MAIL_PORT)
    conn.starttls()
    conn.login(user=settings.mail_config.MAIL_USERNAME, password=settings.mail_config.MAIL_PASSWORD)
    message = MIMEText(f"Привет {name}!\n\nМы обновили тебе пароль. Вот новый: {new_password}\n\n")
    message["Subject"] = "Восстановление пароля"
    message["To"] = email
    message["From"] = settings.mail_config.MAIL_FROM
    conn.sendmail(settings.mail_config.MAIL_FROM, email, message.as_string())


def is_password_strong(password) -> (bool, str):
    """
    Validates if a password is strong based on the following rules:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    """
    # Minimum length
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    # At least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."

    # At least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."

    # At least one digit
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit."

    # If all checks pass
    return True, "Password is strong."


def is_name_or_surname_valid(name: str, first_or_last: str) -> bool:
    if name.isalpha() and len(name) >= 2:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{first_or_last} should consist of 2 or more alphabetic characters"
        )


def generate_new_password():
    """
    Generates a random password that meets the following criteria:
    - 8-16 characters long.
    - Contains at least one lowercase letter.
    - Contains at least one uppercase letter.
    - Contains at least one digit.
    """

    length = random.randint(8, 16)

    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits

    # Ensure at least one character from each set
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
    ]

    # Fill the rest of the password with random choices from all sets
    all_characters = lowercase + uppercase + digits
    password += random.choices(all_characters, k=length - 3)

    # Shuffle the password to avoid predictable patterns
    random.shuffle(password)

    # Convert the list to a string
    return ''.join(password)