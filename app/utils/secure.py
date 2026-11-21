from passlib.context import CryptContext




context = CryptContext(schemes=['argon2'], deprecated='auto')


def hash_password(plain_text):

    encoded = context.hash(plain_text)

    return encoded

def verify_password(plain_text, hashed_password):

    return context.verify(plain_text, hashed_password)


