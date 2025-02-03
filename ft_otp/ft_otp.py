import hmac
import time
import struct
import rsa

with open('key.hex',  'r')as file:
    key = file.read()

try:
    int(key, 16)
except:
    print("error: key must be 64 hexadecimal characters.")

byte_key = bytes.fromhex(key.strip())

byte_timestamp = struct.pack('!Q', int(time.time() / 30))
# print(byte_timestamp)

obj = hmac.new(byte_key, byte_timestamp, 'sha1')

# print(obj.digest())

full_hash = obj.digest()

offset = full_hash[-1] & 0x0F

selected_bytes = full_hash[offset : offset + 4]

code_int = int.from_bytes(selected_bytes, 'big') & 0x7FFFFFFF

totp_code = code_int % 1000000

print(totp_code)

