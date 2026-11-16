# project/starter/app/schemas/user.py
# Module 5 Project — User schemas
#
# TODO: Define UserCreate, UserResponse, TokenResponse

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    """Registration input."""
    # TODO: username, email, password
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    """Returned to clients — no password fields."""
    # TODO: id, username, email + model_config
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)




class TokenResponse(BaseModel):
    """JWT token response."""
    # TODO: access_token, token_type
    access_token: str
    token_type: str = "bearer"