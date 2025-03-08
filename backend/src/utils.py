import random
import string
from smtplib import SMTP
from email.mime.text import MIMEText

from fastapi.openapi.utils import get_openapi

from core.config import settings
from schemas.Payment import UserPayment
from models.payments import PaymentStatus


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


def process_payment(payment: UserPayment) -> PaymentStatus:
    if payment.cvv == 123 and payment.card_number == "1234567890123456" and payment.card_holder == "John Doe":
        return PaymentStatus.SUCCESS
    elif payment.cvv == 000 or len(payment.card_number) < 16 or payment.card_number == "0000000000000000" or len(payment.card_holder) < 3:
        return PaymentStatus.ERROR

    if random.randint(0, 1) == 0:
        return PaymentStatus.NOT_ENOUGH_MONEY

    return PaymentStatus.FAILED

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Your API",
        version="1.0",
        routes=app.routes,
    )

    # Добавляем схему безопасности Bearer JWT
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",  # Указываем, что используется JWT
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema