import hashlib


def str_md5_encrypt(proclaimed):
    proclaimed = bytes(proclaimed, encoding='utf-8')
    ciphertext = hashlib.md5(proclaimed).hexdigest()
    return ciphertext
