from pynamodb.attributes import UnicodeAttribute
from cryptography.fernet import Fernet

class EncryptedUnicodeAttribute(UnicodeAttribute):
    def __init__(self, encryption_key, *args, **kwargs):
        self.cipher = Fernet(encryption_key)
        super().__init__(*args, **kwargs)

    def serialize(self, value):
        encrypted_value = self.cipher.encrypt(value.encode())
        return super().serialize(encrypted_value.decode())

    def deserialize(self, value):
        decrypted_value = self.cipher.decrypt(value.encode())
        return super().deserialize(decrypted_value.decode())