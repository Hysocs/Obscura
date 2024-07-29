import random
import string
from collections import deque
import logging

logger = logging.getLogger(__name__)

class NameGenerator:
    def __init__(self):
        self.recent_names = deque(maxlen=100)  # Cache for recent names to avoid repetition
        self.valid_letters = (
            string.ascii_letters + 'αβγδεζηθικλμνξοπρστυφχψω' + 
            'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' + 
            'ԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖ' +
            'אבגדהוזחטיכלמנסעפצקרשת'
        )
        self.valid_characters = self.valid_letters + string.digits + '_'

    def random_string(self, length=8):
        while True:
            new_name = ''.join(random.choices(self.valid_characters, k=length))
            if new_name[0] in self.valid_letters:  # Ensure first character is a letter
                break
        return new_name

    def generate_name(self):
        new_name = self.random_string()
        if new_name not in self.recent_names:
            self.recent_names.append(new_name)
            return new_name
        return self.generate_name()


name_generator = NameGenerator()

def encode_string(s):
    try:
        return ', '.join(str(ord(char)) for char in s)
    except Exception as e:
        logger.error(f"Error encoding string: {e}")
        return ', '.join(str(ord(char)) for char in "error")

def reverse_string(s):
    return s[::-1]

class CodeGenerator:
    
    @staticmethod
    def generate_anti_debug_code():
        anti_debug_code = """
import sys
import time
import ctypes

def is_debugger_present():
    kernel32 = ctypes.windll.kernel32
    is_present = kernel32.IsDebuggerPresent() != 0
    return is_present

def debug_check():
    if is_debugger_present():
        print("Debugger detected! Exiting...")
        sys.exit(1)

debug_check()
"""
        return anti_debug_code

class CodeValidator:
    @staticmethod
    def validate_expression(expression, function_code, value):
        try:
            local_vars = {}
            exec(function_code, globals(), local_vars)
            result = eval(expression, globals(), local_vars)
            if isinstance(value, int):
                return result == value
            elif isinstance(value, float):
                return abs(result - value) < 0.0001
            elif isinstance(value, str):
                return result == value
            return False
        except Exception as e:
            logger.error(f"Validation exception: {e}")
            return False
