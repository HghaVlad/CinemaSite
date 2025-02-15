from smtplib import SMTP
from email.mime.text import MIMEText

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