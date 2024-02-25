from passlib.context import CryptContext

# we are just telling passlib what the encryption...
# algorithm is.
# we can just copy and paste this.
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)