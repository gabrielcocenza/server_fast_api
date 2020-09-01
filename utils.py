import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import emails
from emails.template import JinjaTemplate
from jose import jwt
from core.security import SECRET_KEY

# from core.config import settings

EMAILS_FROM_NAME = 'foo@gmail.com'
EMAILS_FROM_EMAIL = 'foo@gmail.com'
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = '465'
SMTP_TLS = True
SMTP_USER = 'foo@gmail.com'
SMTP_PASSWORD = 'password'
PROJECT_NAME = 'api'
EMAIL_TEMPLATES_DIR = "./email-templates/build"
SERVER_HOST = ''
EMAIL_RESET_TOKEN_EXPIRE_HOURS = 1


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    # assert False, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(EMAILS_FROM_NAME, EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": SMTP_HOST, "port": SMTP_PORT}
    if SMTP_TLS:
        smtp_options["tls"] = True
    if SMTP_USER:
        smtp_options["user"] = SMTP_USER
    if SMTP_PASSWORD:
        smtp_options["password"] = SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_test_email(email_to: str) -> None:
    project_name = PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None
