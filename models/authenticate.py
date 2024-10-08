from pydantic import BaseModel, EmailStr, validator

class AuthenticateModel(BaseModel):
    """
    Model to authenticate a user
    """
    email: EmailStr
    password: str

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

        # if password is less than 6 characters, raise an error
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters')
        
        # check password should contain atleast 1 capital letter
        if not any(char.isupper() for char in password):
            raise ValueError('Password must contain atleast 1 capital letter')
        
        # check password should contain atleast 1 digit
        if not any(char.isdigit() for char in password):
            raise ValueError('Password must contain atleast 1 digit')

        return password

