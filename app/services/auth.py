from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories import users


class DuplicateEmailError(Exception):
    """Raised when registration uses an existing email address."""


class InvalidCredentialsError(Exception):
    """Raised when login credentials are not valid."""


def register_user(session: Session, email: str, password: str) -> User:
    if users.get_by_email(session, email) is not None:
        raise DuplicateEmailError
    return users.create(session, email, hash_password(password))


def authenticate_user(session: Session, email: str, password: str) -> str:
    user = users.get_by_email(session, email)
    if (
        user is None
        or not user.is_active
        or not verify_password(password, user.password_hash)
    ):
        raise InvalidCredentialsError
    return create_access_token(user.id)
