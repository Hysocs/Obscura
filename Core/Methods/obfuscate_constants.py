import ast
import astor
import logging
import random
from Core.utils import NameGenerator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
COMPLEXITY = 1  # Control the obfuscation complexity
MAX_CHUNK_SIZE = 1000  # Maximum chunk size to prevent excessive recursion
MIN_CHUNK_SIZE = 50  # Minimum chunk size for strings
CHUNK_SIZE_INCREMENT = 50  # Increment chunk size if a recursion error occurs

existing_functions = {}  # Global dictionary to track existing function definitions

# Instantiate the NameGenerator
name_generator = NameGenerator()

def generate_expression(value):
    while True:
        a = random.randint(1, 10)
        b = random.randint(-100, 100)
        c = value // (a + b) if (a + b) != 0 else 1
        d = (a + b) * c - value
        e = random.randint(1, 10)
        f = (a + b) * c - d

        patterns = [
            f"(({a} + {b}) * {c} - {d}) // {e} + {f}",
            f"(({b} + {a}) * {c} - {d}) // {e} + {f}",
            f"(({a} + {b}) // {e} * {c} - {d}) + {f}",
            f"(({a} * {c} + {b}) - {d}) // {e} + {f}",
            f"(({b} - {d}) * {c} // {e}) + {a + f}"
        ]
        expression = random.choice(patterns)

        try:
            if eval(expression) == value:
                return expression
        except ZeroDivisionError:
            continue

def chunk_string(s, chunk_size):
    return [s[i:i+chunk_size] for i in range(0, len(s), chunk_size)]

def create_function_def(value, complexity, chunk_size):
    if value in existing_functions:
        return existing_functions[value]

    function_name = name_generator.generate_name()

    if isinstance(value, (int, float, complex)):
        expression = generate_expression(value)
        return_expression = ast.parse(expression).body[0].value
        function_def = ast.FunctionDef(
            name=function_name,
            args=ast.arguments(
                args=[],
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[]
            ),
            body=[
                ast.Return(value=return_expression)
            ],
            decorator_list=[]
        )
        existing_functions[value] = (function_name, [function_def])
        return function_name, [function_def]
    elif isinstance(value, str):
        if len(value) < MIN_CHUNK_SIZE:
            function_name, function_defs = create_simple_string_function(value)
        else:
            function_name, function_defs = create_string_function(value, complexity, chunk_size)
        existing_functions[value] = (function_name, function_defs)
        return function_name, function_defs
    else:
        raise ValueError(f"Unsupported constant type: {type(value)}")

def create_simple_string_function(value):
    function_name = name_generator.generate_name()
    char_values = [ord(char) for char in value]
    
    obfuscation_keys = [random.randint(1, 255) for _ in range(COMPLEXITY)]
    obfuscated_values = [(char ^ random.choice(obfuscation_keys)) for char in char_values]
    
    obfuscated_list_str = ', '.join(map(str, obfuscated_values))
    key_list_str = ', '.join(map(str, obfuscation_keys))
    
    expression = f"''.join(chr(x ^ y) for x, y in zip([{obfuscated_list_str}], [{key_list_str}] * ({len(char_values)} // {len(obfuscation_keys)} + 1)))"
    return_expression = ast.parse(expression).body[0].value

    function_def = ast.FunctionDef(
        name=function_name,
        args=ast.arguments(
            args=[],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[]
        ),
        body=[
            ast.Return(value=return_expression)
        ],
        decorator_list=[]
    )
    return function_name, [function_def]

