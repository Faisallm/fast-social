from passlib.context import CryptContext

# we are just telling passlib what the encryption...
# algorithm is.
# we can just copy and paste this.
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    # we want to hash and compare, hence verify
    # it's a two step process.
    return pwd_context.verify(plain_password, hashed_password)