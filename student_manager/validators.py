"""Input validation. Each function returns the cleaned value or raises ValidationError."""
import re

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class ValidationError(ValueError):
    """Raised when user input is invalid."""


def validate_name(value: str) -> str:
    value = (value or "").strip()
    if len(value) < 2:
        raise ValidationError("Name must be at least 2 characters.")
    if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", value):
        raise ValidationError("Name may contain only letters, spaces, . ' and -.")
    return value.title()


def validate_email(value: str) -> str:
    value = (value or "").strip().lower()
    if not EMAIL_RE.match(value):
        raise ValidationError("Invalid email format (example: name@example.com).")
    return value


def validate_age(value) -> int:
    try:
        age = int(str(value).strip())
    except ValueError:
        raise ValidationError("Age must be a whole number.")
    if not 5 <= age <= 100:
        raise ValidationError("Age must be between 5 and 100.")
    return age


def validate_course(value: str) -> str:
    value = (value or "").strip()
    if len(value) < 2:
        raise ValidationError("Course must be at least 2 characters.")
    return value
