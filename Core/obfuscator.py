import logging
import os
import base64
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QObject, pyqtSignal
from concurrent.futures import ThreadPoolExecutor
from Core.encryptor import CodeEncryptor
from Core.obfuscators.inline_code import inline_code_obfuscate
from Core.obfuscators.control_flow import control_flow_obfuscate
from Core.obfuscators.control_flow_flatten import control_flow_flatten_obfuscate  # Import the new obfuscator
from Core.obfuscators.function_mirroring import function_mirroring_obfuscate
from Core.obfuscators.number_to_hex import obfuscate_numbers_to_hex
from Core.obfuscators.obfuscate_constants import obfuscate_constants
from Core.obfuscators.obfuscate_identifiers import obfuscate_identifiers
from Core.obfuscators.opaque_predicates import insert_opaque_predicates
from Core.obfuscators.dummy_variable_inserter import insert_dummy_variables
from Core.compress import compress_code

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CodeObfuscator(QObject):
    obfuscation_complete_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    @staticmethod
    def handle_number_to_hex(code, number_to_hex):
        if number_to_hex:
            logger.info("Applying number to hex obfuscation")
            code = obfuscate_numbers_to_hex(code)
        return code

    @staticmethod
    def handle_inline_code_replacement(code, inline_code_replacement, is_reobfuscation):
        if inline_code_replacement and not is_reobfuscation:
            logger.info("Applying inline code obfuscation")
            code = inline_code_obfuscate(code)
        return code

    @staticmethod
    def handle_control_flow_obfuscation(code, control_flow_obfuscation):
        if control_flow_obfuscation:
            logger.info("Applying control flow obfuscation")
            code = control_flow_obfuscate(code)
        return code

    @staticmethod
    def handle_control_flow_flatten_obfuscation(code, control_flow_flatten_obfuscation):
        if control_flow_flatten_obfuscation:
            logger.info("Applying control flow flatten obfuscation")
            code = control_flow_flatten_obfuscate(code)
        return code

    @staticmethod
    def handle_function_mirroring(code, function_mirroring):
        if function_mirroring:
            logger.info("Applying function mirroring obfuscation")
            code = function_mirroring_obfuscate(code)
        return code

    @staticmethod
    def handle_obfuscate_constants(code, obfuscate_constants_flag):
        if obfuscate_constants_flag:
            logger.info("Applying constants obfuscation")
            code = obfuscate_constants(code)
        return code

    @staticmethod
    def handle_obfuscate_identifiers(code, obfuscate_identifiers_flag):
        if obfuscate_identifiers_flag:
            logger.info("Applying identifiers obfuscation")
            code = obfuscate_identifiers(code)
        return code

    @staticmethod
    def handle_opaque_predicates(code, opaque_predicates_flag):
        if opaque_predicates_flag:
            logger.info("Applying opaque predicates obfuscation")
            code = insert_opaque_predicates(code)
        return code
    
    @staticmethod
    def handle_dummy_variables(code, insert_dummy_variables_flag):
        if insert_dummy_variables_flag:
            logger.info("Inserting dummy variables and arguments")
            code = insert_dummy_variables(code)
        return code
    
    @staticmethod
    def handle_encryption(full_code, options, is_reobfuscation=False):
        if not options['encrypt_code'] or is_reobfuscation:
            return full_code

        encryption_method = options['encryption_method']
        if encryption_method == "AES (Requires pycryptodome)":
            secret_key = os.urandom(16)
            encrypted_code = CodeEncryptor.encrypt_code_aes(full_code, secret_key)
            decryption_stub = CodeEncryptor.generate_decryption_stub_aes(options['inject_anti_debug'])
            decryption_stub_code = decryption_stub.format(encrypted_code=encrypted_code)
        elif encryption_method == "Base64 (Default Python)":
            encrypted_code = CodeEncryptor.encrypt_code_base64(full_code)
            decryption_stub = CodeEncryptor.generate_decryption_stub_base64(options['inject_anti_debug'])
            decryption_stub_code = decryption_stub.format(encrypted_code=encrypted_code)
        elif encryption_method == "Hybrid (Anti-V)":
            secret_key, encrypted_data = CodeEncryptor.encrypt_code_anti_v(full_code)
            decryption_stub = CodeEncryptor.generate_decryption_stub_anti_v(options['inject_anti_debug'])
            decryption_stub_code = decryption_stub.format(encryption_key=base64.b64encode(secret_key).decode(), encrypted_data=encrypted_data)
        elif encryption_method == "Hybrid Hash (Custom Method)":
            secret_key, encrypted_data, original_hash = CodeEncryptor.encrypt_code_hash(full_code)
            decryption_stub = CodeEncryptor.generate_decryption_stub_hash(options['inject_anti_debug'])
            decryption_stub_code = decryption_stub.format(encryption_key=base64.b64encode(secret_key).decode(), encrypted_data=encrypted_data, expected_hash=original_hash)
        else:
            logger.error("No valid encryption method found")
            return full_code

        if options['obfuscate_decryption_stub']:
            try:
                logger.info("Starting decryption stub obfuscation")
                obfuscated_decryption_stub = CodeObfuscator.obfuscate_code(decryption_stub_code, options, is_reobfuscation=True)
                logger.info("Decryption stub obfuscation completed successfully")
                return obfuscated_decryption_stub
            except Exception as e:
                logger.error(f"Error obfuscating decryption stub: {e}")
                return decryption_stub_code
        else:
            return decryption_stub_code

    @staticmethod
    def obfuscate_code(code, options, is_reobfuscation=False):
        try:
            logger.info("Starting code obfuscation")
            logger.info(f"Obfuscate code called with options={options}")

            # Apply direct code transformations
            code = CodeObfuscator.handle_dummy_variables(code, options.get("insert_dummy_variables", False))
            code = CodeObfuscator.handle_opaque_predicates(code, options.get("opaque_predicates", False))
            code = CodeObfuscator.handle_obfuscate_identifiers(code, options.get("obfuscate_identifiers", False))
            code = CodeObfuscator.handle_inline_code_replacement(code, options.get("inline_code_replacement", False), is_reobfuscation)
            code = CodeObfuscator.handle_control_flow_obfuscation(code, options.get("control_flow_obfuscation", False))
            code = CodeObfuscator.handle_control_flow_flatten_obfuscation(code, options.get("control_flow_flatten_obfuscation", False))
            code = CodeObfuscator.handle_function_mirroring(code, options.get("function_mirroring", False))
            code = CodeObfuscator.handle_obfuscate_constants(code, options.get("obfuscate_constants", False))
            code = CodeObfuscator.handle_number_to_hex(code, options.get("number_to_hex", False))
            
            
            logger.info("Code obfuscation completed successfully")

            # Apply encryption if necessary
            full_code = CodeObfuscator.handle_encryption(code, options, is_reobfuscation)

            # Compress the code if needed
            if options.get("compress_code_flag", False):
                for _ in range(options.get("repeat_count", 1)):
                    full_code = compress_code(full_code, 1)

            return full_code
        except Exception as e:
            logger.error(f"Error obfuscating code: {e}")
            return code

    @staticmethod
    def obfuscate_file(file_path, options):
        try:
            normalized_file_path = os.path.normpath(file_path)
            
            logger.info(f"Starting obfuscation for file: {normalized_file_path}")
            logger.debug(f"Normalized file path: {normalized_file_path}")

            if not os.path.exists(normalized_file_path):
                raise FileNotFoundError(f"The file {normalized_file_path} does not exist.")
            
            with open(normalized_file_path, 'r', encoding='utf-8') as file:
                original_code = file.read()

            obfuscated_code = CodeObfuscator.obfuscate_code(original_code, options)

            base, ext = os.path.splitext(normalized_file_path)
            new_file_path = f"{base}_obfuscated{ext}"

            if os.path.exists(new_file_path):
                response = QMessageBox.question(None, "File Exists", f"The file {new_file_path} already exists. Do you want to overwrite it?",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if response == QMessageBox.No:
                    logger.info("File overwrite canceled by user")
                    return None

                with open(new_file_path, 'w', encoding='utf-8') as file:
                    file.write('')
                logger.info(f"Emptied existing file: {new_file_path}")

            with open(new_file_path, 'w', encoding='utf-8') as file:
                file.write(obfuscated_code)

            if not os.path.exists(new_file_path) or os.path.getsize(new_file_path) == 0:
                raise IOError(f"Failed to write to {new_file_path}")
            
            logger.info(f"Obfuscated file written to: {new_file_path}")
            return new_file_path
        except UnicodeDecodeError as e:
            logger.error(f"Error obfuscating file {normalized_file_path}: {e}")
            return None
        except FileNotFoundError as e:
            logger.error(f"Error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error obfuscating file {normalized_file_path}: {e}")
            return None