def create_string_function(value, complexity, chunk_size):
    chunks = chunk_string(value, chunk_size)
    function_defs = []
    function_calls = []

    for chunk in chunks:
        function_name = name_generator.generate_name()
        char_values = [ord(char) for char in chunk]
        
        obfuscation_keys = [random.randint(1, 255) for _ in range(complexity)]
        obfuscated_values = [(char ^ random.choice(obfuscation_keys)) for char in char_values]
        
        obfuscated_list_str = ', '.join(map(str, obfuscated_values))
        key_list_str = ', '.join(map(str, obfuscation_keys))
        
        expression = f"''.join(chr(x ^ y) for x, y in zip([{obfuscated_list_str}], [{key_list_str}] * ({len(char_values)} // {len(obfuscation_keys)} + 1)))"
        return_expression = ast.parse(expression).body[0].value

        function_def = ast.FunctionDef(
            name=function_name,
            args=ast.arguments(
                args=[],
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[]
            ),
            body=[
                ast.Return(value=return_expression)
            ],
            decorator_list=[]
        )
        function_defs.append(function_def)
        function_calls.append(ast.Call(func=ast.Name(id=function_name, ctx=ast.Load()), args=[], keywords=[]))

    if len(function_calls) == 0:
        raise ValueError("No function calls generated. This usually indicates an empty input string.")

    if len(function_calls) == 1:
        final_function_name = name_generator.generate_name()
        final_function_def = ast.FunctionDef(
            name=final_function_name,
            args=ast.arguments(
                args=[],
                vararg=None,
                kwonlyargs=[],
                kw_defaults=[],
                kwarg=None,
                defaults=[]
            ),
            body=[
                ast.Return(value=function_calls[0])
            ],
            decorator_list=[]
        )
        function_defs.append(final_function_def)
        return final_function_name, function_defs

    join_expression = ast.BinOp(left=function_calls[0], op=ast.Add(), right=function_calls[1])
    for call in function_calls[2:]:
        join_expression = ast.BinOp(left=join_expression, op=ast.Add(), right=call)

    final_function_name = name_generator.generate_name()
    final_function_def = ast.FunctionDef(
        name=final_function_name,
        args=ast.arguments(
            args=[],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[]
        ),
        body=[
            ast.Return(value=join_expression)
        ],
        decorator_list=[]
    )

    function_defs.append(final_function_def)
    return final_function_name, function_defs

class ConstantObfuscator(ast.NodeTransformer):
    def __init__(self):
        self.constant_mapping = {}
        self.function_definitions = []

    def visit_Constant(self, node):
        value = node.value
        if isinstance(value, (int, float, complex, str)):
            if value not in self.constant_mapping:
                chunk_size = self.determine_chunk_size(value)
                function_name, function_defs = create_function_def(value, COMPLEXITY, chunk_size)
                self.constant_mapping[value] = function_name
                self.function_definitions.extend(function_defs)
            function_name = self.constant_mapping[value]
            return ast.Call(func=ast.Name(id=function_name, ctx=ast.Load()), args=[], keywords=[])
        return node

    def visit_JoinedStr(self, node):
        new_values = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                if value.value not in self.constant_mapping:
                    chunk_size = self.determine_chunk_size(value.value)
                    function_name, function_defs = create_function_def(value.value, COMPLEXITY, chunk_size)
                    self.constant_mapping[value.value] = function_name
                    self.function_definitions.extend(function_defs)
                function_name = self.constant_mapping[value.value]
                new_values.append(ast.FormattedValue(value=ast.Call(func=ast.Name(id=function_name, ctx=ast.Load()), args=[], keywords=[]), conversion=-1))
            else:
                new_values.append(self.visit(value))
        return ast.JoinedStr(values=new_values)

    def visit_Module(self, node):
        self.generic_visit(node)
        node.body = self.function_definitions + node.body
        return node

    def determine_chunk_size(self, value):
        length = len(value) if isinstance(value, str) else value.bit_length()
        chunk_size = min(MAX_CHUNK_SIZE, max(MIN_CHUNK_SIZE, length // 10))
        return chunk_size

def obfuscate_constants(code):
    while True:
        try:
            tree = ast.parse(code)
            obfuscator = ConstantObfuscator()
            obfuscator.visit(tree)
            return astor.to_source(tree)
        except RecursionError as e:
            logger.error(f"Recursion error: {e}")
            break
        except Exception as e:
            logger.error(f"Error obfuscating code: {e}")
            raise
