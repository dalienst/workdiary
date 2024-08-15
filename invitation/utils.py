import secrets
import string

from django.core.mail import send_mail
from django.template.loader import render_to_string

from workdiary.settings import DOMAIN


def generate_token():
    characters = string.ascii_letters + string.digits
    random_string = "".join(secrets.choice(characters) for _ in range(64))
    return random_string


def generate_slug():
    characters = string.ascii_letters + string.digits
    random_string = "".join(secrets.choice(characters) for _ in range(16))
    return random_string


def send_invitation_email(email, token, user, company):
    email_body = render_to_string(
        "email_invitation.html",
        {
            "email": email,
            "token": token,
            "domain": DOMAIN,
            "user": user.first_name + " " + user.last_name,
            "company": company,
        },
    )

    send_mail(
        "Invitation",
        email_body,
        from_email=user,
        recipient_list=[email],
        fail_silently=False,
    )
