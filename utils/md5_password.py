import hashlib


def get_md5_password(salt, password):
    md5 = hashlib.md5()
    md5.update(password.encode() + salt.encode())
    return md5.hexdigest()


