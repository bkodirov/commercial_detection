from Crypto.Cipher import AES
from m3u8 import Segment


def is_encrypted(segment: Segment):
    return segment.key


def decrypt_aes128cbc(blob_bytes: [bytes], key_bytes: [bytes], iv_string: str):
    cipher = AES.new(key_bytes, AES.MODE_CBC, int(iv_string, 16).to_bytes(16, byteorder='big'))
    return cipher.decrypt(blob_bytes)
