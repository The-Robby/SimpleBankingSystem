import re
import hashlib
from hashlib import pbkdf2_hmac as pbkdf2
import os


def check_pass_cond(password):
    pattern = re.compile(r'^(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?=.*[\W_])[a-zA-Z0-9\W_]{6,12}$')

    if re.match(pattern, password):
        return True
    else:
        return False
    




def create_hash(password, salt):
    plaintext = password.encode()
    digest = pbkdf2('sha256', plaintext, salt, 100000)
    hex_hash = digest.hex()
    return hex_hash

def store_pass(password):
    salt=os.urandom(32)
    hashed_password = create_hash(password,salt)
    return [hashed_password, salt.decode('latin1')]

def check_password(account, userPassword):
    hash_password_InDB = account['password'][0]
    salt = account['password'][1].encode('latin1')
    hex_hash = create_hash(userPassword,salt)
    return hex_hash == hash_password_InDB