import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import base64

class DeniableEncryption:
    def __init__(self):
        # Generate primary key pair
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()
         # Generate deniable key pair (decoy)
        self.deniable_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.deniable_public_key = self.deniable_private_key.public_key()

    def encrypt(self, message, use_deniable=False):
        """
        Encrypt message using either primary or deniable public key
        :param message: String message to encrypt
        :param use_deniable: Boolean to choose encryption key
        :return: Base64 encoded encrypted message
        """
        try:
             # Choose which public key to use based on the flag
            key_to_use = self.deniable_public_key if use_deniable else self.public_key
            
            # Convert message to bytes
            message_bytes = message.encode('utf-8')
            
            # Encrypt using OAEP padding
            encrypted = key_to_use.encrypt(
                message_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
                     # Return base64 encoded encrypted message
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            return f"Encryption Error: {str(e)}"

    def decrypt(self, encrypted_message, use_deniable=False):
        """
        Decrypt message using either primary or deniable private key
        :param encrypted_message: Base64 encoded encrypted message
        :param use_deniable: Boolean to choose decryption key
        :return: Decrypted message string
        """
        try:
            # Choose which private key to use based on the flag
            key_to_use = self.deniable_private_key if use_deniable else self.private_key
            
            # Decode base64 message
            encrypted_bytes = base64.b64decode(encrypted_message)
            
            # Decrypt using OAEP padding
            decrypted = key_to_use.decrypt(
                encrypted_bytes,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Return decoded message
            return decrypted.decode('utf-8')
        except Exception as e:
            return f"Decryption Error: {str(e)}"
