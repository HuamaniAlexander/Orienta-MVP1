from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError


class ArgonPasswords:
    def __init__(self):
        self.hasher = PasswordHasher()
        self.dummy = self.hasher.hash("dummy-password-for-timing-only")

    def hash(self, value):
        return self.hasher.hash(value)

    def verify(self, value, hashed):
        try:
            return self.hasher.verify(hashed or self.dummy, value) and hashed is not None
        except (VerificationError, InvalidHashError):
            return False
