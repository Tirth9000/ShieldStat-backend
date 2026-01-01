import re
from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional

class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    username: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class QuestionOptionSchema(BaseModel):
    option_key: str
    option_text: str
    score: int

class QuestionResponseSchema(BaseModel):
    _id: str
    id: int
    category_id: int
    category_name: str
    question_text: str
    options: List[QuestionOptionSchema]