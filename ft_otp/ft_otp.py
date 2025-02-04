import hmac
import time
import struct
import rsa
import argparse
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_keys():
    private_key = RSA.generate(2048)

    public_key = private_key.publickey()

    with open ("private.pem", "wb") as prv_file:
        prv_file.write(private_key.exportKey('PEM'))

    with open ("public.pem", "wb") as pub_file:
        pub_file.write(public_key.exportKey('PEM'))

def open_keys():
    with open ("private.pem", "rb") as file:
        private_key = RSA.import_key(file.read())

    with open ("public.pem", "rb") as file:
        public_key =  RSA.import_key(file.read())
    return private_key, public_key

def encrypt_key(fileName):
    private_key, public_key = open_keys()

    cipher = PKCS1_OAEP.new(public_key)

    with open (fileName, "rb") as file:
        data_to_encrypt = file.read()

    try:
        int(data_to_encrypt, 16)
        if len(str(data_to_encrypt)) != 67:
            raise Exception("error: key must be 64 hexadecimal characters.")
    except Exception as e:
        err(e)

    encrypted = cipher.encrypt(data_to_encrypt)

    with open ("ft_otp.key", "wb") as file:
        file.write(encrypted)


def decrypt_key():
    private_key, public_key = open_keys()

    decipher = PKCS1_OAEP.new(private_key)

    with open ("ft_otp.key", "rb") as file:
        encrypted = file.read()

    decrypted = decipher.decrypt(encrypted)

    return decrypted.decode('ascii')

def err(errorMsg):
    print(errorMsg)
    exit(1)

def generate_TOTP(fileName):

    open_keys()
    key = decrypt_key()

    print(key)

    try:
        int(key, 16)
        if len(str(key)) != 64:
            raise Exception("error: key must be 64 hexadecimal characters.")
    except Exception as e:
        err(e)

    byte_key = bytes.fromhex(key.strip())

    byte_timestamp = struct.pack('!Q', int(time.time() / 30))

    obj = hmac.new(byte_key, byte_timestamp, 'sha1')

    full_hash = obj.digest()

    offset = full_hash[-1] & 0x0F

    selected_bytes = full_hash[offset : offset + 4]

    code_int = int.from_bytes(selected_bytes, 'big') & 0x7FFFFFFF

    totp_code = code_int % 1000000

    print(f"TOTP code :{totp_code : 07d}")

def generate_crypted_key(fileName):
    generate_keys()
    open_keys()
    encrypt_key(fileName)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='This program generates a TOTP code based on a given key')

    parser.add_argument('-g', "--generate", nargs='?')
    parser.add_argument('-k', "--keyfile", nargs='?')
    args = parser.parse_args()

    # print(args.keyfile, args.generate)

    if not args.keyfile and not args.generate or args.keyfile and args.generate:
        err("error: either -k keyfile.key or -g keyfile.hex is needed")

    try:
        if args.generate:
            generate_crypted_key(args.generate)
        elif args.keyfile:
            generate_TOTP(args.keyfile)
    except Exception as e:
        err(e)
