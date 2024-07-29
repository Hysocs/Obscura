import zlib
import base64
import logging

logger = logging.getLogger(__name__)

def compress_code(code, repeat_count=1):
    try:
        compressed_code = code.encode('utf-8')
        for _ in range(repeat_count):
            compressed_code = zlib.compress(compressed_code, 9)
        
        base64_encoded = base64.b64encode(compressed_code)
        further_compressed = zlib.compress(base64_encoded, 9)
        final_base64_encoded = base64.b64encode(further_compressed).decode('utf-8')

        decompression_stub = f"""
import zlib, base64
exec(zlib.decompress(base64.b64decode(zlib.decompress(base64.b64decode('{final_base64_encoded}')))).decode('utf-8'))
"""

        return decompression_stub
    except Exception as e:
        logger.error(f"Error compressing code: {e}")
        return code
