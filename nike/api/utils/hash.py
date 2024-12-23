from passlib.context import CryptContext
import hashlib

pwd_txt = CryptContext(schemes=['bcrypt'], deprecated='auto')

class Hash:
    def bcrypt(password: str):
        return pwd_txt.hash(password)
    
    def verify( plain_password: str, hashed_password: str):
        return pwd_txt.verify(plain_password, hashed_password)

def hash256(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()