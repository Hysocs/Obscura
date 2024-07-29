import os
import base64
import zlib
import marshal
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from cryptography.fernet import Fernet
from Core.utils import CodeGenerator, name_generator

class CodeEncryptor:
    @staticmethod
    def encrypt_code_aes(code, secret_key):
        iv = os.urandom(16)
        cipher = AES.new(secret_key, AES.MODE_CBC, iv)
        encrypted_code = cipher.encrypt(pad(code.encode('utf-8'), AES.block_size))
        return base64.b64encode(iv + encrypted_code + secret_key).decode('utf-8')

    @staticmethod
    def encrypt_code_base64(code):
        return base64.b64encode(code.encode('utf-8')).decode('utf-8')

    @staticmethod
    def encrypt_code_anti_v(code):
        secret_key = Fernet.generate_key()
        cipher_suite = Fernet(secret_key)
        encrypted_data = cipher_suite.encrypt(zlib.compress(code.encode()))
        marshalled_data = marshal.dumps(encrypted_data)
        compressed_data = zlib.compress(marshalled_data)
        return secret_key, base64.b64encode(compressed_data).decode('utf-8')

    @staticmethod
    def encrypt_code_hash(code):
        secret_key = Fernet.generate_key()
        cipher_suite = Fernet(secret_key)
        encrypted_data = cipher_suite.encrypt(zlib.compress(code.encode()))
        marshalled_data = marshal.dumps(encrypted_data)
        compressed_data = zlib.compress(marshalled_data)
        original_hash = hashlib.sha256(code.encode()).hexdigest()
        return secret_key, base64.b64encode(compressed_data).decode('utf-8'), original_hash

    @staticmethod
    def generate_decryption_stub_aes(inject_anti_debug):
        anti_debug_code = CodeGenerator.generate_anti_debug_code() if inject_anti_debug else ""

        stub_template = f"""
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import random
import types

def get4():
    return 2 + 2

def get8():
    return get4() + get4()

def get10():
    return 5 * 2

def get6():
    return 3 * 2

def get16():
    return get10() + get6()

def get32():
    return get16() * 2

def part1(data):
    part1 = data[:get8()]
    part2 = data[get8():get16()]
    part3 = data[get16():-get32()]
    part4 = data[-get32():-get16()]
    part5 = data[-get16():]
    return part1 + part2, part3 + part4, part5

def part2(iv, encryptedcode, secretkey):
    c = AES.new(secretkey, AES.MODE_CBC, iv)
    dummyoperation = len(iv) + len(encryptedcode) + len(secretkey)
    return unpad(c.decrypt(encryptedcode), AES.block_size).decode('utf-8')

def part3(encodeddata):
    d = base64.b64decode(encodeddata)
    i, e, s = part1(d)
    return part2(i, e, s)

def part4(data):
    dummylist = [chr((ord(c) + 1) % 256) for c in 'dummy']
    for _ in dummylist:
        pass  # No-op loop

def part5(data):
    part4(data)
    result = data[::-1]
    part4(result)
    result = result[::-1]
    part4(result)
    return part3(result)

def assemblekey():
    part1 = bytes([18, 52, 86, 120])
    part2 = bytes([154, 188, 222, 240])
    part3 = bytes([1, 35, 69, 103])
    part4 = bytes([137, 171, 205, 239])
    key = part1 + part2 + part3 + part4
    key = bytearray(key)
    random.shuffle(key)
    key = bytes(key)
    return key

def part6(data):
    key = assemblekey()
    return part5(data)

def createsecureexec():
    # Obfuscate function creation to avoid easy replacement
    def secureexec(decryptedcode):
        # Use compile and exec to minimize exposure
        exec(compile(decryptedcode, '<string>', 'exec'), globals())
    return secureexec

class EncryptedLoader(types.ModuleType):
    def __init__(self, encryptedcode):
        super().__init__('encryptedmodule')
        self.encryptedcode = encryptedcode

    def load(self):
        decryptedcode = part5(self.encryptedcode)
        secureexec = createsecureexec()
        secureexec(decryptedcode)

{anti_debug_code}

encryptedcode = '''{{encrypted_code}}'''
loader = EncryptedLoader(encryptedcode)
loader.load()
"""
        final_stub_code = stub_template.replace("{encrypted_code}", "{encrypted_code}")

        return final_stub_code

    @staticmethod
    def generate_decryption_stub_base64(inject_anti_debug):
        anti_debug_code = CodeGenerator.generate_anti_debug_code() if inject_anti_debug else ""

        stub_template = f"""
import base64
import marshal
import random
import types

def get4():
    return 2 + 2

def get8():
    return get4() + get4()

def get10():
    return 5 * 2

def get6():
    return 3 * 2

def get16():
    return get10() + get6()

def get32():
    return get16() * 2

def part4(data):
    dummylist = [chr((ord(c) + 1) % 256) for c in 'dummy']
    for _ in dummylist:
        pass  # No-op loop

def part5(data):
    part4(data)
    result = data[::-1]
    part4(result)
    result = result[::-1]
    part4(result)
    return base64.b64decode(data).decode('utf-8')

def createsecureexec():
    # Obfuscate function creation to avoid easy replacement
    def secureexec(decryptedcode):
        # Use compile and exec to minimize exposure
        exec(compile(decryptedcode, '<string>', 'exec'), globals())
    return secureexec

class EncryptedLoader(types.ModuleType):
    def __init__(self, encryptedcode):
        super().__init__('encryptedmodule')
        self.encryptedcode = encryptedcode

    def load(self):
        decryptedcode = part5(self.encryptedcode)
        secureexec = createsecureexec()
        secureexec(decryptedcode)

{anti_debug_code}

encryptedcode = '''{{encrypted_code}}'''
loader = EncryptedLoader(encryptedcode)
loader.load()
"""

        final_stub_code = stub_template.replace("{encrypted_code}", "{encrypted_code}")

        return final_stub_code

    @staticmethod
    def generate_decryption_stub_anti_v(inject_anti_debug):
        anti_debug_code = CodeGenerator.generate_anti_debug_code() if inject_anti_debug else ""

        stub_template = f"""
import base64
import zlib
import marshal
from cryptography.fernet import Fernet
import random

def get4():
    return 2 + 2

def get8():
    return get4() + get4()

def get10():
    return 5 * 2

def get6():
    return 3 * 2

def get16():
    return get10() + get6()

def get32():
    return get16() * 2

def part4(data):
    dummylist = [chr((ord(c) + 1) % 256) for c in 'dummy']
    for _ in dummylist:
        pass  # No-op loop

def part5(data):
    part4(data)
    result = data[::-1]
    part4(result)
    result = result[::-1]
    part4(result)
    return base64.b64decode(data + '=' * (-len(data) % 4))

def assemblekey():
    part1 = bytes([18, 52, 86, 120])
    part2 = bytes([154, 188, 222, 240])
    part3 = bytes([1, 35, 69, 103])
    part4 = bytes([137, 171, 205, 239])
    key = part1 + part2 + part3 + part4
    key = bytearray(key)
    random.shuffle(key)
    key = bytes(key)
    return key

def part6(data):
    key = assemblekey()
    return part5(data)

def createsecureexec():
    # Obfuscate function creation to avoid easy replacement
    def secureexec(decryptedcode):
        # Use compile and exec to minimize exposure
        exec(compile(decryptedcode, '<string>', 'exec'), globals())
    return secureexec

{anti_debug_code}

key = base64.b64decode('{{encryption_key}}')
encrypteddata = base64.b64decode('{{encrypted_data}}')

# Decompress and load the marshaled data
decompresseddata = zlib.decompress(encrypteddata)
marshalleddata = marshal.loads(decompresseddata)

# Decrypt the data
ciphersuite = Fernet(key)
decrypteddata = ciphersuite.decrypt(marshalleddata)

# Decompress the decrypted data and execute
finaldata = zlib.decompress(decrypteddata).decode()
secureexec = createsecureexec()
secureexec(finaldata)
"""
        final_stub_code = stub_template.replace("{encryption_key}", "{encryption_key}").replace("{encrypted_data}", "{encrypted_data}")

        return final_stub_code

    @staticmethod
    def generate_decryption_stub_hash(inject_anti_debug):
        anti_debug_code = CodeGenerator.generate_anti_debug_code() if inject_anti_debug else ""

        stub_template = f"""
import base64
import zlib
import marshal
from cryptography.fernet import Fernet
import random
import hashlib

{anti_debug_code}

def get4():
    return 2 + 2

def get8():
    return get4() + get4()

def get10():
    return 5 * 2

def get6():
    return 3 * 2

def get16():
    return get10() + get6()

def get32():
    return get16() * 2

def part4(data):
    dummylist = [ord(c) + 1 for c in 'dummy']
    for _ in dummylist:
        pass  # No-op loop

def part5(data):
    part4(data)
    result = data[::-1]
    part4(result)
    result = result[::-1]
    part4(result)
    return base64.b64decode(data + '=' * (-len(data) % 4))

def assemblekey():
    part1 = bytes([18, 52, 86, 120])
    part2 = bytes([154, 188, 222, 240])
    part3 = bytes([1, 35, 69, 103])
    part4 = bytes([137, 171, 205, 239])
    key = part1 + part2 + part3 + part4
    key = bytearray(key)
    random.shuffle(key)
    key = bytes(key)
    return key

def part6(data):
    key = assemblekey()
    return part5(data)

def verifyintegrity(data, expectedhash):
    actualhash = hashlib.sha256(data.encode()).hexdigest()
    return actualhash == expectedhash

def createsecureexec():
    # Obfuscate function creation to avoid easy replacement
    def secureexec(decryptedcode):
        # Use compile and exec to minimize exposure
        exec(compile(decryptedcode, '<string>', 'exec'), globals())
    return secureexec

key = base64.b64decode('{{encryption_key}}')
encrypteddata = base64.b64decode('{{encrypted_data}}')
expectedhash = '{{expected_hash}}'

# Decompress and load the marshaled data
decompresseddata = zlib.decompress(encrypteddata)
marshalleddata = marshal.loads(decompresseddata)

# Decrypt the data
ciphersuite = Fernet(key)
decrypteddata = ciphersuite.decrypt(marshalleddata)

# Decompress the decrypted data and verify integrity
finaldata = zlib.decompress(decrypteddata).decode()

def fakefunc1():
    pass

def fakefunc2(x):
    return x

def fakefunc3(y, z):
    if isinstance(y, (int, float)) and isinstance(z, (int, float)):
        return y + z
    return y

if verifyintegrity(finaldata, expectedhash):
    # Execute the code using dynamic import
    part1 = "uselessstring_" + "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", k=20))
    part2 = 42
    part3 = 3.14159
    part4 = part2 + part3
    part5 = []
    for _ in range(10):
        part5.append(random.randint(0, 100))
    part6 = dict()
    for i in range(10):
        part6[i] = i

    execfunc = getattr(__import__('builtins'), 'exec')

    part7 = []
    for i in range(10):
        part7.append(i)
    part8 = 0
    for i in range(10):
        part8 += i * i
    part9 = ""
    for i in range(10):
        part9 += chr((i % 26) + 97)
    part10 = "".join(random.choices("0123456789abcdef", k=10))

    fakefunc1()
    fakefunc2(part1)
    fakefunc3(part2, part3)

    secureexec = createsecureexec()
    secureexec(finaldata)

    part11 = len(part5) * part2
    part12 = part4 / part3
    part13 = part8 - part11
    part14 = [part1, part9, part10]
    for _ in range(10):
        part12 += 1

    fakefunc1()
    fakefunc2(part3)
    fakefunc3(part2, part3)  # Using only numerical types
else:
    print("Code integrity verification failed.")
"""
        final_stub_code = stub_template.replace("{encryption_key}", "{encryption_key}").replace("{encrypted_data}", "{encrypted_data}").replace("{expected_hash}", "{expected_hash}")

        return final_stub_code
