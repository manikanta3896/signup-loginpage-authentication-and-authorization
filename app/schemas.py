from pydantic import BaseModel, EmailStr, ConfigDict


class UserSignup(BaseModel):
    username: str
    first_name: str
    last_name: str
    phone: str
    email: EmailStr


class CreatePassword(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    phone: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)