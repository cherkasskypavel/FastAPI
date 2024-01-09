from passlib.context import CryptContext

crypt_context = CryptContext(['bcrypt'])


def encrypt_pass(password: str):
    return crypt_context.hash(password)


def verify_pass(password: str, encoded_pasword: str):
    return crypt_context.verify(password, encoded_pasword)