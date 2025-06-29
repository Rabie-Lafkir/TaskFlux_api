from pydantic import BaseModel, EmailStr, constr
from typing import Optional

UsernameStr = constr(strip_whitespace=True, min_length=3, max_length=50)
NameStr     = constr(max_length=50)
PasswordStr = constr(min_length=6)

class UserRegisterSchema(BaseModel):
    username: UsernameStr # type: ignore
    email:    EmailStr
    password: PasswordStr # type: ignore
    first_name: Optional[NameStr] = None # type: ignore
    last_name:  Optional[NameStr] = None # type: ignore
    profile_pic: Optional[str] = None

class UserLoginSchema(BaseModel):
    email:    EmailStr
    password: PasswordStr # type: ignore

class UserUpdateSchema(BaseModel):
    username:   Optional[UsernameStr] = None # type: ignore
    email:      Optional[EmailStr]    = None
    first_name: Optional[NameStr]     = None # type: ignore
    last_name:  Optional[NameStr]     = None # type: ignore
    profile_pic: Optional[str]        = None 
