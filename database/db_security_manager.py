import base64
import sys
sys.modules['Crypto'] = __import__('crypto')

from crypto.Cipher import AES
from crypto.Util.Padding import unpad, pad

class DBSecurityManager():
    secret_key = b'HOTYE49jV2DpF7iF55p1aVov6vWEaeuq'
    def __init__(self) -> None:
        pass

    def encode_message(self, message:str) -> str:
        iv = base64.b64encode(AES.get_random_bytes(16))[:16]
        
        cipher = AES.new(self.secret_key, AES.MODE_CBC, iv)

        padded_data = pad(message.encode('utf-8'), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        
        encrypted_message = base64.b64encode(iv + encrypted_data).decode('utf-8')
        return encrypted_message

    def decode_message(self, message:str) -> str:
        encrypted_with_iv = base64.b64decode(message)
        
        iv = encrypted_with_iv[:16]
        encrypted_data = encrypted_with_iv[16:]

        cipher = AES.new(self.secret_key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        return decrypted.decode('utf-8')