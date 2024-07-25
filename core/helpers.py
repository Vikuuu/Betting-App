import secrets
import random


def generate_access_medium():
    return secrets.token_urlsafe(16)


def generate_otp():
    return random.randint(100000, 999999)
