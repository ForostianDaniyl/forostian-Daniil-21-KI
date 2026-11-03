import hashlib


def hash_demo(text="lab4"):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()