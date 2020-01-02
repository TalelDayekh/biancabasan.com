from pathlib import Path
from typing import Type

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.exceptions import ValidationError


def password_strength_validator(password: str) -> None:
    # Checks that a password has at least one capitalized letter,
    # one number and is longer than or equal to eight characters.
    password = str(password)
    if not (
        any(character.isupper() for character in password)
        and any(character.isdigit() for character in password)
        and len(password) >= 8
    ):
        raise ValidationError(
            {
                "message": "Your password has to be at least 8 characters and contain both digits and upper case letters."
            }
        )


def send_password_reset_email(
    user: Type[CustomUser], domain: str, use_https: bool = False
) -> None:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    protocol = "https://" if use_https else "http://"
    password_reset_url = protocol + str(
        Path(domain).joinpath("password_reset", uid, token)
    )

    email = EmailMessage(
        subject="Password Reset",
        body="Click the link and follow the instructions to reset your password "
        + str(password_reset_url),
        from_email=os.environ.get("BIANCA_BASAN_EMAIL_USERNAME"),
        to=[user.email],
    )
    email.send()
