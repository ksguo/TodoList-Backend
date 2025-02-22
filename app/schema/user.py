import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False


# Properties to receive via API on creation


# for internal use
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


# for external use
class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)


# Properties to receive via API on update


# admin use
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


# user use
class UserUpdateMe(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)


# user use
class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
# Database storage and ORM operations
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


# Properties to return via API, id is always required
# Returns public information of a single user
class UserPublic(UserBase):
    id: uuid.UUID


# Return paged/batch user query results
class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
