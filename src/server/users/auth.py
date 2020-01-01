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
