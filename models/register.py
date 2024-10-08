from pydantic import BaseModel, EmailStr, validator

class RegisterModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    
    @validator('first_name')
    def first_name_must_be_valid(cls, first_name):
        # if first_name is empty, raise an error
        if not first_name:
            raise ValueError('First name is required')

        return first_name

    @validator('last_name')
    def last_name_must_be_valid(cls, last_name):
        # if last_name is empty, raise an error
        if not last_name:
            raise ValueError('Last name is required')

        return last_name

    @validator('email')
    def email_must_be_valid(cls, email):
        # if email is empty, raise an error
        if not email:
            raise ValueError('Email is required')

        # if email does not contain @, raise an error
        if '@' not in email:
            raise ValueError('Invalid email')
        
        # if email does not contain ., raise an error
        if '.' not in email:
            raise ValueError('Invalid email')
    
        return email

    @validator('password')
    def password_must_be_valid(cls, password):
        # if password is empty, raise an error
        if not password:
            raise ValueError('Password is required')

        # if password is less than 8 characters, raise an error
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters')

        return password

    