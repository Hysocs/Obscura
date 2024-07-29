import re
import logging

logger = logging.getLogger(__name__)

def convert_number_to_hex(match):
    value = match.group(0)
    try:
        if '.' in value:  # float
            integer_part, fractional_part = value.split('.')
            integer_part = int(integer_part)
            fractional_part = float('0.' + fractional_part)
            hex_value = f"0x{integer_part:x} + {fractional_part:.15f}"
            # Verify the converted value
            if abs(eval(hex_value) - float(value)) < 1e-9:
                #logger.info(f"Converting {value} to {hex_value}")
                return hex_value
            else:
                logger.error(f"Conversion mismatch for {value}")
                return value
        else:  # int
            hex_value = f"0x{int(value):x}"
            # Verify the converted value
            if eval(hex_value) == int(value):
                #logger.info(f"Converting {value} to {hex_value}")
                return hex_value
            else:
                logger.error(f"Conversion mismatch for {value}")
                return value
    except Exception as e:
        logger.error(f"Error converting {value} to hex: {e}")
        return value

def obfuscate_numbers_to_hex(code):
    try:
        # Regex to find all numeric literals (integers and floats)
        pattern = re.compile(r'\b\d+(\.\d+)?\b')
        obfuscated_code = re.sub(pattern, convert_number_to_hex, code)
        #logger.info(f"Number to hex obfuscation applied:\n{obfuscated_code}")
        return obfuscated_code
    except Exception as e:
        logger.error(f"Error in number to hex obfuscation: {e}")
        return code
