from pydantic import BaseModel, Field, field_validator


class Credentials(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if "@" not in normalized or normalized.startswith("@"):
            raise ValueError("A valid email address is required")
        return normalized


class RegisterRequest(Credentials):
    pass


class LoginRequest(Credentials):
    pass


class UserResponse(BaseModel):
    id: str
    email: str
    is_active: bool

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
