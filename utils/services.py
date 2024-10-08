import bcrypt
def hash_password(password: str) -> str:
    """
    Hash the password
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify the password
    """
    verification = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    return verification
