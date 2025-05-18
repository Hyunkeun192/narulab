# narulab/utils/encryption.py

from Crypto.Cipher import AES
import base64
import hashlib

# ✅ 실제 사용 중인 암호화 키로 교체해야 함
SECRET_KEY = "narulab-secret-key"

def get_cipher():
    key = hashlib.sha256(SECRET_KEY.encode()).digest()
    iv = key[:16]
    return AES.new(key, AES.MODE_CBC, iv)

def aes_decrypt(encrypted_text):
    cipher = get_cipher()
    decoded = base64.b64decode(encrypted_text)
    decrypted = cipher.decrypt(decoded)
    pad = decrypted[-1]
    return decrypted[:-pad].decode('utf-8')
